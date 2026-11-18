# Mac mini

## Identify it first
Model number is on the bottom.
- **A1103: Mac mini G4 (2005).** PowerPC G4, at most 1 GB RAM, IDE drive. Two USB ports on the back.
- **A1176: Mac mini Intel (2006/2007).** Core Solo/Duo or Core 2 Duo. Four USB ports on the back.

## Options
### If it's a G4
- **Retro Mac (best fit):** Mac OS X 10.4/10.5 for classic Mac software and games. A patched Mac OS 9.2.2 can also boot on it.
- **Light Linux/BSD box:** current OSes that still support 32-bit PowerPC include OpenBSD/macppc, NetBSD, Void PPC, Adélie and Debian ports. It's slow and RAM-limited, but fine as a headless server.
- **Cheap upgrades:** max out the RAM at 1 GB and swap the drive for an IDE-to-SD or mSATA adapter.

### If it's Intel
- **Linux home server:** Home Assistant, file server, or a backend for the dashboards in this repo.
- Core Solo/Duo chips are 32-bit only. Swapping in a socketed Core 2 Duo (e.g. T7200) makes it 64-bit.

## Open questions
- [ ] Model number (A1103 or A1176)?
- [ ] Does it power on? How much RAM, and what drive?
