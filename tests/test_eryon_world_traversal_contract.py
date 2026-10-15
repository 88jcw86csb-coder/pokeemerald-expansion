"""Prevent recurrence of Eryon blocked events, lost roads, or broken warps.

This is a collision-bit structural test only, not a substitute for Delta.
"""
import unittest

from tools.eryon_map_traversal_audit import inspect


class EryonWorldTraversalContract(unittest.TestCase):
    def test_all_registered_maps_and_region_edges_have_reachable_events(self):
        names, results, errors = inspect()
        self.assertEqual(len(names), 42)
        self.assertEqual(len(results), 42)
        self.assertFalse(errors, "\n".join(errors))

    def test_league_and_echo_village_are_reachable(self):
        _, results, errors = inspect()
        self.assertFalse(errors, "\n".join(errors))
        for name in ("Eryon_AldeiaDosEcos", "Eryon_ValeDosEcos",
                     "Eryon_CaminhoDaLiga", "Eryon_CidadeDaLiga",
                     "Eryon_LigaClassificatoria", "Eryon_LigaEliteFour"):
            with self.subTest(map=name):
                self.assertIn(name, results)
                self.assertGreater(results[name][2], 50)


if __name__ == "__main__":
    unittest.main()
