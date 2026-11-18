# Stereo equipment

## Inventory (from photo; confirm model numbers on the rear labels)
| Unit | Notes | Role |
|---|---|---|
| **NAD 7220PE** stereo receiver | Well regarded, "Power Envelope" amp. Phono, CD, tape monitor, video inputs | **Main amp** for the streaming setup |
| **Sony STR-D590** A/V receiver | Dolby Surround, phono input, many inputs | Second-room amp, or the synth's amp |
| **Sony PS-LX250H** turntable | Fully automatic, belt drive | Vinyl, and vinyl to Sonos (see below) |
| **Pioneer PD-M501** 6-disc CD changer | Magazine changer | Keep as a CD source |
| **Sony RDR-VX** VCR/DVD recorder combo | Records VHS directly to DVD | Digitize old VHS tapes |
| **Gakken Toy Record Maker** (Otona no Kagaku kit) | Cuts audio grooves into blank discs and plays them back | Cut synth recordings onto discs |

## Projects

### 1. Wi-Fi streaming into the NAD (ESP32)
- ESP32 + PCM5102A DAC into the NAD's **CD** or **Video** input.
- squeezelite-esp32 firmware gives AirPlay, Spotify Connect and Bluetooth (original ESP32 only for Bluetooth).

### 2. Vinyl to Sonos (Mac mini)
- Turntable -> receiver PHONO in -> receiver **TAPE OUT** -> Mac mini **audio line-in** (the 2006 mini has an analog/optical input jack).
- The Mac mini encodes the audio as a live stream (darkice + Icecast). Sonos plays it as a radio station URL, so every room can play the record.
- Expect a few seconds of delay, which is fine for listening around the house.

### 3. IR automation (ESP32 + IR LED)
- The ESP32 sends the receivers' remote codes: power on and switch input when streaming starts, and control volume.
- Sony uses the SIRC protocol, and NAD likely uses NEC. Both are supported by the IRremote / IRremoteESP8266 libraries. You can also capture the real remote's codes with a cheap IR receiver.
- Can be tied to the Sonos controller knob.

### 4. VHS -> DVD -> files
- The RDR-VX records tapes straight to DVD-R. Rip the DVDs on the Mac mini's drive (it reads DVDs) with HandBrake or ffmpeg.

### 5. Smart jukebox (ESP32 IR + Mac mini web page)
- The Pioneer changer and both receivers are IR-controlled. One web page (served by the Mac mini) or the ESP32 knob box can pick a disc and track, power on the NAD and switch its input.

### 6. Light-up VU meter
- Take audio from the NAD's **TAPE OUT**, sample it with the ESP32 (biased into an ADC pin), and drive an LED strip or small display as a spectrum or VU meter.

### 7. Digitize the record collection and VHS tapes
- **Built:** see [projects/archiver](../../projects/archiver/).

## Combined system: "Retro hi-fi with modern brains"
```
 Turntable --phono--> NAD 7220PE <--CD in-- ESP32 streamer (AirPlay/Spotify/BT)
 CD changer --CD/video-->   |  TAPE OUT --> Mac mini line-in --> Icecast stream --> Sonos rooms
                            |
                     speakers                ESP32 IR blaster <-- Mac mini web UI / knob box
 Sony STR-D590: second zone or synth amp
```

## Before anything else: health check
- [ ] Power on each unit; check the display and lamps.
- [ ] Test **every input and both channels** on both receivers with a phone or CD player.
- [ ] Scratchy volume knobs or cutting-out channels: spray contact cleaner (e.g. DeoxIT D5) into the pots, switches and input buttons and work them back and forth.
- [ ] Turntable: the belt is likely stretched after decades (replacements are cheap); inspect the stylus. Check the back for a PHONO/LINE switch.
- [ ] Never run a receiver with the speaker wires shorted or at high volume with nothing connected.
