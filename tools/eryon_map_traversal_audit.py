#!/usr/bin/env python3
"""Conservative physical/network audit of all registered Eryon maps.

This validates blockdata collision bits, connectivity, reciprocal warps and
script-declared transitions. It cannot validate tileset behaviors, NPC
blocking, battle execution, dialogue rendering, or Delta gameplay.
"""
from collections import deque
import json
from pathlib import Path
import re
import struct

ROOT = Path(__file__).resolve().parents[1]
OPPOSITE = {"up": "down", "down": "up", "left": "right", "right": "left"}


def data(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def inspect():
    names = data("data/maps/map_groups.json")["gMapGroup_Eryon"]
    layouts = {layout["id"]: layout for layout in data("data/layouts/layouts.json")["layouts"]}
    maps = {name: data(f"data/maps/{name}/map.json") for name in names}
    names_by_id = {m["id"]: name for name, m in maps.items()}
    errors = []
    edges = {name: set() for name in names}
    results = {}
    if len(names) != len(set(names)) or len(names_by_id) != len(names):
        errors.append("duplicate Eryon map name or map ID")

    for name, m in maps.items():
        layout = layouts.get(m["layout"])
        if not layout:
            errors.append(f"{name}: missing layout {m['layout']}")
            continue
        w, h = layout["width"], layout["height"]
        path = ROOT / layout["blockdata_filepath"]
        if not path.is_file():
            errors.append(f"{name}: missing layout blockdata {path}")
            continue
        raw = path.read_bytes()
        if len(raw) != w * h * 2:
            errors.append(f"{name}: blockdata length {len(raw)} != {2*w*h}")
            continue
        tiles = struct.unpack(f"<{w*h}H", raw)

        def passable(x, y):
            return 0 <= x < w and 0 <= y < h and not (tiles[y*w+x] & 0x0C00)

        event_groups = (("warp", m.get("warp_events", [])),
                        ("NPC", m.get("object_events", [])),
                        ("sign", m.get("bg_events", [])),
                        ("coordinate", m.get("coord_events", [])))
        events = [(kind, e) for kind, group in event_groups for e in group]
        event_coords = [(e["x"], e["y"]) for _, e in events]
        if len(set(event_coords)) != len(event_coords):
            errors.append(f"{name}: multiple events occupy identical tiles")
        for kind, e in events:
            if not passable(e["x"], e["y"]):
                errors.append(f"{name}: {kind} at ({e['x']},{e['y']}) is blocked")
        start = (10, 10) if name == "Eryon_VilaAurora" else (
            event_coords[0] if event_coords else None)
        if start is None or not passable(*start):
            errors.append(f"{name}: no walkable start candidate")
            continue
        seen = {start}
        q = deque([start])
        while q:
            x, y = q.popleft()
            for nx, ny in ((x-1,y), (x+1,y), (x,y-1), (x,y+1)):
                if (nx, ny) not in seen and passable(nx, ny):
                    seen.add((nx, ny))
                    q.append((nx, ny))
        for kind, e in events:
            if (e["x"], e["y"]) not in seen:
                errors.append(f"{name}: {kind} at ({e['x']},{e['y']}) is unreachable")
        results[name] = (w, h, len(seen), len(events))

        for index, warp in enumerate(m.get("warp_events", [])):
            dest = names_by_id.get(warp["dest_map"])
            if dest is None:
                errors.append(f"{name}: warp {index} points outside Eryon")
                continue
            to_warps = maps[dest].get("warp_events", [])
            dest_index = int(warp["dest_warp_id"])
            if not 0 <= dest_index < len(to_warps):
                errors.append(f"{name}: warp {index} has invalid target index")
                continue
            opposite = to_warps[dest_index]
            if opposite["dest_map"] != m["id"] or int(opposite["dest_warp_id"]) != index:
                errors.append(f"{name}: warp {index} lacks reciprocal counterpart")
            edges[name].add(dest)
        for connection in m.get("connections") or []:
            dest = names_by_id.get(connection["map"])
            direction = connection.get("direction")
            if dest is None or direction not in OPPOSITE:
                errors.append(f"{name}: unknown edge connection {connection}")
                continue
            reciprocal = any(
                c["map"] == m["id"] and c["direction"] == OPPOSITE[direction]
                for c in maps[dest].get("connections") or [])
            if not reciprocal:
                errors.append(f"{name}: edge connection to {dest} is not reciprocal")
            if direction == "up":
                border = [(x, 0) for x in range(w)]
            elif direction == "down":
                border = [(x, h-1) for x in range(w)]
            elif direction == "left":
                border = [(0, y) for y in range(h)]
            else:
                border = [(w-1, y) for y in range(h)]
            if not any(p in seen for p in border):
                errors.append(f"{name}: edge connection {direction} cannot be reached")
            edges[name].add(dest)
        source = (ROOT / "data/maps" / name / "scripts.inc").read_text(encoding="utf-8")
        for target_id in re.findall(r"(?m)^\s*warp\s+(MAP_ERYON_[A-Z0-9_]+)\s*,", source):
            dest = names_by_id.get(target_id)
            if dest is None:
                errors.append(f"{name}: script warp to unregistered map {target_id}")
            else:
                edges[name].add(dest)

    start = "Eryon_VilaAurora"
    seen_maps = {start}
    pending = deque([start])
    while pending:
        name = pending.popleft()
        for dest in edges[name]:
            if dest not in seen_maps:
                seen_maps.add(dest)
                pending.append(dest)
    for missing in sorted(set(names) - seen_maps):
        errors.append(f"{missing}: unreachable in regional warp/connection/script graph")
    return names, results, errors


def main():
    names, results, errors = inspect()
    print(f"Eryon physical audit: {len(results)}/{len(names)} maps inspected")
    print("Network graph includes script transitions; this is not a gameplay test.")
    for e in errors:
        print("FAIL:", e)
    if errors:
        return 1
    print("PASS: registered event coordinates, physical corridors, warp reciprocity and region graph")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
