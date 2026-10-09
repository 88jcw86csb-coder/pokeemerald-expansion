#!/usr/bin/env python3
"""Validate the Star Cavern concept before it is installed in the game."""
import unittest
from eryon_star_cavern import ROOT, W, H, cavern, reachable, render


class StarCavernTests(unittest.TestCase):
    def test_connected_cavern_and_synchronized_plan(self):
        terrain=cavern()
        self.assertEqual(len(terrain),H)
        self.assertTrue(all(len(row)==W for row in terrain))
        walkable={(x,y) for y,row in enumerate(terrain)
                  for x,tile in enumerate(row) if tile!="#"}
        self.assertEqual(reachable(terrain),walkable)
        self.assertIn((47,22),walkable)
        source=ROOT/"docs/eryon/gruta_das_estrelas_terrain_plan.txt"
        self.assertEqual(source.read_text(encoding="utf-8"),render(terrain))


if __name__=="__main__":
    unittest.main()
