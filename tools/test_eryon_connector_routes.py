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
                self.assertEqual(path.read_text(encoding="utf-8"),render(name,t))


if __name__=="__main__":
    unittest.main()
