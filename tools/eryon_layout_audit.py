#!/usr/bin/env python3
"""Inspect actual GBA map blockdata at Eryon warp coordinates.

Read-only diagnostics: this does not claim that a tile is traversable.
Block word layout: 10-bit metatile ID, 2-bit collision, 4-bit elevation.
"""
import argparse
import json
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read_json(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def inspect():
    groups = read_json("data/maps/map_groups.json")
    layouts = {x["id"]: x for x in read_json("data/layouts/layouts.json")["layouts"]}
    failures = []
    for name in groups["gMapGroup_Eryon"]:
        data = read_json(f"data/maps/{name}/map.json")
        layout = layouts[data["layout"]]
        width, height = layout["width"], layout["height"]
        path = ROOT / layout["blockdata_filepath"]
        if not path.exists():
            failures.append(f"{name}: missing {path}")
            continue
        raw = path.read_bytes()
        if len(raw) != width * height * 2:
            failures.append(f"{name}: blockdata {len(raw)} bytes, expected {width * height * 2}")
            continue
        source = layout["blockdata_filepath"]
        print(f"MAP {name}: {width}x{height}, terrain={source}")
        for index, warp in enumerate(data.get("warp_events", [])):
            x, y = warp["x"], warp["y"]
            if not (0 <= x < width and 0 <= y < height):
                failures.append(f"{name}: warp {index} outside map")
                continue
            word = struct.unpack_from("<H", raw, 2 * (y * width + x))[0]
            tile, collision, elevation = word & 0x3FF, (word >> 10) & 3, word >> 12
            print(f"  warp {index} ({x},{y}) tile={tile} collision={collision} "
                  f"elevation={elevation} -> {warp['dest_map']}:{warp['dest_warp_id']}")
            if collision:
                print("  WARNING: warp block has nonzero collision bits; inspect in Porymap")
        if not source.startswith("data/layouts/Eryon_"):
            print("  WARNING: inherited Hoenn terrain; geometry not yet original")
    return failures


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--strict", action="store_true",
                        help="fail if any map still uses inherited terrain")
    args = parser.parse_args()
    failures = inspect()
    if args.strict:
        layouts = {x["id"]: x for x in read_json("data/layouts/layouts.json")["layouts"]}
        for name in read_json("data/maps/map_groups.json")["gMapGroup_Eryon"]:
            data = read_json(f"data/maps/{name}/map.json")
            source = layouts[data["layout"]]["blockdata_filepath"]
            if not source.startswith("data/layouts/Eryon_"):
                failures.append(f"{name}: inherited terrain {source}")
    for failure in failures:
        print("ERROR:", failure)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
