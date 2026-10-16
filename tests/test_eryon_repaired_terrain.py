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

    def test_all_42_region_maps_have_no_used_storefront_fragment_as_stone(self):
        names=json.loads((ROOT/"data/maps/map_groups.json").read_text())["gMapGroup_Eryon"]
        layouts={x["id"]:x for x in json.loads((ROOT/"data/layouts/layouts.json").read_text())["layouts"]}
        for name in names:
            with self.subTest(map=name):
                info=json.loads((ROOT/"data/maps"/name/"map.json").read_text())
                layout=layouts[info["layout"]]
                raw=(ROOT/layout["blockdata_filepath"]).read_bytes()
                words=struct.unpack(f"<{len(raw)//2}H",raw)
                self.assertNotIn(0x3003,words)
                self.assertNotIn(0x3C01,words)
                self.assertTrue(any((x&0xFC00)==0x3000 for x in words))

    def test_region_repair_is_idempotent_on_all_maps(self):
        originals={}
        try:
            names=json.loads((ROOT/"data/maps/map_groups.json").read_text())["gMapGroup_Eryon"]
            layouts={x["id"]:x for x in json.loads((ROOT/"data/layouts/layouts.json").read_text())["layouts"]}
            for name in names:
                info=json.loads((ROOT/"data/maps"/name/"map.json").read_text())
                path=ROOT/layouts[info["layout"]]["blockdata_filepath"]
                originals[path]=path.read_bytes()
            repair()
            for path,data in originals.items():
                self.assertEqual(path.read_bytes(),data,path)
        finally:
            for path,data in originals.items():
                path.write_bytes(data)

if __name__=="__main__":unittest.main()
