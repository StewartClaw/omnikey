"""Read-only full capture of the OMNIKEY 5x27 web console.
- Only clicks tab labels and the KW 'Card Type' view selector. Never Apply/Save/Upload.
- Blocks upload/firmware/config-export URLs.
- Records every POST request body and the reader's response (raw MIB reads).
usage: python -I final.py <outdir> <scratchdir>
"""
import json, sys, os, re
from playwright.sync_api import sync_playwright

OUT, S = sys.argv[1], sys.argv[2]
os.makedirs(OUT + "/screens", exist_ok=True)
os.makedirs(OUT + "/screens/kw-by-card-type", exist_ok=True)
FIND = open(S + "/find.js").read()
DUMP = open(S + "/dump.js").read()
PAGES = [] if os.environ.get("KW_ONLY") else json.load(open(S + "/steps-full.json"))
CARD_TYPES = ["Seos", "BLE", "FSK Prox (e.g. HID Prox, AWID)", "PSK Prox (e.g. Indala)",
    "ASK Prox (e.g. EM4450, Acura)", "HID iCLASS", "MIFARE Classic", "MIFARE Ultralight",
    "MIFARE Desfire", "MIFARE Desfire EV1", "MIFARE Desfire EV2", "MIFARE Plus", "FeliCa",
    "PIV", "CEPAS", "Generic ISO14443A", "Generic ISO14443B", "Generic ISO15693"]
CARD_TYPES = json.loads(os.environ["TYPES"]) if os.environ.get("TYPES") else CARD_TYPES
KW_SUB = [("card-data", "Card Data Selection"), ("input", "Input Data Manipulation"),
          ("out1", "Out 1 Data Manipulation"), ("out2", "Out 2 Data Manipulation")]

reqlog, blocked = [], []
def guard(route, req):
    if any(k in req.url for k in ("poster.txt", "signed.fw", "toSign.fw", "ok5x27_ck.cfg")):
        blocked.append(req.url); return route.abort()
    route.continue_()
def on_resp(resp):
    r = resp.request
    if r.method == "POST":
        try: body = resp.text()
        except Exception as e: body = f"<err {e}>"
        reqlog.append({"url": r.url.replace("http://192.168.63.99", ""), "request": r.post_data, "response": body})

def slug(s): return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")

with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", headless=True)
    pg = b.new_page(viewport={"width": 960, "height": 680})
    pg.route("**/*", guard); pg.on("response", on_resp)
    pg.goto("http://192.168.63.99/"); pg.wait_for_timeout(9000)
    def click(label):
        pos = pg.evaluate(FIND, label)
        if not pos: raise SystemExit("label not found: " + label)
        pg.mouse.click(pos[0], pos[1]); pg.wait_for_timeout(2000)
    values = {}
    for name, labels in PAGES:
        for l in labels: click(l)
        pg.screenshot(path=f"{OUT}/screens/{name}.jpg", type="jpeg", quality=88)
        values[name] = pg.evaluate(DUMP)
        print("page", name)
    click("Keyboard Wedge")
    for ct in CARD_TYPES:
        click("Card Data Selection")
        pg.mouse.click(260, 216); pg.wait_for_timeout(1200)         # open Card Type list
        opt = pg.evaluate("""(t) => { for (const e of document.querySelectorAll('body *')) {
            let r = e.getBoundingClientRect();
            if (r.y > 225 && r.width > 0 && e.children.length === 0 && (e.innerText||'').trim() === t && r.x < 200) {
              e.scrollIntoView({block: 'nearest'}); r = e.getBoundingClientRect();
              const x = r.x + r.width/2, y = r.y + r.height/2, hit = document.elementFromPoint(x, y);
              // only click if the option itself is what's under the pointer
              return (hit === e || e.contains(hit) || (hit && hit.contains(e) && (hit.innerText||'').trim() === t)) ? [x, y] : null;
            } } return null; }""", ct)
        if not opt:
            print("SKIPPED (not safely clickable):", ct); pg.keyboard.press("Escape"); pg.wait_for_timeout(800); continue
        pg.mouse.click(opt[0], opt[1]); pg.wait_for_timeout(2500)
        for sub, label in KW_SUB:
            click(label)
            pg.screenshot(path=f"{OUT}/screens/kw-by-card-type/{slug(ct)}-{sub}.jpg", type="jpeg", quality=88)
            values[f"kw/{ct}/{sub}"] = pg.evaluate(DUMP)
        print("card type", ct)
    b.close()

json.dump(values, open(OUT + "/page-values.json", "w"), indent=1)
json.dump(reqlog, open(OUT + "/raw-mib-reads.json", "w"), indent=1)
print("blocked:", blocked, "| posts:", len(reqlog))
