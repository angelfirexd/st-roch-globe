#!/usr/bin/env python3
"""Re-extract the VOYAGE object from an updated 2D Leaflet build into voyage.json.
Usage: python3 extract_voyage.py path/to/2d_index.html   (default: source_2d.html)"""
import re, json, sys, pathlib
src = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "source_2d.html")
html = src.read_text(encoding="utf-8")
m = re.search(r"const VOYAGE = (\{.*?\});\s*\n", html, re.S)
if not m: raise SystemExit("VOYAGE object not found in " + str(src))
data = json.loads(m.group(1))
json.dump(data, open("voyage.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("voyage.json updated from", src)
