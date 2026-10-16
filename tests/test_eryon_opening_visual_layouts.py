"""Prevent broken sign tiles, random scattered blockers and missing paths on first two maps."""
from pathlib import Path
import struct
import unittest
from tools.eryon_opening_visual_layouts import MAPS,TILES,layout_bytes,validate,component,REQUIRED
ROOT=Path(__file__).resolve().parents[1]

class OpeningVisualLayoutTests(unittest.TestCase):
    def test_source_and_binaries_agree_without_background_regeneration(self):
        for name,rows in MAPS.items():
            with self.subTest(map=name):
                data=layout_bytes(rows)
                self.assertEqual((ROOT/"data/layouts"/name/"map.bin").read_bytes(),data)
                validate(name,data)
                self.assertNotIn(0x3003,struct.unpack("<400H",data))
                self.assertNotIn(0x3C01,struct.unpack("<400H",data))

    def test_four_complete_rooftops_in_aurora(self):
        rows=MAPS["Eryon_VilaAurora"]
        self.assertEqual(sum(row.count("A") for row in rows),4)
        self.assertEqual(sum(row.count("I") for row in rows),4)
        self.assertGreater(sum(row.count("=") for row in rows),65)
        self.assertGreater(sum(row.count("T") for row in rows),15)

    def test_route_has_two_connected_entry_points_and_clusters(self):
        rows=MAPS["Eryon_Rota01"]
        self.assertGreater(sum(row.count("T") for row in rows),35)
        self.assertGreater(sum(row.count("=") for row in rows),40)
        data=layout_bytes(rows)
        visited=component(data,(10,19))
        self.assertTrue(set(REQUIRED["Eryon_Rota01"]).issubset(visited))

if __name__=="__main__":
    unittest.main()
