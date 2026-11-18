#!/usr/bin/env bash
# Live input level meter. Play the LOUDEST part of a record and adjust the
# capture gain in alsamixer until peaks reach about 70-80% and never 100%.
# Usage: ./levels.sh            (Ctrl+C to stop)
# Set ARCHIVER_DEVICE to use a different capture device (default plughw:0,0).
set -euo pipefail
DEVICE="${ARCHIVER_DEVICE:-plughw:0,0}"
echo "Metering $DEVICE. Ctrl+C to stop."
exec arecord -D "$DEVICE" -f S24_3LE -r 48000 -c 2 -V stereo -t raw /dev/null
