# Sonos Controller

Local control of Sonos speakers from repurposed hardware.

## How Sonos local control works
Every Sonos speaker exposes a local UPnP/SOAP API on port 1400 (works on S1 and S2). No cloud or account is needed for basic control: play/pause, volume, grouping, favorites and now-playing info.
- **SoCo** (Python) is a mature library and runs fine on 32-bit.
- An **ESP32 can talk to Sonos directly** over UPnP, with no hub needed.

## Proposed architecture
```
 Physical controls (ESP32: volume knob, buttons) --HTTP--+
 Old iPad / Nook (now-playing display)   ---HTTP---------+--> Mac mini hub (Debian 12 i386, Python + SoCo)
 Phone browser (web UI)                  ---HTTP---------+          |
                                                                    +--UPnP--> Sonos speakers
```
The hub gives one place for logic (scenes, schedules, which room a knob controls) and serves a web UI and display image. Simple controllers could skip it and talk to Sonos directly.

## Open questions
- [ ] What should the controller be: a physical knob box, a touchscreen, a wall dashboard, or all of these?
- [ ] How many Sonos speakers and rooms? S1 or S2 app?
