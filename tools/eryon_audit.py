#!/usr/bin/env python3
"""Static audit for the opening of Pokémon Eryon.

Run from the repository root: python3 tools/eryon_audit.py
Exit 0 only if all required migration checks pass.
This does not compile or test the ROM.
"""
from pathlib import Path
import json
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
problems = []

def check(label, passed, detail):
    print(f"{'PASS' if passed else 'FAIL'} | {label} | {detail}")
    if not passed:
        problems.append(label)

starter = ROOT / "src/starter_choose.c"
if not starter.is_file():
    check("Starter source exists", False, str(starter))
else:
    code = starter.read_text(encoding="utf-8")
    count = re.search(r"^#define\s+STARTER_MON_COUNT\s+(\d+)\b", code, re.M)
    mons = re.search(r"sStarterMon\s*\[\s*STARTER_MON_COUNT\s*\]\s*=\s*\{([^}]*)\}", code, re.S)
    species = re.findall(r"\bSPECIES_[A-Z0-9_]+\b", mons.group(1)) if mons else []
    check("Riolu is the only starter", bool(count and count.group(1) == "1" and species == ["SPECIES_RIOLU"]),
          f"count={count.group(1) if count else 'missing'}, species={species}")

for name in ("LittlerootTown", "Route101"):
    path = ROOT / "data/maps" / name / "map.json"
    if not path.is_file():
        check(f"{name} map exists", False, str(path))
        continue
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        check(f"{name} map JSON valid", False, str(exc))
        continue
    check(f"{name} replaced with Eryon region",
          data.get("region") != "REGION_HOENN" and not data.get("region_map_section", "").startswith("MAPSEC_LITTLEROOT"),
          f"region={data.get('region')}, map_section={data.get('region_map_section')}")
    if name == "Route101":
        legacy = any(c.get("map") == "MAP_OLDALE_TOWN" for c in data.get("connections", []))
        check("Route 1 no longer connects directly to Oldale", not legacy,
              f"oldale_connection={legacy}")
        scripts = ROOT / "data/maps/Route101/scripts.inc"
        if scripts.exists():
            text = scripts.read_text(encoding="utf-8")
            check("Route 1 Birch rescue script migrated", "Route101_EventScript_StartBirchRescue" not in text,
                  "legacy rescue script " + ("found" if "Route101_EventScript_StartBirchRescue" in text else "absent"))

print(f"\n{len(problems)} failed check(s).")
sys.exit(1 if problems else 0)
