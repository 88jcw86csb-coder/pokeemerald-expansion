#!/usr/bin/env python3
"""Validate Eryon's custom opening GBA terrain binaries.

Checks dimensions and conservative on-foot reachability, not emulator physics.
"""
import json
import struct
import unittest
from collections import deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OPENING = (
    "Eryon_VilaAurora",
    "Eryon_Rota01",
    "Eryon_Rota02",
    "Eryon_Verdelume",
    "Eryon_Rota03",
)


def flood(raw, width, height, start):
    def clear(x, y):
        if x < 0 or y < 0 or x >= width or y >= height:
            return False
        word = struct.unpack_from("<H", raw, 2 * (y * width + x))[0]
        return (word & 0x0C00) == 0

    if not clear(*start):
        return set()
    seen = {start}
    queue = deque([start])
    while queue:
        x, y = queue.popleft()
        for point in ((x + 1, y), (x - 1, y),
                      (x, y + 1), (x, y - 1)):
            if point not in seen and clear(*point):
                seen.add(point)
                queue.append(point)
    return seen


class EryonOpeningTerrainTests(unittest.TestCase):
    def test_opening_maps_have_correct_unique_dimensions_and_walkable_exits(self):
        layouts = json.loads((ROOT / "data/layouts/layouts.json").read_text(
            encoding="utf-8"))["layouts"]
        index = {entry["id"]: entry for entry in layouts}
        used = set()
        for name in OPENING:
            with self.subTest(map=name):
                data = json.loads((ROOT / "data/maps" / name / "map.json").read_text(
                    encoding="utf-8"))
                layout = index[data["layout"]]
                terrain = layout["blockdata_filepath"]
                self.assertTrue(
                    terrain.startswith("data/layouts/" + name + "/"),
                    f"{name} still inherits a Hoenn blockdata file"
                )
                self.assertNotIn(terrain, used)
                used.add(terrain)
                width, height = layout["width"], layout["height"]
                raw = (ROOT / terrain).read_bytes()
                self.assertEqual(len(raw), width * height * 2)

                start = (
                    (10, 10) if name == "Eryon_VilaAurora"
                    else (10, height - 1) if name == "Eryon_Rota01"
                    else (data["warp_events"][0]["x"],
                          data["warp_events"][0]["y"])
                )
                reachable = flood(raw, width, height, start)
                self.assertTrue(reachable)
                for event in (
                    data["warp_events"] + data["object_events"]
                    + data["bg_events"]
                ):
                    self.assertIn(
                        (event["x"], event["y"]), reachable,
                        f"{name}: blocked event or exit at {event['x']},{event['y']}"
                    )
                if name == "Eryon_VilaAurora":
                    self.assertIn((10, 0), reachable)
                elif name == "Eryon_Rota01":
                    self.assertIn((10, height - 1), reachable)

    def test_first_five_maps_do_not_require_flash_or_cut_events(self):
        for name in OPENING:
            with self.subTest(map=name):
                data = json.loads((ROOT / "data/maps" / name / "map.json").read_text(
                    encoding="utf-8"))
                self.assertFalse(data["requires_flash"])
                script = (ROOT / "data/maps" / name / "scripts.inc").read_text(
                    encoding="utf-8")
                for command in ("MOVE_CUT", "MOVE_STRENGTH", "MOVE_ROCK_SMASH",
                                "MOVE_SURF", "MOVE_DIVE", "MOVE_WATERFALL"):
                    self.assertNotIn(command, script)


if __name__ == "__main__":
    unittest.main()
