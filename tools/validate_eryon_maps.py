#!/usr/bin/env python3
"""Static checks for Eryon map registration, reciprocal warps and event scripts.

Run from the repository root: python3 tools/validate_eryon_maps.py
This does not replace a ROM build or in-game collision tests.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAPS = ROOT / "data/maps"
groups = json.loads((MAPS / "map_groups.json").read_text())
layouts = json.loads((ROOT / "data/layouts/layouts.json").read_text())
registered = groups["gMapGroup_Eryon"]
layout_by_id = {entry["id"]: entry for entry in layouts["layouts"]}
errors = []
maps = {}
for name in registered:
    folder = MAPS / name
    try:
        data = json.loads((folder / "map.json").read_text())
        scripts = (folder / "scripts.inc").read_text()
    except (OSError, ValueError) as exc:
        errors.append(f"{name}: missing or invalid files: {exc}")
        continue
    if data["name"] != name:
        errors.append(f"{name}: name mismatch: {data['name']}")
    if data["id"] in maps:
        errors.append(f"{name}: duplicate map id {data['id']}")
    maps[data["id"]] = (name, data)
    layout = layout_by_id.get(data["layout"])
    if layout is None:
        errors.append(f"{name}: missing layout {data['layout']}")
        continue
    width, height = layout["width"], layout["height"]
    occupied = set()
    for kind in ("object_events", "bg_events", "warp_events", "coord_events"):
        for event in data.get(kind, []):
            x, y = event["x"], event["y"]
            if kind == "object_events":
                if (x, y) in occupied:
                    errors.append(f"{name}: overlapping NPCs at ({x},{y})")
                occupied.add((x, y))
            if not (0 <= x < width and 0 <= y < height):
                errors.append(f"{name}: {kind} at ({x},{y}) outside {width}x{height}")
            script = event.get("script")
            if script and not re.search(r"^" + re.escape(script) + r"::", scripts, re.M):
                errors.append(f"{name}: undefined script {script}")
master = (ROOT / "data/event_scripts.s").read_text()
for name, data in maps.values():
    include = f'data/maps/{name}/scripts.inc'
    if include not in master:
        errors.append(f"{name}: script missing from data/event_scripts.s")
    for index, warp in enumerate(data.get("warp_events", [])):
        destination = maps.get(warp["dest_map"])
        if destination is None:
            errors.append(f"{name}: warp {index} points to unregistered map {warp['dest_map']}")
            continue
        dest_name, dest_data = destination
        dest_warps = dest_data.get("warp_events", [])
        dest_index = int(warp["dest_warp_id"])
        if not (0 <= dest_index < len(dest_warps)):
            errors.append(f"{name}: warp {index} has invalid destination index {dest_index} in {dest_name}")
        elif dest_warps[dest_index]["dest_map"] != data["id"]:
            errors.append(f"{name}: warp {index} does not return from {dest_name}")
# Connections must point back to the source map in the opposite direction.
opposites = {"up": "down", "down": "up", "left": "right", "right": "left"}
for name, data in maps.values():
    for connection in data.get("connections") or []:
        dest = maps.get(connection["map"])
        if dest is None:
            errors.append(f"{name}: connection to unregistered map {connection['map']}")
            continue
        dest_name, dest_map = dest
        if not any(
            other["map"] == data["id"]
            and other["direction"] == opposites.get(connection["direction"])
            for other in dest_map.get("connections") or []
        ):
            errors.append(f"{name}: connection to {dest_name} lacks reverse direction")

# Shared base-game blockdata is temporary and must not be called original terrain.
for name, data in maps.values():
    layout = layout_by_id.get(data["layout"])
    if layout and not layout["blockdata_filepath"].startswith("data/layouts/Eryon"):
        print(f"WARNING: {name} still reuses base-game terrain: {layout['blockdata_filepath']}")

if errors:
    print("Eryon static validation FAILED:")
    for error in errors:
        print(" -", error)
    sys.exit(1)
print(f"Eryon static validation OK: {len(maps)} maps checked.")
