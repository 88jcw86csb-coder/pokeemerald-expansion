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

    def test_echo_village_witness_and_binary_are_physically_accessible(self):
        import json
        import struct
        plan = village("aldeia_dos_ecos")
        self.assertIn((21, 20), reachable(plan))
        self.assertEqual(plan[20][21], ".")
        world = json.loads((ROOT / "data/maps/Eryon_AldeiaDosEcos/map.json").read_text())
        self.assertTrue(any(e["script"]=="EryonAldeia_EventScript_Witness"
                            and (e["x"],e["y"])==(21,20)
                            for e in world["object_events"]))
        from build_eryon_map_bins import SPECS, compile_plan
        self.assertNotIn("aldeia_dos_ecos", SPECS)
        plan_path = ROOT / "docs/eryon/vilas/aldeia_dos_ecos_village_plan.txt"
        tile = {"#":0x3C01, ".":0x3001, ",":0x3002, ":":0x3003,
                **dict.fromkeys("PCMHI",0x3001)}
        expected = compile_plan(plan_path,tile,width=36,height=30)
        self.assertEqual((ROOT/"data/layouts/Eryon_AldeiaDosEcos/map.bin").read_bytes(),expected)
        self.assertEqual(struct.unpack_from("<H",expected,2*(20*36+21))[0],0x3001)


if __name__=="__main__":
    unittest.main()
