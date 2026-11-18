#!/usr/bin/env bash
# Copy the video off a finalized DVD (e.g. one made by the Sony VCR/DVD
# recorder) into MKV files, without re-encoding. The picture is copied
# bit-for-bit, so it's fast and lossless.
#
# Usage: ./rip-dvd.sh <name> [source] [--encode]
#   name    base name for the output files, e.g. "Christmas 1994"
#   source  DVD device (default /dev/sr0), or a folder containing
#           VIDEO_TS/ or DVD_RTAV/ (an already-mounted or copied disc)
#   --encode  also make a smaller, deinterlaced H.264 copy for phones/TVs
#             (slow on the Mac mini's Core Duo: roughly real time or slower)
#
# Output goes to $ARCHIVER_VIDEO_DIR (default ~/archive/video).
set -euo pipefail

ENCODE=0
ARGS=()
for a in "$@"; do
  if [[ "$a" == "--encode" ]]; then ENCODE=1; else ARGS+=("$a"); fi
done
if [[ ${#ARGS[@]} -lt 1 ]]; then
  sed -n '2,15p' "$0" | sed 's/^# \{0,1\}//'
  exit 1
fi

NAME="${ARGS[0]}"
SRC="${ARGS[1]:-/dev/sr0}"
OUT_DIR="${ARCHIVER_VIDEO_DIR:-$HOME/archive/video}"
mkdir -p "$OUT_DIR"

MNT=""
cleanup() { if [[ -n "$MNT" ]]; then sudo umount "$MNT" || true; rmdir "$MNT" || true; fi; }
trap cleanup EXIT

if [[ -b "$SRC" ]]; then
  MNT="$(mktemp -d)"
  echo "Mounting $SRC ..."
  sudo mount -o ro "$SRC" "$MNT"
  ROOT="$MNT"
else
  ROOT="$SRC"
fi

# Pick audio handling: DVD LPCM can't go straight into MKV, so make it FLAC.
audio_codec_for() {
  local codec
  codec="$(ffprobe -v error -analyzeduration 100M -probesize 100M -select_streams a:0 \
    -show_entries stream=codec_name -of csv=p=0 "$1" 2>/dev/null | head -n1)"
  if [[ "$codec" == pcm_* ]]; then echo flac; else echo copy; fi
}

remux() {  # remux <input (file or concat:...)> <probe file> <output.mkv>
  local in="$1" probe="$2" out="$3" acodec
  acodec="$(audio_codec_for "$probe")"
  echo "Writing $out"
  ffmpeg -hide_banner -loglevel warning -stats -fflags +genpts \
    -analyzeduration 100M -probesize 100M -i "$in" \
    -map 0:v:0 -map '0:a?' -c:v copy -c:a "$acodec" "$out"
  if [[ $ENCODE -eq 1 ]]; then
    local small="${out%.mkv} (h264).mp4"
    echo "Encoding $small (this takes a while) ..."
    ffmpeg -hide_banner -loglevel warning -stats -i "$out" \
      -vf bwdif=mode=send_frame -c:v libx264 -preset veryfast -crf 20 \
      -c:a aac -b:a 192k -movflags +faststart "$small"
  fi
}

made=0
VTS_DIR="$(find "$ROOT" -maxdepth 1 -iname VIDEO_TS -type d | head -n1)"
VR_FILE="$(find "$ROOT" -maxdepth 2 -ipath '*DVD_RTAV/VR_MOVIE.VRO' | head -n1)"

if [[ -n "$VTS_DIR" ]]; then
  # One output per title set (VTS_01, VTS_02, ...). Skip *_0.VOB (menus).
  mapfile -t SETS < <(find "$VTS_DIR" -maxdepth 1 -iname 'VTS_[0-9][0-9]_[1-9].VOB' \
    -printf '%f\n' | cut -c1-6 | tr '[:lower:]' '[:upper:]' | sort -u)
  for set in "${SETS[@]}"; do
    mapfile -t VOBS < <(find "$VTS_DIR" -maxdepth 1 -iname "${set}_[1-9].VOB" | sort)
    concat="concat:$(IFS='|'; echo "${VOBS[*]}")"
    suffix=""
    if [[ ${#SETS[@]} -gt 1 ]]; then suffix=" - ${set#VTS_}"; fi
    remux "$concat" "${VOBS[0]}" "$OUT_DIR/$NAME$suffix.mkv"
    made=$((made + 1))
  done
elif [[ -n "$VR_FILE" ]]; then
  # DVD-RW recorded in VR mode: all recordings live in one file.
  remux "$VR_FILE" "$VR_FILE" "$OUT_DIR/$NAME.mkv"
  made=1
fi

if [[ $made -eq 0 ]]; then
  echo "No VIDEO_TS or DVD_RTAV found under $ROOT. Was the disc finalized?" >&2
  exit 1
fi
echo "Done: $made file(s) in $OUT_DIR"
