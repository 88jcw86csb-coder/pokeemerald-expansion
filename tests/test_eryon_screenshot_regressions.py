"""Protect fixes for real Delta screenshot defects (bad sign tiles/old Elya).

This detects structural regressions. It does not declare source artwork
production-ready or replace emulator screenshots.
"""
from pathlib import Path
import json
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"tools"))
from eryon_terrain_visual_repair import retile_word, repair

class ScreenshotRegressions(unittest.TestCase):
    def test_bad_sign_must_never_be_used_as_stone(self):
        # Screenshot of route with horizontal sign stripes showed why
        # metatile 0x003 is not a terrain tile.
        self.assertEqual(retile_word(0x3003)&0x3ff,0x06c)
        self.assertEqual(retile_word(0x3001)&0x3ff,0x069)
        self.assertEqual(retile_word(0x3002)&0x3ff,0x01c)
        self.assertEqual(retile_word(0x3c01)&0x3ff,0x016)
        for v in (0x3001,0x3002,0x3003,0x3c01):
            self.assertEqual(retile_word(v)&0xfc00,v&0xfc00)

    def test_all_42_registered_maps_are_repaired_without_changing_collision(self):
        result=repair(write=False)
        self.assertEqual(result["region_maps"],42)
        self.assertEqual(result["collision_elevation"],"identical")
        self.assertEqual(len(result["maps"]),42)

    def test_final_build_repairs_terrain_after_terrain_generator(self):
        script=(ROOT/"tools/build_eryon.sh").read_text(encoding="utf-8")
        first=script.index("python3 tools/build_eryon_map_bins.py")
        repair_pos=script.index("python3 tools/eryon_terrain_visual_repair.py")
        compile_pos=script.index("make -j")
        self.assertLess(first,repair_pos)
        self.assertLess(repair_pos,compile_pos)
        self.assertIn("python3 tools/eryon_overworld_preview.py",script)

    def test_professor_references_real_custom_portrait_not_birch(self):
        generator=(ROOT/"tools/eryon_visual_assets.py").read_text(encoding="utf-8")
        self.assertIn("graphics/eryon_original/professor_elya.png",generator)
        self.assertTrue((ROOT/"graphics/eryon_original/professor_elya.png").exists())
        main=(ROOT/"src/main_menu.c").read_text(encoding="utf-8")
        self.assertIn("CreateTrainerSprite(TRAINER_PIC_ERYON_ELYA",main)
        self.assertNotIn("birchSpriteId = AddNewGameBirchObject(",main)
        self.assertIn("gTrainerFrontPic_EryonElya",(ROOT/"src/data/graphics/trainers.h").read_text(encoding="utf-8"))

if __name__=="__main__":
    unittest.main()
