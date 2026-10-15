"""Conservative terrain-level regression for Eryon's opening and orchard journey.

Uses real registered map.bin blocks, not just JSON warp declarations.
Passing says nothing about runtime warp behavior, tileset effects, or Delta.
"""
import json
import struct
import unittest
from collections import deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAPS = ROOT / "data/maps"
LAYOUTS = {
    item["id"]: item for item in
    json.loads((ROOT / "data/layouts/layouts.json").read_text())["layouts"]
}
CASES = {
    "Eryon_VilaAurora": ((10, 10), (10, 0)),
    "Eryon_Rota01": ((10, 19), (19, 10)),
    "Eryon_Rota04": ((0, 22), (47, 22)),
    "Eryon_Rota03": ((0, 11), (49, 11)),
    "Eryon_Neonara": ((0, 28), (63, 28)),
}


def connected_component(raw, width, height, start):
    words = struct.unpack("<" + "H" * (width * height), raw)
    def clear(x, y):
        return 0 <= x < width and 0 <= y < height and not words[y * width + x] & 0xC00
    if not clear(*start):
        return set()
    seen = {start}
    q = deque([start])
    while q:
        x, y = q.popleft()
        for nxt in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
            if nxt not in seen and clear(*nxt):
                seen.add(nxt)
                q.append(nxt)
    return seen


class EryonFirstActPhysicalJourneyTests(unittest.TestCase):
    def test_five_map_terrain_traversal(self):
        for name, (start, exit_at) in CASES.items():
            with self.subTest(map=name):
                data = json.loads((MAPS / name / "map.json").read_text())
                layout = LAYOUTS[data["layout"]]
                width, height = layout["width"], layout["height"]
                raw = (ROOT / layout["blockdata_filepath"]).read_bytes()
                self.assertEqual(len(raw), width * height * 2)
                component = connected_component(raw, width, height, start)
                self.assertIn(exit_at, component,
                              f"{name}: connection/warp tile unreachable from entry")

    def test_road_04_all_events_are_accessible_from_arrival(self):
        name = "Eryon_Rota04"
        data = json.loads((MAPS / name / "map.json").read_text())
        layout = LAYOUTS[data["layout"]]
        raw = (ROOT / layout["blockdata_filepath"]).read_bytes()
        visited = connected_component(raw, layout["width"], layout["height"], (0,22))
        self.assertGreaterEqual(len(visited), 700)
        for kind in ("warp_events", "object_events", "bg_events"):
            for e in data[kind]:
                self.assertIn((e["x"], e["y"]), visited,
                              f"Rota04 {kind} at ({e['x']},{e['y']}) is blocked")


if __name__ == "__main__":
    unittest.main()
