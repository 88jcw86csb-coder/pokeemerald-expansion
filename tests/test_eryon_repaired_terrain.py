"""Prevent regression to 0x003 storefront signs and grass walls in Eryon maps."""
from pathlib import Path
import json
import struct
import unittest
from tools.eryon_terrain_visual_repair import retile_word,repair

ROOT=Path(__file__).resolve().parents[1]

class MetatileQualityContracts(unittest.TestCase):
    def test_placeholder_sign_and_same_grass_wall_are_remapped(self):
        self.assertEqual(retile_word(0x3003),0x3069)
        self.assertEqual(retile_word(0x3002),0x301C)
        self.assertEqual(retile_word(0x3001),0x302C)
        self.assertEqual(retile_word(0x3C01),0x3C16)
        for word in (0x3C01,0x3001,0x3002,0x3003,0x30A7,0x3C0D):
            self.assertEqual(retile_word(word)&0xFC00,word&0xFC00)

    def test_all_42_region_maps_have_repairable_collisions(self):
        """Base maps remain byte-identical until after regression testing."""
        from tools.eryon_terrain_visual_repair import retile_word
        names=json.loads((ROOT/"data/maps/map_groups.json").read_text())["gMapGroup_Eryon"]
        layouts={x["id"]:x for x in json.loads((ROOT/"data/layouts/layouts.json").read_text())["layouts"]}
        self.assertEqual(len(names),42)
        for name in names:
            with self.subTest(map=name):
                info=json.loads((ROOT/"data/maps"/name/"map.json").read_text())
                layout=layouts[info["layout"]]
                raw=(ROOT/layout["blockdata_filepath"]).read_bytes()
                words=struct.unpack(f"<{len(raw)//2}H",raw)
                repaired=[retile_word(w) for w in words]
                self.assertEqual([w&0xFC00 for w in words],
                                 [w&0xFC00 for w in repaired])
                self.assertNotIn(0x3003,repaired)
                self.assertNotIn(0x3C01,repaired)

if __name__=="__main__":unittest.main()
