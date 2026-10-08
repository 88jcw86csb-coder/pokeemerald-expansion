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


def decode_block(raw, width, x, y):
    """Return metatile, collision bits and elevation for one block."""
    word = struct.unpack_from("<H", raw, 2 * (y * width + x))[0]
    return word & 0x3FF, (word >> 10) & 3, word >> 12


def connected_by_collision_bits(raw, width, height, start, goal):
    """Conservative four-direction reachability on zero-collision blocks.

    A successful result does not guarantee in-game movement: tileset behavior,
    elevation, ledges and map connections also affect traversal.
    """
    from collections import deque

    def clear(x, y):
        return 0 <= x < width and 0 <= y < height and decode_block(raw, width, x, y)[1] == 0

    if not clear(*start) or not clear(*goal):
        return False
    pending = deque([start])
    seen = {start}
    while pending:
        x, y = pending.popleft()
        if (x, y) == goal:
            return True
        for nxt in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
            if nxt not in seen and clear(*nxt):
                seen.add(nxt)
                pending.append(nxt)
    return False


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
        warps = data.get("warp_events", [])
        valid = []
        for index, warp in enumerate(warps):
            x, y = warp["x"], warp["y"]
            if not (0 <= x < width and 0 <= y < height):
                failures.append(f"{name}: warp {index} outside map")
                continue
            tile, collision, elevation = decode_block(raw, width, x, y)
            print(f"  warp {index} ({x},{y}) tile={tile} collision={collision} "
                  f"elevation={elevation} -> {warp['dest_map']}:{warp['dest_warp_id']}")
            valid.append((index, (x, y)))
            if collision:
                print("  WARNING: warp block has nonzero collision bits; inspect in Porymap")
        for i, (a_index, a_pos) in enumerate(valid):
            for b_index, b_pos in valid[i + 1:]:
                if not connected_by_collision_bits(raw, width, height, a_pos, b_pos):
                    print(f"  WARNING: warp {a_index} to warp {b_index} has no "
                          "four-direction zero-collision route; inspect in Porymap")
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
