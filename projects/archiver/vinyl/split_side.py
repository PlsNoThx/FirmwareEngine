#!/usr/bin/env python3
"""Split a recorded vinyl side into tagged FLAC tracks.

Finds the quiet gaps between songs, trims the lead-in and lead-out grooves,
and writes one 24-bit FLAC per track plus a FLAC master of the whole side.

Needs: sox, metaflac (Debian packages: sox, flac). Pure stdlib Python.

Examples:
  # Best: tell it how many songs are on the side
  split_side.py side-A.wav --artist "Fleetwood Mac" --album "Rumours" --tracks 6

  # Track titles from a text file (one per line), numbering continues on side B
  split_side.py side-B.wav --artist ... --album ... --titles side-b.txt --start-number 7

  # Just show where it would split, write nothing
  split_side.py side-A.wav --tracks 6 --dry-run

  # Override with your own split times (m:ss, from start of the recording)
  split_side.py side-A.wav --artist ... --album ... --splits 3:21,7:45,11:02
"""
import argparse
import array
import math
import os
import re
import shutil
import subprocess
import sys

ENV_RATE = 2000          # Hz, sample rate for the level envelope
WIN = 0.1                # seconds per level window
SMOOTH = 10              # windows (1 s) for smoothing
MIN_TRACK = 20.0         # seconds; splits closer than this are rejected
EDGE_MARGIN = 10.0       # seconds; no splits this close to music start/end


def run(cmd, **kw):
    return subprocess.run(cmd, check=True, **kw)


def envelope_db(path):
    """Return per-window level in dB (0 dB = full scale), WIN seconds each."""
    raw = run(["sox", path, "-t", "raw", "-e", "signed", "-b", "16",
               "-c", "1", "-r", str(ENV_RATE), "-"],
              stdout=subprocess.PIPE).stdout
    samples = array.array("h")
    samples.frombytes(raw[: len(raw) - len(raw) % 2])
    if sys.byteorder == "big":
        samples.byteswap()
    n = int(ENV_RATE * WIN)
    levels = []
    for i in range(0, len(samples) - n + 1, n):
        chunk = samples[i:i + n]
        power = sum(s * s for s in chunk) / n
        levels.append(10 * math.log10(power / (32768.0 ** 2) + 1e-12))
    return levels


def smooth(levels):
    """Moving average in the power domain, centred, SMOOTH windows wide."""
    p = [10 ** (l / 10) for l in levels]
    half = SMOOTH // 2
    out = []
    acc = sum(p[:half])
    count = half
    for i in range(len(p)):
        if i + half < len(p):
            acc += p[i + half]
            count += 1
        if i - half - 1 >= 0:
            acc -= p[i - half - 1]
            count -= 1
        out.append(10 * math.log10(acc / count + 1e-12))
    return out


def music_bounds(sm):
    """Trim lead-in/lead-out: music is where level is 15 dB above the floor."""
    floor = min(sm)
    loud = [i for i, l in enumerate(sm) if l > floor + 15]
    if not loud:
        sys.exit("Couldn't find any music in this recording. Check the input level.")
    start = max(0, loud[0] - int(0.5 / WIN))
    end = min(len(sm), loud[-1] + int(1.5 / WIN))
    return start, end, floor


def gap_centre(sm, i, lo, hi):
    """Expand a quiet point to its surrounding gap and return the middle."""
    limit = sm[i] + 6
    a = i
    while a > lo and sm[a - 1] < limit:
        a -= 1
    b = i
    while b < hi - 1 and sm[b + 1] < limit:
        b += 1
    return (a + b) // 2


def find_splits(sm, raw, start, end, floor, tracks):
    lo = start + int(EDGE_MARGIN / WIN)
    hi = end - int(EDGE_MARGIN / WIN)
    min_sep = int(MIN_TRACK / WIN)
    if tracks is not None:
        if tracks <= 1:
            return []
        picked = []
        for i in sorted(range(lo, hi), key=lambda k: sm[k]):
            c = gap_centre(sm, i, lo, hi)
            if all(abs(c - p) >= min_sep for p in picked):
                picked.append(c)
                if len(picked) == tracks - 1:
                    break
        if len(picked) < tracks - 1:
            print(f"Warning: only found {len(picked) + 1} tracks, not {tracks}.",
                  file=sys.stderr)
        return sorted(picked)
    # Auto mode: any quiet stretch >= 1 s close to the noise floor.
    # Uses unsmoothed levels so short (1-3 s) gaps aren't blurred away.
    limit = floor + 10
    splits, run_start = [], None
    for i in range(lo, hi):
        if raw[i] < limit:
            if run_start is None:
                run_start = i
        elif run_start is not None:
            if (i - run_start) * WIN >= 1.0:
                c = (run_start + i) // 2
                if not splits or c - splits[-1] >= min_sep:
                    splits.append(c)
            run_start = None
    return splits


