#!/usr/bin/env python3
"""Regression tests for the eight large gym-city design layouts."""
import unittest
from eryon_gym_cities import ROOT, CITIES, W, H, BUILDINGS, city, accessible, render


class GymCityTests(unittest.TestCase):
    def test_each_city_has_its_own_accessible_district(self):
        landmarks = {
            "verdelume": (7, 7), "neonara": (55, 7),
            "frostheim": (7, 48), "arkhara": (55, 48),
            "umbra": (8, 8), "ignivar": (55, 8),
            "lunaris": (8, 47), "drakonia": (55, 47),
        }
        for name, point in landmarks.items():
            with self.subTest(city=name):
                tiles = city(name)
                self.assertEqual(tiles[point[1]][point[0]], "P")
                self.assertIn(point, accessible(tiles))

    def test_cities_have_reachable_facilities_and_exits(self):
        for name in CITIES:
            with self.subTest(city=name):
                tiles = city(name)
                self.assertEqual(len(tiles), H)
                self.assertTrue(all(len(row) == W for row in tiles))
                reached = accessible(tiles)
                required = {(0,28), (W-1,28), (32,0), (32,H-1)}
                required.update(BUILDINGS.values())
                self.assertTrue(required <= reached, f"{name}: blocked gym, services or exit")
                saved = (ROOT / "docs/eryon/cidades" / f"{name}_city_plan.txt").read_text(encoding="utf-8")
                self.assertEqual(saved, render(name, tiles))


if __name__ == "__main__":
    unittest.main()
