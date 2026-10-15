#!/usr/bin/env python3
"""Audit scripted Eryon map warps against registered layout collision data.

JSON warp reciprocity alone misses the League rooms, whose doors are scripts.
This checks script destinations and physical arrival components, without
pretending to verify metatile behavior, movement elevation or emulator play.
"""
from collections import deque
import json
from pathlib import Path
import re
import struct

ROOT = Path(__file__).resolve().parents[1]
SCRIPT_WARP = re.compile(
    r"(?m)^\s*warp\s+(MAP_[A-Z0-9_]+)\s*,\s*(\d+)\s*,\s*(\d+)\s*(?:@[^\n]*)?$"
)
LEAGUE_ROOMS = {
    "Eryon_LigaRecepcao",
    "Eryon_LigaClassificatoria",
    "Eryon_LigaRecuperacao",
    "Eryon_LigaEliteFour",
}


def component(words, width, height, origin):
    def clear(p):
        x, y = p
        return (0 <= x < width and 0 <= y < height
                and not words[y * width + x] & 0xC00)

    if not clear(origin):
        return set()
    visited = {origin}
    pending = deque([origin])
    while pending:
        x, y = pending.popleft()
        for neighbor in ((x - 1, y), (x + 1, y),
                         (x, y - 1), (x, y + 1)):
            if neighbor not in visited and clear(neighbor):
                visited.add(neighbor)
                pending.append(neighbor)
    return visited


def audit(root=ROOT):
    groups = json.loads((root / "data/maps/map_groups.json").read_text())
    names = groups["gMapGroup_Eryon"]
    layouts = {
        item["id"]: item
        for item in json.loads((root / "data/layouts/layouts.json").read_text())["layouts"]
    }
    maps = {
        name: json.loads((root / "data/maps" / name / "map.json").read_text())
        for name in names
    }
    by_id = {item["id"]: name for name, item in maps.items()}
    errors, warnings, landings = [], [], {}
    count = 0
    for name in names:
        text = (root / "data/maps" / name / "scripts.inc").read_text()
        for match in SCRIPT_WARP.finditer(text):
            count += 1
            target_id, xs, ys = match.groups()
            target_name = by_id.get(target_id)
            if target_name is None:
                errors.append(f"{name}: scripted warp targets unknown map {target_id}")
                continue
            dest = maps[target_name]
            layout = layouts.get(dest["layout"])
            if layout is None:
                errors.append(f"{name}: scripted warp targets missing layout {target_name}")
                continue
            x, y = int(xs), int(ys)
            width, height = layout["width"], layout["height"]
            if not 0 <= x < width or not 0 <= y < height:
                errors.append(f"{name}: scripted warp to {target_name} outside {width}x{height}: ({x},{y})")
                continue
            landing = (x, y)
            landings.setdefault(target_name, set()).add(landing)
    for name, arrivals in landings.items():
        data = maps[name]
        layout = layouts[data["layout"]]
        width, height = layout["width"], layout["height"]
        path = root / layout["blockdata_filepath"]
        if not path.is_file():
            errors.append(f"{name}: missing collision binary {path}")
            continue
        raw = path.read_bytes()
        if len(raw) != width * height * 2:
            errors.append(f"{name}: wrong collision binary length")
            continue
        blocks = struct.unpack(f"<{width * height}H", raw)
        for landing in sorted(arrivals):
            region = component(blocks, width, height, landing)
            if not region:
                errors.append(f"{name}: scripted arrival {landing} is blocked")
                continue
            for kind in ("object_events", "bg_events"):
                for index, event in enumerate(data[kind]):
                    pos = (event["x"], event["y"])
                    adjacent = (
                        pos, (pos[0] - 1, pos[1]), (pos[0] + 1, pos[1]),
                        (pos[0], pos[1] - 1), (pos[0], pos[1] + 1)
                    )
                    if not any(p in region for p in adjacent):
                        issue = f"{name}: scripted arrival {landing} cannot reach {kind}[{index}] at {pos}"
                        if name in LEAGUE_ROOMS:
                            errors.append(issue)
                        else:
                            warnings.append(issue)
    if not landings:
        errors.append("No Eryon scripted-warp destinations were found")
    return {
        "maps": len(names),
        "script_warps": count,
        "destinations": len(landings),
        "errors": errors,
        "warnings": warnings,
    }


def main():
    report = audit()
    print(f"Scripted Eryon warp arrivals: {report['script_warps']} transitions, "
          f"{report['destinations']} destination maps / {report['maps']} registered maps")
    for item in report["warnings"]:
        print("REVIEW:", item)
    for item in report["errors"]:
        print("ERROR:", item)
    if report["errors"]:
        return 1
    print("PASS: declared script arrivals exist and League NPCs are physically approachable")
    print("NOTE: static tile collision only; emulator gameplay remains unverified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
