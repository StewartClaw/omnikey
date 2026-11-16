# Reader web console - configuration backup

Captured 2026-11-16 ~2:34 PM from the reader's built-in management console at
http://192.168.63.99/ (reached over the USB CDC EEM network interface, driver 3.15).
Read-only capture. Nothing on the reader was changed.

## Restore point
- `ok5x27_ck.cfg` - the console's own "Export Config" output (encrypted, 2537 bytes).
  To restore: open the console > System Config > "Upload Config", choose this file,
  then "Apply Changes". This is the primary way to put the reader back to the BYU baseline.
- Screenshots of each section are the human-readable fallback:
  `screenshot-kw-general.jpg`, `screenshot-contactless-polling.jpg`,
  `screenshot-host-interfaces.jpg`, `screenshot-system-config.jpg`.
- `index.html`, `webserver.js` - the console's front-end files.

## Reader info (General Overview)
- Firmware 01.05.0203 | MAC 10:00:00:0F:C1:01 | Unique ID 010100533056533934055B4634254630
- CCID slots: 1

## Host Interfaces
- IP 192.168.63.99 / mask 255.255.255.0 / gateway 192.168.63.1 (link to the host PC only)
- Host name: ok5x27_ck | EEM Enable: ON | TFTP Enable: ON
- Keyboard Wedge USB Endpoint: Endpoint 3

## Contactless Config > Polling (enabled card technologies)
- ENABLED:  ISO 14443 Type A, iCLASS 14443 Type B, Prox, BLE, Config cards
- DISABLED: ISO 14443 Type B, FeliCa, iCLASS 15693, ISO 15693
- Polling: Frequency 1, Delay 0, Removal Delay 5, Removal Persist 2,
  RF Field Off Delay 5, RF Field On Delay 20, EMD Enable OFF, EMD Frame Length 3,
  Enhanced Polling OFF
- Tech order: Seos, FSK Prox (HID Prox/AWID), Generic ISO14443A, HID iCLASS, BLE,
  MIFARE Classic, MIFARE Ultralight, MIFARE DESFire (/EV1/EV2), MIFARE Plus ...

## Keyboard Wedge > General Config
- Keyboard Wedge Enable: OFF (reader is currently in CCID mode)
- Output Type: Keyboard Wedge | Boot Interface: OFF
- Keyboard Layout: US | Hex Output Case: Upper | Inter-Keystroke Delay: 20
- Host OS: Windows | Custom CSN Resolution: Bytes | Multi PACS length: OFF
- Keyboard Wedge Encryption: OFF (no encryption key set)

## System Config
- Access Password: NOT SET (console shows "Please set Access Password...")
- Password timeout: 10 mins | Signing Key / Verification Key: blank

## Security observations (for the report, not acted on)
- The management console is reachable with NO password. Anyone who can reach the
  EEM interface can read and change the reader's config.
- "Config cards" is enabled: a configuration card could reprogram the reader.
- TFTP is enabled: a firmware/config transfer channel is open.
- These are default-ish settings; hardening would set an access password,
  disable Config cards and TFTP if unused, and turn off the EEM console when not needed.
