#!/usr/bin/env bash
# Record one side of a record to a 24-bit / 48 kHz WAV.
#
# Usage: ./record-side.sh <output-folder> <side-name> [max-minutes]
#   e.g. ./record-side.sh ~/archive/raw/rumours side-A
#
# Start this, THEN drop the needle. Press Ctrl+C after the side ends
# (or it stops on its own after max-minutes, default 35).
# Set ARCHIVER_DEVICE to use a different capture device (default plughw:0,0).
set -euo pipefail

if [[ $# -lt 2 ]]; then
  sed -n '2,10p' "$0" | sed 's/^# \{0,1\}//'
  exit 1
fi

OUT_DIR="$1"
SIDE="$2"
MAX_MIN="${3:-35}"
DEVICE="${ARCHIVER_DEVICE:-plughw:0,0}"
FILE="$OUT_DIR/$SIDE.wav"

mkdir -p "$OUT_DIR"
if [[ -e "$FILE" ]]; then
  echo "$FILE already exists; pick another side name or delete it." >&2
  exit 1
fi

echo "Recording to $FILE (max $MAX_MIN min). Drop the needle now; Ctrl+C when the side ends."
# arecord writes a valid WAV header when interrupted with Ctrl+C.
arecord -D "$DEVICE" -f S24_3LE -r 48000 -c 2 -d $((MAX_MIN * 60)) -V stereo "$FILE" || true

if [[ -s "$FILE" ]]; then
  echo
  echo "Saved $FILE"
  if command -v soxi >/dev/null; then soxi -d "$FILE" | sed 's/^/Length: /'; fi
  echo "Next: ./split_side.py \"$FILE\" --artist \"...\" --album \"...\" --tracks N --dry-run"
fi
