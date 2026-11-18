#!/usr/bin/env bash
# One-time setup for the archiver on the Mac mini (Debian 12).
# Usage: sudo ./setup.sh [--samba]
set -euo pipefail

if [[ $EUID -ne 0 ]]; then
  echo "Run with sudo: sudo ./setup.sh" >&2
  exit 1
fi

apt-get update
apt-get install -y alsa-utils sox flac ffmpeg python3

if [[ "${1:-}" == "--samba" ]]; then
  apt-get install -y samba
  echo
  echo "Samba installed. Add the share block from README.md to /etc/samba/smb.conf,"
  echo "then run: sudo smbpasswd -a \$SUDO_USER && sudo systemctl restart smbd"
fi

echo
echo "Audio capture devices (the Mac mini's line-in should be card 0):"
arecord -l || true
echo
echo "Next: run 'alsamixer', press F4 for capture controls, select 'Line' as the"
echo "capture source and unmute it (space bar). Then run vinyl/levels.sh."
