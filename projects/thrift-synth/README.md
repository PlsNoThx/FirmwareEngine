# Thrift Synth

A custom synth built mostly from thrift-store parts.

## Architecture
```
 [Keys]  toy keyboard matrix / MIDI keyboard / game controller
    |
 [Controls]  salvaged pots, EQ sliders, encoders  -->  74HC4051 mux (if many)
    |
 [Brain]  ESP32 (synthesis)  +  PCM5102A I2S DAC
    |
 [Output]  salvaged powered speakers / boombox AUX / headphone jack
    |
 [Enclosure]  old radio, cassette deck, cigar box, keyboard shell
```
- **ESP32 + PCM5102A:** the main sound engine. It does oscillators, filters, envelopes, a sequencer, and optionally MIDI over Bluetooth LE.
- **Arduino Uno:** either a dedicated key and knob scanner that sends serial/MIDI to the ESP32, or a simple lo-fi synth on its own using the Mozzi library (PWM audio on pin 9).

## What to look for

### Keys and playing surfaces
| Find | Use | Notes |
|---|---|---|
| **Cheap Casio/Yamaha keyboards** | Gut it and scan its key matrix with the ESP32/Uno; the case becomes your enclosure | Count the ribbon-cable pins; the matrix is usually easy to trace with a multimeter |
| **Keyboards with MIDI OUT (5-pin DIN)** | Instant controller, no gutting | DIN MIDI in needs a 6N138 optocoupler circuit |
| **USB MIDI controllers** (M-Audio Keystation, Akai, etc.) | Controller | Needs USB host: ESP32-S3 has it, the original ESP32 doesn't |
| **Guitar Hero / Rock Band controllers** | Frets, strum bar and whammy as synth controls | Wii versions plug into a Wii remote and talk I2C, which is easy to read |
| **Wii Nunchuk** | Joystick plus accelerometer for pitch-bend and filter sweeps | I2C, 3.3 V, very easy with the ESP32 |
| **Laptop touchpads** | XY pad | Older ones speak PS/2, which Arduino libraries can read |
| **Old hard drives** | The spindle motor becomes a scratch or jog wheel: spinning it generates pulses | Platter makes a nice heavy wheel |

### Knobs, sliders and buttons
| Find | Use |
|---|---|
| **Graphic equalizers** (home or car audio) | A bank of 5–31 sliders, ideal for a step sequencer or additive/harmonic control |
| **Stereo receivers, mixers, guitar pedals** | Pots, switches, jacks and knob caps |
| **Car stereos, old receivers** | Rotary encoders for menus |
| **Arcade sticks / old game controllers** | Big buttons for drum pads or triggers |

Prefer **linear (B-taper) pots** for controls. Volume knobs are often audio (A-taper), which feels uneven. Anything from about 10k to 100k works.

### Sound sources to circuit-bend or sample
- **Talking toys, electronic toys, keychain sound effects:** classic circuit-bending fodder. Probe for glitchy shorts with a resistor and a pot rather than a bare wire.
- **Cassette players and Walkmans:** controlling the motor speed gives tape warble, pitch and wow effects. You can also make tape loops.
- **Speak & Spell, Casio SK-1, Casio VL-Tone:** legendary for bending, but now collectible. Grab one if it's cheap.

### Output and enclosure
- **Powered computer speakers:** a built-in amp, simplest output.
- **Boombox or portable radio:** amp, speaker and battery box in one, and a great enclosure.
- **Old radios, typewriter cases, cassette decks, cigar boxes:** for looks.

## Electrical gotchas
- The ESP32 runs at **3.3 V**. Power pots from 3.3 V, never 5 V.
- Use **ADC1 pins only** (GPIO 32–39) on the ESP32; ADC2 doesn't work while Wi-Fi is on. Its ADC is noisy, so smooth the readings in software.
- For more pots than pins, use a **74HC4051** 8-channel multiplexer (several can be chained).
- Don't connect toy circuits running at other voltages directly to the ESP32 without checking levels first.

## Shopping list (buy new, cheap)
- PCM5102A I2S DAC board, the same one as for the stereo streamer
- 74HC4051 multiplexers
- 6N138 optocoupler and a 5-pin DIN jack, if adding MIDI in
- 3.5 mm / 1/4" jacks, knob caps
