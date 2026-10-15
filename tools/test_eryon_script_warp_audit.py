"""Regression coverage for scripted League-room entrances and regional exits.

Runs against registered map.json, scripts.inc and real map.bin collision bits.
Structural proof only: movement behavior, save/load and Delta are not tested.
"""
import unittest

from eryon_script_warp_audit import audit, component, SCRIPT_WARP


class EryonScriptedWarpAuditTests(unittest.TestCase):
    def test_script_opcode_pattern_parses_destinations(self):
        sample = "    warp MAP_ERYON_LIGA_RECUPERACAO, 12, 14\n"
        match = SCRIPT_WARP.search(sample)
        self.assertIsNotNone(match)
        self.assertEqual(match.groups(), ("MAP_ERYON_LIGA_RECUPERACAO", "12", "14"))

    def test_collision_graph_rejects_blocked_arrival(self):
        blocks = (0x3001, 0x3C01, 0x3001,
                  0x3C01, 0x3C01, 0x3C01,
                  0x3001, 0x3C01, 0x3001)
        self.assertEqual(component(blocks, 3, 3, (1, 1)), set())
        self.assertEqual(component(blocks, 3, 3, (0, 0)), {(0, 0)})

    def test_actual_script_destinations_and_league_accessibility(self):
        report = audit()
        self.assertEqual(report["maps"], 42)
        self.assertGreaterEqual(report["script_warps"], 7)
        self.assertGreaterEqual(report["destinations"], 4)
        self.assertEqual(report["errors"], [], "\n".join(report["errors"]))


if __name__ == "__main__":
    unittest.main()
