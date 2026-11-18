# Stereo equipment

## Best plan: Add wireless streaming with the ESP32
- **ESP32 plus an I2S DAC board (e.g. PCM5102A)** into the amp's AUX/line input.
- Firmware: **squeezelite-esp32** supports AirPlay, Spotify Connect and Bluetooth A2DP. Alternatively, write a minimal Bluetooth A2DP sink in Arduino.
- This needs the original ESP32. S2/S3/C3 chips lack Bluetooth Classic, so they can't do A2DP.

## Other options
- Add a remote, auto power-on or input switching by having the ESP32 or Uno control relays or IR.
- Turn a receiver's display or VU meters into a network status display.

## Open questions
- [ ] Brands and models of each piece? (Receiver, amp, tape deck, CD player?)
- [ ] Do they all work?
- [ ] Which ESP32 variant is on your board? (The chip marking says ESP32, ESP32-S3, etc.)
