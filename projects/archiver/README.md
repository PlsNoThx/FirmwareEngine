# The Archiver

Turns the Mac mini into a station that preserves records and VHS tapes as digital files, and serves them to the house (and Sonos) over the network.

```
 VINYL   Sony turntable --phono--> NAD 7220PE --TAPE OUT--> Mac mini line-in
                                                              | record-side.sh
                                                              | split_side.py
                                                              v
                                              ~/archive/music/Artist/Album/01 - Song.flac
 VHS     tape --> Sony RDR-VX combo --dub--> DVD-R --> Mac mini DVD drive
                                                              | rip-dvd.sh
                                                              v
                                              ~/archive/video/Christmas 1994.mkv
 SHARE   ~/archive  --Samba-->  computers on the network;  ~/archive/music --> Sonos library
```

## What you need
- The Mac mini (A1176), with Ethernet if possible
- **RCA (2 plugs) to 3.5 mm stereo cable** to go from the NAD's TAPE OUT to the Mac mini's audio input
- A blank CD-R, to install Linux
- **Blank DVD-R discs** for the VHS dubs
- An **external USB hard drive**, strongly recommended (see [Storage](#storage))

| Script | Runs on | What it does |
|---|---|---|
| `setup.sh` | Mac mini, once | Installs sox, flac, ffmpeg, ALSA tools; optional Samba |
| `vinyl/levels.sh` | Mac mini | Live input meter for setting the recording level |
| `vinyl/record-side.sh` | Mac mini | Records one side to 24-bit / 48 kHz WAV |
| `vinyl/split_side.py` | Mac mini | Finds the gaps, splits into tagged FLAC tracks, saves a master |
| `video/rip-dvd.sh` | Mac mini | Copies a finalized DVD to MKV losslessly (optional H.264 copy) |

---

## Step 1: Install Debian 12 on the Mac mini

This erases the Mac mini's drive. Copy off anything you want to keep first.

1. On another computer, download the **Debian 12 i386 netinst** ISO from debian.org: the file named `debian-12.x.x-i386-netinst.iso`. It has to be **i386**, not amd64, because this Core Duo is 32-bit. Burn it to a CD-R.
   - Burning a CD is the most reliable way to boot this model. Its firmware is picky about USB sticks.
2. Plug in Ethernet, keyboard and monitor. Insert the CD, power on, and **hold `C`** until the installer appears.
3. Install mostly with defaults:
   - Hostname: `archiver`
   - Partitioning: **Guided, use entire disk**
   - Software selection: untick the desktop and tick **SSH server** and **standard system utilities**. (Pick Xfce instead if you want to use Audacity on the mini itself.)
4. Reboot and remove the CD. If it shows a flashing folder, hold **Option** at power-on and pick the disk labelled **"Windows"**, which is how Mac firmware names a BIOS-boot disk.
5. From now on you can work from your main computer: `ssh youruser@archiver.local` (or use the IP shown by `hostname -I`).

## Step 2: Install the archiver tools

On the Mac mini:

```bash
sudo apt install -y git avahi-daemon
```

```bash
git clone -b claude/laughing-lovelace-ujz6bj https://github.com/PlsNoThx/FirmwareEngine.git ~/firmwareengine && cd ~/firmwareengine/projects/archiver
```

If the repo is private, git asks for your GitHub username and a **personal access token** (not your password). Alternatively, copy the `archiver` folder over from another computer with `scp -r`.

```bash
sudo ./setup.sh --samba
```

Then set the input. Run `alsamixer`, press **F4** for capture controls, select the **Line** input as the capture source, and unmute it with the space bar.

## Step 3: Wire the turntable

1. Turntable to **NAD PHONO** in. If the turntable has a PHONO/LINE switch on the back, set it to **PHONO**, since the NAD does the phono amplification. Connect its ground wire to the NAD's GND screw if it has one.
2. **NAD TAPE OUT** (the "REC" RCA jacks) to the Mac mini's **audio input** jack, the one next to the headphone jack.
   - TAPE OUT isn't affected by the volume or tone knobs, so the recording is flat and consistent whatever you do with the speakers.
3. Press **PHONO** on the NAD. You can still listen through the speakers while it records.
4. If you hear a hum in the recording, try a **ground loop isolator** (cheap, 3.5 mm) between the cable and the Mac mini.

## Step 4: Set the level (once)

```bash
cd ~/firmwareengine/projects/archiver/vinyl
```

```bash
./levels.sh
```

Play the **loudest** part of a loud record. In a second SSH window, run `alsamixer` and adjust the capture gain until peaks hit about **70-80% and never 100%**. Clipping can't be fixed later; a slightly quiet recording can.

## Step 5: Record a record

Before recording, clean the record and the stylus; it matters more than any software.

**1. Record side A.** Start the script, then drop the needle. Press Ctrl+C once the side ends.

```bash
./record-side.sh ~/archive/raw/rumours side-A
```

**2. Preview the split.** Tell it how many songs are on the side; this is the most reliable mode.

```bash
./split_side.py ~/archive/raw/rumours/side-A.wav --tracks 6 --dry-run
```

It prints where each track starts and ends. If those look right, run it for real with tags:

```bash
./split_side.py ~/archive/raw/rumours/side-A.wav --artist "Fleetwood Mac" --album "Rumours" --year 1977 --tracks 6
```

**3. Repeat for side B**, continuing the numbering:

```bash
./split_side.py ~/archive/raw/rumours/side-B.wav --artist "Fleetwood Mac" --album "Rumours" --year 1977 --tracks 5 --start-number 7
```

**Splitter options:**
- `--titles songs.txt`: a text file with one title per line. It names the files and tags, and sets the track count.
- `--splits 3:21,7:45,11:02`: your own split times, if it guesses wrong (e.g. a song with a long silent pause).
- No `--tracks`: auto mode. It splits at every quiet gap of 1 second or more. Good for most pop/rock, worse for quiet classical or live albums.

**Output:**
- Tracks: `~/archive/music/<Artist>/<Album>/01 - Title.flac` (24-bit/48 kHz FLAC, tagged)
- Whole-side masters: `~/archive/masters/<Artist> - <Album>/side-A.flac`, kept separately so Sonos doesn't list them
- Once you're happy with the tracks, delete the raw WAVs in `~/archive/raw` to save space.

Optional: to remove clicks and pops, open a track in **Audacity** and use **Effect > Noise Removal and Repair > Click Removal**. Always keep the master untouched.

## Step 6: VHS tapes

**On the Sony RDR-VX combo:**
1. Insert the tape and a blank **DVD-R**.
2. Use the **VHS-to-DVD dub** function. Choose the **highest quality mode** that fits the tape (e.g. 1-hour or 2-hour mode); VHS gains nothing from longer modes.
3. **Finalize** the disc when done, from the disc settings menu. An unfinalized disc won't read in a computer. Exact menu names are in the manual for your model.

**On the Mac mini:** insert the DVD in the slot and run:

```bash
cd ~/firmwareengine/projects/archiver/video
```

```bash
./rip-dvd.sh "Christmas 1994"
```

This copies the video **bit-for-bit** into `~/archive/video/Christmas 1994.mkv`. It's fast and loses no quality. Discs with several title sets produce `... - 01.mkv`, `... - 02.mkv`.

To also make a smaller, deinterlaced copy that plays on phones and smart TVs:

```bash
./rip-dvd.sh "Christmas 1994" /dev/sr0 --encode
```

The encode is slow on this CPU (roughly real time), so leave it running overnight for long tapes.

**Notes:**
- Both normal DVD-Video discs and DVD-RW discs recorded in **VR mode** are handled.
- You can reuse a DVD+RW/DVD-RW for each tape once it's ripped, but DVD-R is the most reliable to read.

## Storage

Rough sizes:

| Item | Size |
|---|---|
| One LP, as tracks + master (24/48 FLAC) | about 0.8-1 GB |
| One DVD (up to 2 hours of VHS) | about 4.5 GB |

The internal 80 GB drive fills up fast, so use an external USB drive mounted at `~/archive`.

1. Find the drive with `lsblk`; it'll be something like `/dev/sdb`.
2. Format it. **This erases the drive**; double-check the name first:

```bash
sudo mkfs.ext4 -L archive /dev/sdX1
```

3. Make it mount at boot with this line in `/etc/fstab` (`nofail` lets the mini boot even if the drive is unplugged):

```
LABEL=archive  /home/youruser/archive  ext4  defaults,nofail  0  2
```

4. Mount it and take ownership:

```bash
mkdir -p ~/archive && sudo mount -a && sudo chown -R "$USER": ~/archive
```

## Sharing to the house and Sonos

Add these share blocks to the end of `/etc/samba/smb.conf` (replace `youruser`):

```ini
[archive]
   path = /home/youruser/archive
   valid users = youruser
   read only = no

[music]
   path = /home/youruser/archive/music
   valid users = youruser
   read only = yes
```

Then set a Samba password and restart:

```bash
sudo smbpasswd -a youruser && sudo systemctl restart smbd
```

- **Computers:** connect to `smb://archiver.local/archive` (Mac/Linux) or `\\archiver\archive` (Windows).
- **Sonos:** in the Sonos app, find **Music Library** settings, add a shared folder `\\<mac-mini-ip>\music` (get the IP with `hostname -I`), and enter the Samba username and password. Sonos plays FLAC up to 24-bit/48 kHz, which is why the recordings are made at 48 kHz.

## Tested
- `split_side.py`: tested on a synthetic side with surface-noise gaps of 2-3 s, a quiet passage inside one song, and lead-in/lead-out grooves. `--tracks`, auto and `--splits` modes all split at the right places, and output is tagged 24-bit FLAC.
- `rip-dvd.sh`: tested on synthetic discs: VIDEO_TS with two title sets and AC-3 audio (menus skipped, VOB parts joined), and a VR-mode disc with LPCM audio (converted to FLAC), including `--encode`.
- Not yet tested on the real Mac mini's line-in. The first real record is the real test, so report back what `levels.sh` shows.
