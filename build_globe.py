#!/usr/bin/env python3
"""
build_globe.py - St. Roch + Panikpakuttuk family map on MapLibre GL v5 (globe).

The 2D Leaflet build (source_2d.html) is the source of truth: its VOYAGE object
already carries the merged route legs AND the full `family` overlay (aboard 1944,
the 1944-1946 way home by ship / sled / Nascopie, side trips, ship-onward track).

This script:
  1. Loads voyage.json (extracted verbatim from the 2D build's VOYAGE object).
  2. Appends a short globe note to meta.note (idempotent).
  3. Injects it as __DATA__ into template_globe.html  ->  index.html.

To refresh after editing the 2D map, re-extract its VOYAGE object into voyage.json:
    python3 extract_voyage.py        (one-liner provided alongside)
then re-run this script.
"""
import json, pathlib

HERE = pathlib.Path(__file__).parent
voyage = json.load(open(HERE / "voyage.json", encoding="utf-8"))

globe_note = (
    "This is a globe view (MapLibre GL): the Arctic is drawn on a sphere instead of a "
    "flat web map, so the routes and the family's two-year way home keep their true shape "
    "over the top of the world. Optional 3D terrain (key-free elevation) is in the layers panel."
)
voyage.setdefault("meta", {}).setdefault("note", [])
if globe_note not in voyage["meta"]["note"]:
    voyage["meta"]["note"].append(globe_note)

template = open(HERE / "template_globe.html", encoding="utf-8").read()
html = template.replace("__DATA__", json.dumps(voyage, ensure_ascii=False, separators=(",", ":")))
out = HERE / "index.html"
out.write_text(html, encoding="utf-8")

v1, v2 = voyage["voyages"]
fam = voyage.get("family")
print("built ->", out)
print(f"  Voyage I : {len(v1['stops'])} stops, {len(v1['legs'])} legs")
print(f"  Voyage II: {len(v2['stops'])} stops, {len(v2['legs'])} legs")
if fam:
    print(f"  family: aboard {len(fam['aboard']['stops'])} stops / {len(fam['aboard']['geom'])} pts; "
          f"home {len(fam['home'])} nodes; side {len(fam.get('side',[]))}; onward {len(fam.get('shipOnward',[]))} pts")
print(f"  output size: {out.stat().st_size/1024:.0f} KB")
