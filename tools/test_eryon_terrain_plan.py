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

    def test_committed_terrain_matches_generator(self):
        kinds = {
            "bosque_de_lumina": "forest",
            "serra_dos_cristais": "mountain",
            "passagem_rochosa": "passage",
            "estrada_oriental": "road",
            "vale_dos_ventos": "valley",
        }
        for name, kind in kinds.items():
            with self.subTest(map=name):
                plan = ROOT / "docs" / "eryon" / f"{name}_terrain_plan.txt"
                rows = plan.read_text(encoding="utf-8").splitlines()[4:]
                self.assertEqual(rows, ["".join(row) for row in route(kind)],
                                 f"{name}: committed plan is out of sync")

    def test_lumina_northern_pond_loop(self):
        tiles = route("forest")
        accessible = reachable(tiles, (16, 38))
        for point in ((16, 10), (33, 14), (36, 17), (16, 17)):
            self.assertIn(point, accessible)
        self.assertEqual(tiles[14][33], ",")

    def test_lumina_eastern_fern_grove(self):
        tiles = route("forest")
        accessible = reachable(tiles, (16, 38))
        self.assertIn((36, 25), accessible)
        self.assertIn((23, 25), accessible)
        self.assertEqual(tiles[25][36], ",")

    def test_lumina_moss_sanctuary_has_accessible_detour(self):
        tiles = route("forest")
        accessible = reachable(tiles, (16, 38))
        for x, y in ((8, 30), (10, 28), (16, 30)):
            self.assertIn((x, y), accessible)
        self.assertEqual(tiles[30][8], ".")
        self.assertEqual(tiles[28][8], ",")

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

    def test_serra_eastern_crystal_shelf(self):
        tiles = route("mountain")
        accessible = reachable(tiles)
        for point in ((43, 11), (44, 12), (44, 22)):
            self.assertIn(point, accessible)
        self.assertEqual(tiles[11][43], ":")

    def test_serra_northwest_crystal_overlook(self):
        tiles = route("mountain")
        accessible = reachable(tiles)
        for point in ((8, 8), (12, 9), (24, 9), (24, 20)):
            self.assertIn(point, accessible)
        self.assertEqual(tiles[8][8], ":")

    def test_passage_southern_cavern_remains_accessible(self):
        tiles = route("passage")
        connected = reachable(tiles)
        for point in ((34, 34), (34, 37), (42, 37), (42, 38)):
            self.assertIn(point, connected)
        self.assertEqual(tiles[38][42], ":")

    def test_road_northern_watchpost_access(self):
        tiles = route("road")
        connected = reachable(tiles)
        for point in ((13, 10), (26, 10), (34, 10), (34, 22)):
            self.assertIn(point, connected)
        self.assertEqual(tiles[10][26], ":")

    def test_valley_southwest_windmill_ruins(self):
        tiles = route("valley")
        accessible = reachable(tiles)
        for point in ((6, 31), (10, 30), (10, 22)):
            self.assertIn(point, accessible)
        self.assertEqual(tiles[31][6], ",")

    def test_valley_has_no_unlinked_east_exit(self):
        tiles = route("valley")
        self.assertTrue(all(row[-1] == "#" for row in tiles))
        self.assertIn((31, 7), reachable(tiles))
        self.assertIn((0, 22), reachable(tiles))

    def test_mountain_and_routes_have_connected_exits(self):
        for kind in ("mountain", "passage", "road"):
            with self.subTest(kind=kind):
                tiles = route(kind)
                self.assertIn((47, 22), reachable(tiles))

if __name__ == "__main__":
    unittest.main()
