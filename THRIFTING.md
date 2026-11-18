# Thrift Store Field Guide

What to grab, what to skip, and how to check a device in the store. Prices and support change, so look up the model on your phone before buying.

## Bring with you
- A phone with these sites bookmarked (see "Look it up"):
  - OpenWrt Table of Hardware
  - MrChromebox supported devices
  - postmarketOS wiki
  - LineageOS devices
- A USB power bank and a few cables (USB-C, micro-USB, Lightning, Mini-USB)
- Optional: a small multimeter, for checking whether a power adapter outputs anything

## Top targets

### Easy wins
| Find | What it becomes | Check before buying |
|---|---|---|
| **Thin clients** (HP t620/t630/t640, Dell Wyse 5070, Fujitsu Futro) | Low-power x86 home server, OPNsense/pfSense router, Home Assistant box | Has a power brick; RAM and SSD are usually upgradeable |
| **Chromebooks** | Full Linux laptop with MrChromebox UEFI firmware | Model is on the MrChromebox list; needs the charger |
| **Wi-Fi routers** | OpenWrt: VPN gateway, network-wide ad blocker, mesh node, Wi-Fi extender | Model **and hardware version** are supported; at least 16 MB flash / 128 MB RAM |
| **Kindles** (Kindle 4, Touch, Paperwhite 1–3) and **Nook Simple Touch** | E-ink dashboards, hackable readers | Whether a jailbreak exists for its firmware version (check MobileRead) |
| **Nintendo Wii / DS / PSP** | Homebrew and emulators. The Wii is very easy to softmod. | Powers on; has the cables |
| **Older smart plugs and bulbs** | Local control with Tasmota or ESPHome, no cloud | Many older ones use ESP8266 chips; newer ones may use Beken or Realtek chips (try OpenBeken) |

### Parts donors
| Find | What to salvage |
|---|---|
| **Inkjet printers and flatbed scanners** | Stepper and DC motors, linear rails, belts, optical endstops, power supplies |
| **DVD/Blu-ray drives** | Small steppers and lead screws for mini CNC/plotter builds. The laser diodes are an eye-safety hazard. |
| **Old receivers and VCRs** | VFD displays (they need a high-voltage driver), knobs, rotary encoders |
| **Laptops** (any condition) | LCD panels (often eDP or LVDS, usable with a cheap driver board), 18650 cells from older battery packs (only if healthy) |
| **Speakers and subwoofers** | Drivers for DIY Bluetooth or Wi-Fi speakers driven by the ESP32 |

### Audio (pairs with the ESP32 streamer)
- **Vintage receivers and integrated amps:** add AirPlay or Spotify Connect with an ESP32 and a DAC. Test every input and both channels.
- **Powered speakers with AUX in:** the easiest streaming target.

## Skip or be careful
- **iCloud-locked iPhones and iPads:** Activation Lock makes them close to useless. Check that it boots to the home screen or a setup screen that isn't locked.
- **Android with FRP lock, or carrier-locked bootloaders** (e.g. Verizon, many US Samsungs): custom ROMs may be impossible. Pixels and Nexus devices are the safest bets.
- **Swollen batteries:** a bulging case or a lifted screen means fire risk. Don't buy, or remove the battery very carefully.
- **CRT TVs and monitors, microwaves:** lethal stored voltage. Skip unless you know high-voltage safety.
- **Devices with proprietary, missing chargers:** check that a replacement is cheap first.
- **Anything with a locked, signed bootloader and no community** (fish finders, most smart TVs, car head units): parts value only.

## Look it up
1. Find the model number on the label underneath or behind the battery. For routers, note the hardware version too (e.g. "v2").
2. Search `<model> OpenWrt`, `<model> postmarketOS`, `<model> jailbreak`, or `<model> custom firmware`.
3. Healthy forum or wiki activity means a good buy. If nothing comes up, treat it as a parts donor.
