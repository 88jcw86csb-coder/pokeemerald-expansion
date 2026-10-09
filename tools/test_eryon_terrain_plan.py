#!/usr/bin/env python3
"""Regression checks for Eryon's five distinct terrain plans."""
import unittest
from eryon_terrain_plan import WIDTH, HEIGHT, route, reachable

class TerrainPlansTests(unittest.TestCase):
    def test_forest_uses_north_south_trail_not_horizontal_highway(self):
        tiles = route("forest")
        self.assertEqual((len(tiles), len(tiles[0])), (HEIGHT, WIDTH))
        self.assertIn((14, 5), reachable(tiles, (16, 38)))
        self.assertEqual(tiles[22][0], "#")
        self.assertEqual(tiles[22][WIDTH - 1], "#")
        for x, y in ((15, 14), (23, 18), (20, 25), (13, 16), (19, 21)):
            self.assertIn((x, y), reachable(tiles, (16, 38)))

    def test_mountain_and_routes_have_connected_exits(self):
        for kind in ("mountain", "passage", "road", "valley"):
            with self.subTest(kind=kind):
                tiles = route(kind)
                self.assertIn((47, 22), reachable(tiles))

if __name__ == "__main__":
    unittest.main()
