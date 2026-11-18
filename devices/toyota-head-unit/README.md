# Toyota factory head unit (CD/MP3/WMA, AM-SAT, Disc-AUX)

From a **2006 4Runner Sport (non-JBL)**, so the **built-in amplifier is present**. Toyota part number on the top or side label: `86120-xxxxx` (TBD; needed for the exact pinout).

## Projects

### 1. Bench / garage stereo (easiest)
- Power from a **12 V, 5 A+ supply** (or an old PC power supply's 12 V rail).
- Wire: **B+ (constant 12 V) and ACC (switched 12 V)** both to +12 V, GND to ground, plus speaker outputs. Get the pinout for the exact part number and confirm it with a multimeter before applying power.
- Non-JBL unit, so the built-in 4-channel amp (roughly 4 x 15-20 W) drives speakers directly.
- **Speaker outputs are bridged (BTL).** Never connect any speaker negative (-) to ground, or to another speaker's negative. Each speaker gets its own +/- pair, or the amp chip can be damaged.
- Easiest connector option: buy a **factory-style Toyota radio harness pigtail** (vehicle-side plug for 2003+ Toyota) instead of soldering to the pins.
- Feed the **AUX** input with the ESP32 + PCM5102A for Bluetooth/AirPlay. The "Disc-AUX" button suggests an AUX input on the rear connector (it was wired to the dash jack).
- Some Toyota units have an owner-set anti-theft code. If it shows "SEC" or "ERROR", look up the reset for the part number.

### 2. Synth amp and enclosure
- Built-in 12 V 4-channel amp drives car or bookshelf speakers directly from the synth's DAC output via AUX.

### 3. Advanced: AVC-LAN emulation
- Toyota units talk to CD changers and other modules over the AVC-LAN bus. Arduino projects exist that emulate a CD changer to enable AUX or receive button presses. The Uno is a reasonable fit.

### 4. Parts donor
- Rotary encoder with push (TUNE-FILE knob), volume pot or encoder, tactile buttons, slot-load CD mechanism.
- The display is a custom segment LCD with a proprietary driver, so it's hard to reuse.

## Open questions
- [ ] Part number (86120-xxxxx) from the label
- [ ] What is the black unit stacked on top?