def parse_time(t):
    parts = [float(x) for x in t.strip().split(":")]
    secs = 0.0
    for p in parts:
        secs = secs * 60 + p
    return secs


def fmt(secs):
    return f"{int(secs // 60)}:{secs % 60:05.2f}"


def safe(name):
    return re.sub(r'[\\/:*?"<>|]', "_", name).strip() or "untitled"


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("side", help="recorded side (WAV or FLAC)")
    ap.add_argument("--artist", default="Unknown Artist")
    ap.add_argument("--album", default="Unknown Album")
    ap.add_argument("--year", help="release year tag")
    ap.add_argument("--tracks", type=int, help="number of songs on this side (recommended)")
    ap.add_argument("--titles", help="text file with one track title per line")
    ap.add_argument("--start-number", type=int, default=1,
                    help="first track number (e.g. 7 for side B)")
    ap.add_argument("--splits", help="manual split times, e.g. 3:21,7:45")
    ap.add_argument("--out", help="output folder for the tracks "
                    "(default: $ARCHIVER_MUSIC_DIR or ~/archive/music, then <artist>/<album>)")
    ap.add_argument("--dry-run", action="store_true", help="print splits only")
    args = ap.parse_args()

    for tool in ("sox", "metaflac"):
        if not shutil.which(tool):
            sys.exit(f"Missing '{tool}'. Run: sudo apt install sox flac")

    titles = None
    if args.titles:
        with open(args.titles, encoding="utf-8") as f:
            titles = [l.strip() for l in f if l.strip()]
        if args.tracks is None and not args.splits:
            args.tracks = len(titles)

    print(f"Analysing {args.side} ...")
    levels = envelope_db(args.side)
    sm = smooth(levels)
    start, end, floor = music_bounds(sm)

    if args.splits:
        cut_times = [parse_time(t) for t in args.splits.split(",")]
    else:
        cut_times = [i * WIN for i in find_splits(sm, levels, start, end, floor, args.tracks)]

    bounds = [start * WIN] + cut_times + [end * WIN]
    segments = list(zip(bounds[:-1], bounds[1:]))
    print(f"Noise floor {floor:.1f} dB. Music {fmt(bounds[0])} to {fmt(bounds[-1])}.")
    for n, (a, b) in enumerate(segments, args.start_number):
        print(f"  Track {n:2d}: {fmt(a)} - {fmt(b)}  ({fmt(b - a)})")

    if titles and len(titles) != len(segments):
        print(f"Warning: {len(titles)} titles but {len(segments)} tracks.", file=sys.stderr)
    if args.dry_run:
        return

    music_root = os.environ.get("ARCHIVER_MUSIC_DIR", os.path.expanduser("~/archive/music"))
    masters_root = os.environ.get("ARCHIVER_MASTERS_DIR", os.path.expanduser("~/archive/masters"))
    out = args.out or os.path.join(music_root, safe(args.artist), safe(args.album))
    # Masters live outside the music library so Sonos doesn't index them.
    master_dir = os.path.join(masters_root, f"{safe(args.artist)} - {safe(args.album)}")
    os.makedirs(out, exist_ok=True)
    os.makedirs(master_dir, exist_ok=True)

    stem = os.path.splitext(os.path.basename(args.side))[0]
    master = os.path.join(master_dir, stem + ".flac")
    run(["sox", args.side, "-b", "24", master])
    print(f"Master: {master}")

    for idx, (a, b) in enumerate(segments):
        n = args.start_number + idx
        title = titles[idx] if titles and idx < len(titles) else f"Track {n}"
        path = os.path.join(out, f"{n:02d} - {safe(title)}.flac")
        run(["sox", args.side, "-b", "24", path,
             "trim", f"{a:.3f}", f"={b:.3f}", "fade", "0.005", "-0", "0.005"])
        tags = [f"--set-tag=ARTIST={args.artist}", f"--set-tag=ALBUMARTIST={args.artist}",
                f"--set-tag=ALBUM={args.album}", f"--set-tag=TITLE={title}",
                f"--set-tag=TRACKNUMBER={n}", "--set-tag=SOURCE=Vinyl"]
        if args.year:
            tags.append(f"--set-tag=DATE={args.year}")
        run(["metaflac", "--remove-all-tags", *tags, path])
        print(f"Wrote {path}")


if __name__ == "__main__":
    main()
