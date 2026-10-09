#!/usr/bin/env python3
"""Validate planned League and Victory Road layouts and their exits."""
import unittest
from eryon_league_maps import ROOT, route, league, connected, render


class LeagueMapTests(unittest.TestCase):
    def test_league_approach_and_hub(self):
        for name, fn, start, exit in (
            ("caminho_da_liga", route, (0,22), (47,22)),
            ("liga_eryon", league, (32,55), (32,0)),
        ):
            with self.subTest(name=name):
                t=fn()
                reached=connected(t,start)
                floor={(x,y) for y,row in enumerate(t) for x,c in enumerate(row) if c!="#"}
                self.assertEqual(reached,floor)
                self.assertIn(exit,reached)
                path=ROOT/"docs/eryon"/f"{name}_terrain_plan.txt"
                self.assertEqual(path.read_text(encoding="utf-8"),render(name,t))


if __name__=="__main__":
    unittest.main()
