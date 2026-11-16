# HID OMNIKEY 5427 G2 — Security Research

IT&C 567 end-of-semester project: a security look at a BYU-issued **HID OMNIKEY 5427 G2**
desktop RFID / smart card reader (USB + Bluetooth LE, iCLASS Elite keys).
Everything here was gathered read-only. Nothing on the reader has been reconfigured
except switching it from keyboard wedge to CCID mode, which is logged and reversible.

## Device at a glance

| | |
|---|---|
| **Model** | HID OMNIKEY 5427 G2 (USB name "5427 CK"), Rev B, made in Philippines |
| **Part number** | R54270111-UNI-ELITE (multi-technology, HID iCLASS Elite keys) |
| **FCC ID** | JQ6-OK5427G2 |
| **USB serial / Unique ID** | 010100533056533934055B4634254630 |
| **EEM MAC** | 10:00:00:0F:C1:01 |
| **BLE chip UUID / address** | 0000000000001000800000177a000002 / aff70cee365d |
| **USB IDs** | VID `076B`, PID `5428` (keyboard wedge) / `5427` (CCID) |
| **USB interfaces** | HID keyboard or CCID smart card reader + **CDC EEM** (USB network adapter) |
| **Firmware** | 01.05.0203 (build 211, 2024-09-20) · SIO/SAM 01.A6 · BLE 06.07 · HW 00 |
| **OS / stack** | FreeRTOS 10.4.3, uIP / lwIP TCP/IP; Atmel AT91 libraries (likely AT91 ARM MCU) |
| **Card tech (13.56 MHz)** | Seos, iCLASS, MIFARE Classic/Plus/DESFire/Ultralight, FeliCa, ISO 14443 A/B, ISO 15693, NFC |
| **Card tech (125 kHz)** | HID Prox, AWID, Indala, EM4x |
| **Bluetooth LE** | HID Mobile Access; Tap In on (-40 dBm), Twist and Go off, Tx -4 dBm |
| **Enabled on this unit** | ISO 14443 A (Seos), Prox, BLE, **Config cards** — 14443 B, FeliCa, iCLASS 14443 B / 15693, ISO 15693 off |
| **Keyboard wedge output** | Only Seos enabled: PACS as HEX + `[ENTER]` |
| **Management** | Web console at `http://192.168.63.99` over USB EEM, TFTP, SNMP, config cards, OMNIKEY Workbench |

Full details, with a confidence marker on every value: **[DEVICE-INFO.txt](DEVICE-INFO.txt)**.

## Key findings so far

1. **Web console has no password.** It's reachable over plain HTTP on the USB network
   interface, and anything that can reach it can read and change the reader's config.
2. **TFTP is enabled.** It's a firmware/config transfer channel.
3. **Configuration cards are enabled.** A config card could reprogram the reader.
4. **125 kHz Prox is enabled.** Prox has no cryptography and is easy to clone.
5. **iCLASS High Security Mode is off**, and **keyboard wedge encryption is off**.
6. **OMNIKEY Workbench runs a local API (`localhost:5000`) with no authentication.**

Mitigations are in [DEVICE-INFO.txt](DEVICE-INFO.txt) section 11.

## What's in this repo

| Path | Contents |
|---|---|
| [`DEVICE-INFO.txt`](DEVICE-INFO.txt) | Complete device write-up: label, USB, firmware, web console, specs, security notes, timeline, open questions, hardening |
| [`BACKLOG.md`](BACKLOG.md) | Next steps (card tap + log capture first) |
| [`omnikey-5427g2-backup/`](omnikey-5427g2-backup/) | Baseline record of the reader's original state and how to restore it |
| [`omnikey-5427g2-backup/web-config/SETTINGS.md`](omnikey-5427g2-backup/web-config/SETTINGS.md) | Summary of every web console setting |
| [`omnikey-5427g2-backup/web-config/full-capture/CONSOLE-PAGES.txt`](omnikey-5427g2-backup/web-config/full-capture/CONSOLE-PAGES.txt) | Every console page as text (all 21 pages + keyboard wedge for all 18 card types) |
| [`omnikey-5427g2-backup/web-config/full-capture/`](omnikey-5427g2-backup/web-config/full-capture/) | Raw reader responses for every setting, plus field values per page (JSON) |
| [`tools/console-capture/`](tools/console-capture/) | Read-only headless-Chrome script used to capture the console |

## Ground rules

- BYU-owned device: **no firmware updates, no factory reset / Restore Default, no key extraction.**
  The iCLASS Elite keys can't be restored if lost.
- Use only our own or test credentials, and redact card numbers in anything published.
- Back up the current value before every settings change, and record each change in
  [`omnikey-5427g2-backup/README.md`](omnikey-5427g2-backup/README.md).
