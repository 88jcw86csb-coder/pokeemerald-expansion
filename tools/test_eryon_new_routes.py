#!/usr/bin/env python3
"""Check all three proposed Eryon route plans against their generator."""
import unittest
from eryon_new_routes import ROOT, W, H, ROUTES, build, connected, render


class NewRoutesTests(unittest.TestCase):
    def test_all_new_routes_are_connected_and_synchronized(self):
        for name, kind in ROUTES.items():
            with self.subTest(name=name):
                tiles = build(kind)
                self.assertEqual(len(tiles), H)
                self.assertTrue(all(len(row) == W for row in tiles))
                start = (23, 43) if kind == "waterfalls" else (0, 22)
                goal = (23, 0) if kind == "waterfalls" else (47, 22)
                accessible = connected(tiles, start)
                self.assertIn(goal, accessible)
                walkable = {(x, y) for y, row in enumerate(tiles)
                            for x, cell in enumerate(row) if cell != "#"}
                self.assertEqual(accessible, walkable)
                saved = (ROOT / "docs/eryon" / f"{name}_terrain_plan.txt").read_text(encoding="utf-8")
                self.assertEqual(saved, render(name, tiles))

    def test_distinct_terrain(self):
        signatures = {"".join("".join(row) for row in build(kind)) for kind in ROUTES.values()}
        self.assertEqual(len(signatures), 3)


if __name__ == "__main__":
    unittest.main()
