#!/usr/bin/env python3
"""Regression checks for Eryon's five distinct terrain plans."""
import unittest
import json
from pathlib import Path
from eryon_terrain_plan import WIDTH, HEIGHT, ROOT, MAP_NAMES, route, reachable

class TerrainPlansTests(unittest.TestCase):
    def test_forest_uses_north_south_trail_not_horizontal_highway(self):
        tiles = route("forest")
        self.assertEqual((len(tiles), len(tiles[0])), (HEIGHT, WIDTH))
        self.assertIn((14, 5), reachable(tiles, (16, 38)))
        self.assertEqual(tiles[22][0], "#")
        self.assertEqual(tiles[22][WIDTH - 1], "#")
        for x, y in ((15, 14), (23, 18), (20, 25), (13, 16), (19, 21)):
            self.assertIn((x, y), reachable(tiles, (16, 38)))

    def test_passage_northern_ridge_connects_to_eclipse_checkpoint(self):
        tiles = route("passage")
        accessible = reachable(tiles)
        for position in ((9, 11), (37, 11), (42, 11), (37, 14), (37, 18)):
            self.assertIn(position, accessible)
        self.assertEqual(tiles[11][24], ":")

    def test_all_registered_events_reachable(self):
        kinds = {
            "bosque_de_lumina": "forest",
            "serra_dos_cristais": "mountain",
            "passagem_rochosa": "passage",
            "estrada_oriental": "road",
            "vale_dos_ventos": "valley",
        }
        for name, kind in kinds.items():
            with self.subTest(map=name):
                tiles = route(kind)
                start = (16, 38) if kind == "forest" else (0, 22)
                accessible = reachable(tiles, start)
                data = json.loads((ROOT / "data/maps" / MAP_NAMES[name] / "map.json").read_text(encoding="utf-8"))
                events = data["warp_events"] + data["object_events"] + data["bg_events"]
                for event in events:
                    self.assertIn((event["x"], event["y"]), accessible,
                                  f"{name}: unreachable event {event}")

    def test_mountain_and_routes_have_connected_exits(self):
        for kind in ("mountain", "passage", "road", "valley"):
            with self.subTest(kind=kind):
                tiles = route(kind)
                self.assertIn((47, 22), reachable(tiles))

if __name__ == "__main__":
    unittest.main()
