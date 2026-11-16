# Backlog - OMNIKEY 5427 G2 project

Next steps, roughly in priority order. Ground rules still apply: no firmware
update, no factory reset / Restore Default, test cards only, redact card
numbers, and record every settings change in `omnikey-5427g2-backup/README.md`
before making it. Details for each item are in `DEVICE-INFO.txt` (section 10).

## Now - card reads and logs
- [ ] **Tap a card and capture the logs (CCID mode, no settings change).**
  Capture all of these during the same tap:
  - Reader debug log: the console's System Consoles > Debug Console page
    streams from `GET /consoledata`. Just watch or record that stream; don't
    type anything into the console input.
  - Workbench: card ATR / UID / technology as Workbench reports it, plus
    `%APPDATA%\HID Global\OMNIKEY Workbench Tool\logs\Workbench-YYYYMMDD.log`.
  - Windows: Event Viewer > Applications and Services > Microsoft > Windows >
    SmartCard-* and the PnP log for the reader.
  - The General Overview page's "Contactless Card ATR" while a card is on the reader.
- [ ] Repeat for each test card type we have (Seos/BYU ID, Prox, MIFARE, phone
  with Apple Wallet / HID Mobile Access) and fill a table: card, technology,
  ATR, UID, what the debug log shows.
- [ ] **Keyboard wedge output test.** Switch to keyboard wedge in Workbench
  (log the change first), tap each card in Notepad, and fill the table in
  `omnikey-5427g2-backup/README.md`. Expect: Seos types HEX + Enter, others
  type nothing. Switch back to CCID and confirm PID 5427.

## Next - attack surface (read-only first)
- [ ] Port scan only the reader link (`192.168.63.99`): TCP and UDP, including
  SNMP (161) and TFTP (69).
- [ ] TFTP: can files be listed or read without auth? Read only, never upload.
- [ ] SNMP: does it answer `public` / default communities? Read (GET/WALK) only.
- [ ] Web console: confirm no auth on the `/ajax` and `/cjax` endpoints (we already
  know reads work with no password). Document it, but don't send writes.
- [ ] Workbench local API (`localhost:5000`): test whether a web page can send a
  cross-site POST (CSRF). Use a harmless request only.
- [ ] Decode the `/ajax` MIB format (`0d <len> <oid> 05 00` reads) into a
  readable list of setting names and values from `raw-mib-reads.json`.
- [ ] BLE: passive scan. What does the reader advertise (name, services)? Is it
  connectable or pairable?
- [ ] Configuration cards: read the HID docs on how config cards are
  authenticated. "Config cards" polling is ON.

## Research / documentation
- [ ] FCC ID JQ6-OK5427G2: get the internal photos and confirm the main MCU (AT91?),
  BLE chip (Nordic?) and SAM.
- [ ] Get the OMNIKEY 5x27 Software Developer Guide (escape commands, MIB layout, SNMP).
- [ ] Decode the SAM ATR (`O5WWgLH+VR/HR3JhY2UT`).
- [ ] Is the encrypted `ok5x27_ck.cfg` tied to this reader or loadable on any 5x27?
  (Research only, no second reader to test on.)
- [ ] Compare Prox (125 kHz, no crypto) vs iCLASS Elite vs Seos for the report.

## Report
- [ ] Scoping / rules of engagement doc (ground rules from DEVICE-INFO.txt).
- [ ] Findings write-up: no console password, TFTP on, config cards on, Prox on,
  wedge encryption off, iCLASS High Security Mode off, Workbench API has no auth.
- [ ] Mitigations section (DEVICE-INFO.txt section 11).
- [ ] Final check: reader is back in its original mode and config matches
  `omnikey-5427g2-backup/web-config/full-capture/`.
