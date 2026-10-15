#!/usr/bin/env python3
"""Tests for four newly planned connector routes."""
import unittest
from eryon_connector_routes import ROOT, ROUTES, W, H, route, reachable, render


class ConnectorRouteTests(unittest.TestCase):
    def test_exits_connected_and_plans_synchronized(self):
        for name,kind in ROUTES.items():
            with self.subTest(name=name):
                t=route(kind)
                self.assertEqual(len(t),H)
                self.assertTrue(all(len(row)==W for row in t))
                reached=reachable(t)
                self.assertIn((47,22),reached)
                walkable={(x,y) for y,row in enumerate(t)
                          for x,c in enumerate(row) if c!="#"}
                self.assertEqual(reached,walkable)
                path=ROOT/"docs/eryon"/f"{name}_terrain_plan.txt"
                # The committed plans are the playable source of truth. Several
                # routes now include hand-authored side areas after this generic
                # generator was introduced. Do not erase those later additions.
                saved=path.read_text(encoding="utf-8").splitlines()
                self.assertEqual(len(saved),H+4)
                live=[list(row) for row in saved[4:]]
                self.assertTrue(all(len(row)==W and set(row)<={"#", ".", ",", ":"}
                                    for row in live))
                accessible=reachable(live)
                self.assertIn((0,22),accessible)
                self.assertIn((47,22),accessible)
                floor={(x,y) for y,row in enumerate(live)
                       for x,c in enumerate(row) if c!="#"}
                self.assertEqual(accessible,floor)


if __name__=="__main__":
    unittest.main()
