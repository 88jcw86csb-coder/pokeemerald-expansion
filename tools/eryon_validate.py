#!/usr/bin/env python3
"""Static consistency checks for Eryon's opening maps (not an emulator test)."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NAMES = ["Eryon_VilaAurora", "Eryon_Rota01", "Eryon_BosqueDeLumina", "Eryon_Rota02", "Eryon_Verdelume"]


def load(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def main():
    errors = []
    groups = load("data/maps/map_groups.json")
    layouts = {entry["id"]: entry for entry in load("data/layouts/layouts.json")["layouts"]}
    scripts = (ROOT / "data/event_scripts.s").read_text(encoding="utf-8")
    maps = {name: load(f"data/maps/{name}/map.json") for name in NAMES}
    ids = {m["id"]: name for name, m in maps.items()}
    if set(groups.get("gMapGroup_Eryon", [])) != set(NAMES):
        errors.append("Eryon map group does not match opening map files")
    for name, m in maps.items():
        layout = layouts.get(m["layout"])
        if layout is None:
            errors.append(f"{name}: missing layout {m['layout']}")
            continue
        width, height = layout["width"], layout["height"]
        for index, warp in enumerate(m.get("warp_events", [])):
            if not (0 <= warp["x"] < width and 0 <= warp["y"] < height):
                errors.append(f"{name}: warp {index} outside {width}x{height}")
            target = maps.get(ids.get(warp["dest_map"], ""))
            if target is None:
                errors.append(f"{name}: warp {index} unknown destination {warp['dest_map']}")
            elif not (0 <= int(warp["dest_warp_id"]) < len(target.get("warp_events", []))):
                errors.append(f"{name}: warp {index} invalid destination index")
        for index, obj in enumerate(m.get("object_events", [])):
            if not (0 <= obj["x"] < width and 0 <= obj["y"] < height):
                errors.append(f"{name}: NPC {index} outside {width}x{height}")
            if obj["script"] != "0x0":
                script_file = ROOT / "data/maps" / name / "scripts.inc"
                if not script_file.exists() or not re.search(r"(?m)^" + re.escape(obj["script"]) + r"::", script_file.read_text(encoding="utf-8")):
                    errors.append(f"{name}: missing NPC script {obj['script']}")
                if f'data/maps/{name}/scripts.inc' not in scripts:
                    errors.append(f"{name}: NPC scripts not included by data/event_scripts.s")
    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1
    print(f"PASS: {len(maps)} Eryon opening maps; IDs, NPC scripts, and warp indices consistent")
    print("NOTE: collision, tiles, encounters, gameplay and compilation remain untested")
    return 0


if __name__ == "__main__":
    sys.exit(main())
