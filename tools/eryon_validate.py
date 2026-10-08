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
    wild = load("src/data/wild_encounters.json")
    wild_group = next((group for group in wild["wild_encounter_groups"] if group["label"] == "gWildMonHeaders"), None)
    wild_by_map = {entry.get("map"): entry for entry in wild_group["encounters"]} if wild_group else {}
    for route in ("Eryon_Rota01", "Eryon_BosqueDeLumina", "Eryon_Rota02"):
        map_id = maps[route]["id"]
        encounter = wild_by_map.get(map_id)
        if not encounter or "land_mons" not in encounter:
            errors.append(f"{route}: no land wild encounters")
            continue
        mons = encounter["land_mons"]["mons"]
        if len(mons) != 12:
            errors.append(f"{route}: expected 12 land encounter slots, found {len(mons)}")
        for mon in mons:
            if mon["min_level"] > mon["max_level"]:
                errors.append(f"{route}: invalid encounter level range for {mon['species']}")
    for name, m in maps.items():
        layout = layouts.get(m["layout"])
        if layout is None:
            errors.append(f"{name}: missing layout {m['layout']}")
            continue
        width, height = layout["width"], layout["height"]
        block_path = ROOT / layout["blockdata_filepath"]
        if not block_path.exists():
            errors.append(f"{name}: missing layout binary {block_path}")
        elif block_path.stat().st_size != width * height * 2:
            errors.append(f"{name}: layout binary has {block_path.stat().st_size} bytes; expected {width * height * 2}")

        for index, warp in enumerate(m.get("warp_events", [])):
            if not (0 <= warp["x"] < width and 0 <= warp["y"] < height):
                errors.append(f"{name}: warp {index} outside {width}x{height}")
            target = maps.get(ids.get(warp["dest_map"], ""))
            if target is None:
                errors.append(f"{name}: warp {index} unknown destination {warp['dest_map']}")
            elif not (0 <= int(warp["dest_warp_id"]) < len(target.get("warp_events", []))):
                errors.append(f"{name}: warp {index} invalid destination index")
            else:
                reverse = target["warp_events"][int(warp["dest_warp_id"])]
                if reverse["dest_map"] != m["id"] or int(reverse["dest_warp_id"]) != index:
                    errors.append(f"{name}: warp {index} has no reciprocal return warp")
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
    print(f"PASS: {len(maps)} Eryon opening maps; IDs, NPC scripts, warp indices and encounter slots consistent")
    print("NOTE: collision, tiles, encounters, gameplay and compilation remain untested")
    return 0


if __name__ == "__main__":
    sys.exit(main())
