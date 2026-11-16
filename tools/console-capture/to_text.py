"""Turn page-values.json (from final.py) into a readable text file.
Each page is printed row by row in screen order:
  [value]  = text/number field     [x] / [ ] = checkbox on / off
usage: python -I to_text.py page-values.json CONSOLE-PAGES.txt
"""
import json, sys

V = json.load(open(sys.argv[1], encoding="utf-8"))
SKIP = {"▲", "▼", "© HID Global Corporation 2011-2022"}
out = ["OMNIKEY 5427 G2 - web console, every page as text",
       "Captured 2026-11-16 read-only from http://192.168.63.99 (see SETTINGS.md).",
       "[value] = field value, [x] = checkbox ticked, [ ] = not ticked.",
       "Keyboard wedge pages are repeated for each of the 18 card types.", ""]

for page, items in V.items():
    items = [i for i in items if i[2][1] >= 190 and not (i[0] == "text" and i[1] in SKIP)]
    rows = []
    for kind, val, (x, y) in sorted(items, key=lambda i: (i[2][1], i[2][0])):
        if rows and abs(rows[-1][0] - y) <= 10: rows[-1][1].append((x, kind, val))
        else: rows.append([y, [(x, kind, val)]])
    out += ["=" * 70, page.replace("kw/", "Keyboard wedge / ").replace("/", " / "), "=" * 70]
    for _, cells in rows:
        parts = []
        for _, kind, val in sorted(cells):
            if kind == "check": parts.append("[x]" if val else "[ ]")
            elif kind == "text": parts.append(str(val))
            else: parts.append(f"[{val}]")
        out.append("  " + "  ".join(parts))
    out.append("")

open(sys.argv[2], "w", encoding="utf-8").write("\n".join(out))
print(len(V), "pages,", len(out), "lines")
