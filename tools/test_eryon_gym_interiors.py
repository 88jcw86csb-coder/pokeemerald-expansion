"""Gym arena geometry contracts; static checks, not Delta gameplay tests."""
import json
from pathlib import Path
import struct
import unittest

from eryon_gym_interiors import (CITIES, WIDTH, HEIGHT, ARRIVAL, LEADER,
                                  GUIDE, FIRST_PANEL, SECOND_PANEL, EXIT,
                                  EVENTS, layout, validate, reachable)

ROOT = Path(__file__).resolve().parents[1]


class EryonDistinctGymInteriors(unittest.TestCase):
    def test_eight_distinct_collision_safe_arenas(self):
        seen = set()
        for index, city in enumerate(CITIES):
            with self.subTest(city=city):
                cells = layout(index)
                self.assertGreater(validate(cells), 300)
                raw = struct.pack(f"<{WIDTH * HEIGHT}H",
                                  *(v for row in cells for v in row))
                self.assertNotIn(raw, seen, "gym map copied from another gym")
                seen.add(raw)
                self.assertEqual(len(raw), WIDTH * HEIGHT * 2)
                self.assertEqual(raw, (
                    ROOT / "data/layouts" / f"GymEryon_{city}" / "map.bin"
                ).read_bytes())

    def test_npcs_and_puzzle_flags_stay_accessible(self):
        for index, city in enumerate(CITIES):
            with self.subTest(city=city):
                info = json.loads((
                    ROOT / "data/maps" / f"GymEryon_{city}" / "map.json"
                ).read_text(encoding="utf-8"))
                coords = {(obj["x"], obj["y"]) for obj in info["object_events"]}
                signs = {(obj["x"], obj["y"]) for obj in info["bg_events"]}
                self.assertEqual(coords, {LEADER, GUIDE})
                self.assertEqual(signs, {FIRST_PANEL, SECOND_PANEL, EXIT})
                self.assertTrue(coords | signs | {ARRIVAL} <= EVENTS)
                cells = layout(index)
                access = reachable(cells, ARRIVAL, coords)
                self.assertTrue(signs <= access)
                for npc in coords:
                    self.assertTrue(any(
                        (npc[0] + dx, npc[1] + dy) in access
                        for dx, dy in ((0,1),(0,-1),(1,0),(-1,0))
                    ))

    def test_wall_collision_and_floor_elevation(self):
        for index, city in enumerate(CITIES):
            with self.subTest(city=city):
                cells = layout(index)
                for y, row in enumerate(cells):
                    for x, value in enumerate(row):
                        self.assertEqual(value & 0xF000, 0x3000)
                        if x in (0, WIDTH-1) or y in (0, HEIGHT-1):
                            self.assertNotEqual(value & 0x0C00, 0)
                for x, y in EVENTS:
                    self.assertEqual(cells[y][x] & 0x0C00, 0)


if __name__ == "__main__":
    unittest.main()
