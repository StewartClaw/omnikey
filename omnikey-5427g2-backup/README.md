# OMNIKEY 5427 G2 — baseline backup

Captured 2026-11-16, before any changes were made to the reader.

## Device identity (from the label and USB)
| Field | Value |
|---|---|
| Model | HID OMNIKEY 5427 G2 (USB name: "5427 CK"), Rev B |
| Part no. | R54270111-UNI-ELITE |
| USB VID / PID / bcdDevice | 076B / 5428 / 0100 |
| USB serial | 010100533056533934055B4634254630 |
| FCC ID | JQ6-OK5427G2 |
| Mode at capture | Keyboard wedge (HID keyboard on interface 0) |
| Interface 1 ("5427 CK", CDC EEM) | No driver (Code 28) at capture |
| Config tool | OMNIKEY Workbench Tool 2.7.0 |

Full Windows device details are in `pnp-snapshot.json` and `pnputil.txt`.

## Reader internals (Workbench API, read 2026-11-16 ~2:15 PM, in CCID mode)
| Field | Value |
|---|---|
| Workbench reader type | OK5427Gen2Ble ("HID OMNIKEY 5427 CK CL 0") |
| Firmware | 01.05.0203 |
| Hardware version | 00 |
| SAM (secure element) version | 01.A6 |
| SDR version | 00 |
| BLE version | 06.07 |
| Antennas | 1 |
| Workbench settings | `IsEemInterfaceEnabled: true`, `OperatingMode: 0` |

Raw responses: `workbench-readerDiagnostic.json`, `workbench-readerSettings.json`.

**Mode history:** the reader came in keyboard-wedge mode (USB PID 5428). On 2026-11-16
at 13:46 it was switched to CCID mode (PID 5427) through Workbench. To restore it,
switch it back to keyboard wedge in Workbench and confirm the PID is 5428 again.
**Drivers added:** HID OMNIKEY CCID Driver 2.3.4.121, OMNIKEY Workbench Tool 2.7.0,
USB CDC EEM driver 3.15 (gives access to the reader's web console at http://192.168.63.99).

## Web console backup (`web-config/`)
- `web-config/ok5x27_ck.cfg` - **restore point**: the console's Export Config file
  (encrypted). Restore with System Config > Upload Config > Apply Changes.
- `web-config/full-capture/` - readable record of **every** setting: raw reader
  responses for every value (`raw-mib-reads.json`), field values per page
  (`page-values.json`), and screenshots of all 21 pages plus the keyboard wedge
  pages for all 18 card types. Captured read-only (every request checked as a read).
- `web-config/SETTINGS.md` - summary of all values.
- Re-capture script: `tools/console-capture/final.py`.

## What can and can't be backed up
- **Settings:** Workbench can't export them, but the web console can
  (`ok5x27_ck.cfg` above). The reader also stores its own backup copy in flash,
  and has a factory-restore command (MIB "Restore" / console "Restore Default")
  that sets everything back to defaults. **Don't use it** (BYU Elite config).
- **Firmware:** You can't dump or back it up. A firmware update is the only
  change that could brick the reader, and it can't be rolled back. Leave it out
  of scope unless you plan to do it on purpose.

## To-do: finish the baseline (before changing anything)
- [x] Screenshot every configuration page -> done via the web console
      (`web-config/full-capture/screens/`), which covers more than Workbench.
- [x] Core firmware version: 01.05.0203 (build 211, 2024-09-20); SIO 01.a6; BLE 06.07.
- [x] Keyboard-wedge output format (from config): only Seos enabled; PACS as
      HEX (upper case), prestroke `[LED_BUZZ]`, poststroke `[ENTER]`; US layout,
      20 ms inter-keystroke delay. Byte order / bit length still to confirm with a card.
- [ ] Tap each test card in Notepad (in keyboard wedge mode) and paste the output below.

| Card | Technology (Workbench) | Wedge output |
|---|---|---|
| | | |

## Safe-use rules
1. Change one setting at a time. Screenshot the page before and after, then click Apply.
2. Don't unplug the reader during a firmware upload.
3. Recovery order: change the setting back by hand; if that fails, upload
   `web-config/ok5x27_ck.cfg` and Apply Changes; then compare against
   `web-config/full-capture/`. Factory restore is the very last resort.
