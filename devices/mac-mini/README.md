# Mac mini: Confirmed Intel Core Duo (Late 2006)

## Identified from the label
| Field | Value |
|---|---|
| Model | A1176, Macmini1,1 (2006) |
| Config | `MAC MINI 1.83/2X512/80/COMBO/AP/BT-USA` |
| CPU | Intel Core Duo 1.83 GHz (T2400). **32-bit only** |
| RAM | 2 x 512 MB = 1 GB (2 GB max) |
| Storage | 80 GB 2.5" SATA HDD; CD-RW/DVD combo drive |
| Wireless | Wi-Fi (AirPort) + Bluetooth |
| Power | 18.5 V 6 A brick, roughly 20-30 W at idle |
| Firmware | 32-bit EFI; can boot BIOS-mode OSes (Boot Camp CSM) |

## The 32-bit problem
Many current projects no longer ship 32-bit x86 builds:
- **Debian 13** dropped i386 as a full architecture. **Debian 12 (bookworm) i386** is supported until about mid-2028.
- **Home Assistant OS:** no 32-bit x86 support.
- **Node.js:** no official 32-bit x86 Linux builds for current versions.
- **Python:** fine, so Python tools like SoCo work.

## Cheap upgrades (in order of value)
1. **SSD** (2.5" SATA): the biggest speed boost. The HDD is the main bottleneck.
2. **2 x 1 GB DDR2-667 SO-DIMM:** maxes out the RAM at 2 GB.
3. **Core 2 Duo swap** (T7200/T7400/T7600, socket M, cheap used): makes it **64-bit**, so modern distros, Docker and Home Assistant run. Boot the OS in legacy BIOS mode to work around the 32-bit EFI. A known firmware hack also lifts the RAM limit to about 3 GB usable with 4 GB installed.

Opening it: a putty knife around the bottom edge, then unclip. Be gentle with the Wi-Fi antenna wires.

## Planned role: Sonos controller hub
See [projects/sonos-controller](../../projects/sonos-controller/).
