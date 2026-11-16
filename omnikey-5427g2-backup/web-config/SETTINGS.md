# Reader web console - configuration backup

Captured 2026-11-16 ~2:34 PM from the reader's built-in management console at
http://192.168.63.99/ (reached over the USB CDC EEM network interface, driver 3.15).
Read-only capture. Nothing on the reader was changed.

## Restore point
- `ok5x27_ck.cfg` - the console's own "Export Config" output (encrypted, 2537 bytes).
  To restore: open the console > System Config > "Upload Config", choose this file,
  then "Apply Changes". This is the primary way to put the reader back to the BYU baseline.
- `full-capture/CONSOLE-PAGES.txt` is the human-readable fallback (every page as text).
  Screenshots are kept locally in `screenshots/` and are not committed.
- `index.html`, `webserver.js` - the console's front-end files.

## Reader info (General Overview)
- Firmware 01.05.0203 | MAC 10:00:00:0F:C1:01 | Unique ID 010100533056533934055B4634254630
- CCID slots: 1

## Host Interfaces
- IP 192.168.63.99 / mask 255.255.255.0 / gateway 192.168.63.1 (link to the host PC only)
- Host name: ok5x27_ck | EEM Enable: ON | TFTP Enable: ON
- Keyboard Wedge USB Endpoint: Endpoint 3

## Contactless Config > Polling (enabled card technologies)
- ENABLED:  ISO 14443 Type A, Prox, BLE, Config cards
- DISABLED: ISO 14443 Type B, FeliCa, iCLASS 14443 Type B, iCLASS 15693, ISO 15693
  (corrected 2026-11-16 from the screenshot: iCLASS 14443 Type B is unchecked)
- Polling: Frequency 1, Delay 0, Removal Delay 5, Removal Persist 2,
  RF Field Off Delay 5, RF Field On Delay 20, EMD Enable OFF, EMD Frame Length 3,
  Enhanced Polling OFF
- Tech order: see the full list under "Full capture" below.

## Keyboard Wedge > General Config
- Keyboard Wedge Enable: OFF (reader is currently in CCID mode)
- Output Type: Keyboard Wedge | Boot Interface: OFF
- Keyboard Layout: US | Hex Output Case: Upper | Inter-Keystroke Delay: 20
- Host OS: Windows | Custom CSN Resolution: Bytes | Multi PACS length: OFF
- Keyboard Wedge Encryption: OFF (no encryption key set)
- Card Out Event Keystrokes: blank | Error Keystrokes: blank
- Allow prestrokes/poststrokes for errors: OFF | Tech order after error: ON

## System Config
- Access Password: NOT SET (console shows "Please set Access Password...")
- Password timeout: 10 mins | Signing Key / Verification Key: blank
- Buttons on this page: Update Firmware, Upload Config, Encrypt Firmware,
  Load Key Layout, Update BLE Firmware, Export Config, Apply Changes,
  Restore Default, Reboot System. Do NOT press Restore Default.

## Full capture (2026-11-16 ~3:30 PM) - `full-capture/`
Every console page was captured read-only with a scripted headless Chrome
(`tools/console-capture/final.py`). The script only clicked tab labels and the
keyboard wedge "Card Type" view selector, and blocked the upload/firmware URLs.
Every request it sent was checked afterward: 705 MIB items, all reads
(`0d <oid> 05 00`), plus `ff680b` read commands. Nothing was written.

| File | What it is |
|---|---|
| `raw-mib-reads.json` | **Best data record.** Every read request the console sent and the reader's raw response, i.e. every setting value, including fields hidden by scrolling. |
| `CONSOLE-PAGES.txt` | **Readable version:** every page row by row; `[x]`/`[ ]` = checkbox, `[value]` = field. Includes the keyboard wedge pages for all 18 card types. |
| `page-values.json` | Same data as JSON with screen positions (93 views), including checkbox states. |

The `.cfg` export is still the restore point. These files are the readable record.

### Values that were missing before
- **Reader Information:** main firmware 01.05.0203, build `rev 20240920T124303-a0cf96db74e1+`,
  build 211, built 2024-09-20 10:48:25; SIO firmware 01.a6; BLE firmware 06.07;
  board type OMNIKEY 5427 Gen2; HW 00; Mod number 0; host interface USB;
  1 antenna; Enabled Features: None.
- **General Overview:** Contactless Card ATR blank (no card present).
- **Full Tech Order:** Seos, FSK Prox, Generic ISO14443A, HID iCLASS, BLE,
  MIFARE Classic, MIFARE Ultralight, MIFARE Desfire, Desfire EV1, Desfire EV2,
  MIFARE Plus, FeliCa, PIV, CEPAS, PSK Prox, ASK Prox, Generic ISO14443B,
  Generic ISO15693.
- **Keyboard wedge per card type:** only **Seos** has "Enable" ticked. The other
  17 types (BLE, FSK/PSK/ASK Prox, HID iCLASS, all MIFARE, FeliCa, PIV, CEPAS,
  Generic 14443A/B/15693) are not enabled for wedge output.
  Seos Out 2: PACS prestroke `[LED_BUZZ]`, poststroke `[ENTER]`; all string formats HEX.
  BLE has PACS Custom 1 preset to offset 14 / length 20 bits (not enabled).
- **Antennas:** 1 antenna, appearance Combined, selection Automatic, active Antenna 0, enabled, 1 card slot.
- **LEDs & Buzzer:** legacy KW LED/buzzer OFF, manual control OFF; Keyboard Wedge
  sequence: step 1 LED2+buzzer 100 ms, step 2 50 ms, step 3 LED1 50 ms; repeat 0.
- **ISO14443A:** enabled, anti-collision ON, max Tx/Rx 106k; FDT 1180, REQA 2712,
  anticollision 2712, halt 13560, FWT 65536 (13.56 MHz cycles).
- **ISO14443B:** disabled; TR2 1790, REQB 10848, max Tx/Rx 424k.
- **ISO15693:** disabled; T2 4192, wait time 12204.
- **FeliCa:** disabled; timeout 42036, max 212k.
- **iCLASS:** 14443 B OFF, 15693 OFF, No Range Check ON (greyed), **High Security Mode OFF**;
  Tchip 543 / 2116, Tout 6780 / 12204, ACTALL 27120, Tprog 108480.
- **Prox:** enabled, ATR mode PROX_STANDARD, custom Prox format all 0.
- **BLE:** enabled; chip UUID `0000000000001000800000177a000002`; static random
  address `aff70cee365d`; brand HID Global; Tap In ON, Twist and Go OFF;
  Tap In range -40 dBm, Twist and Go range -74 dBm, Tx power -4 dBm.
- **System Consoles:** Debug Console, empty (nothing typed; typing there sends commands).
- **About:** FreeRTOS V10.4.3 LTS Patch 2, uIP TCP/IP stack, Atmel AT91 libraries, lwIP AutoIP.
- Antenna register values for 14443A/B, 15693 and FeliCa are in `CONSOLE-PAGES.txt`.

## Security observations (for the report, not acted on)
- The management console is reachable with NO password. Anyone who can reach the
  EEM interface can read and change the reader's config.
- "Config cards" is enabled: a configuration card could reprogram the reader.
- TFTP is enabled: a firmware/config transfer channel is open.
- These are default-ish settings; hardening would set an access password,
  disable Config cards and TFTP if unused, and turn off the EEM console when not needed.
