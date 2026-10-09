#!/usr/bin/env python3
"""Regression checks for seven planned Eryon villages."""
import unittest
from eryon_villages import ROOT, VILLAGES, BUILDINGS, W, H, village, reachable, render


class VillageTests(unittest.TestCase):
    def test_village_facilities_and_exits(self):
        for name in VILLAGES:
            with self.subTest(village=name):
                t=village(name)
                self.assertEqual(len(t),H)
                self.assertTrue(all(len(row)==W for row in t))
                reached=reachable(t)
                needed={(0,14),(W-1,14),(18,0),(18,H-1)}
                needed.update(BUILDINGS.values())
                self.assertTrue(needed<=reached)
                path=ROOT/"docs/eryon/vilas"/f"{name}_village_plan.txt"
                self.assertEqual(path.read_text(encoding="utf-8"),render(name,t))


if __name__=="__main__":
    unittest.main()
