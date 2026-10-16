"""Do not regress to amateur rectangles, missing poses or palette mismatch.

Acceptance is static data integrity; this does NOT certify artistic originality.
"""
from pathlib import Path
import struct
import unittest
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"tools"))
from eryon_native_overworld import ACTIONS,png_info,source_palette

class EryonNativeFieldArt(unittest.TestCase):
    def test_hero_art_uses_complete_native_gba_animation_frames(self):
        for native,name in (("brendan","eryon_hero"),("may","eryon_hero_f")):
            for action,dimensions in ACTIONS.items():
                with self.subTest(player=name,action=action):
                    base=ROOT/"graphics/object_events/pics/people"
                    expected=(base/native/(action+".png")).read_bytes()
                    actual=(base/name/(action+".png")).read_bytes()
                    self.assertEqual(actual,expected)
                    self.assertEqual(png_info(base/name/(action+".png")),dimensions)

    def test_male_and_female_use_distinct_compatible_palettes(self):
        graphics=(ROOT/"src/data/object_events/object_event_graphics.h").read_text()
        self.assertIn('palettes/eryon_hero.pal"',graphics)
        self.assertIn('palettes/eryon_hero_f.pal"',graphics)
        for native,hero in (("brendan","eryon_hero"),("may","eryon_hero_f")):
            source=source_palette(native)
            base=ROOT/"graphics/object_events/palettes"
            for suffix in (".pal","_reflection.pal"):
                path=base/(hero+suffix)
                lines=path.read_text().splitlines()
                self.assertEqual(lines[:3],["JASC-PAL","0100","16"])
                self.assertEqual(len(lines),19)
            actual=[tuple(map(int,s.split())) for s in (base/(hero+".pal")).read_text().splitlines()[3:]]
            self.assertEqual(actual[0],source[0])
            self.assertEqual(len(actual),16)

    def test_build_and_visual_preview_use_final_field_art(self):
        script=(ROOT/"tools/build_eryon.sh").read_text()
        self.assertLess(script.index("python3 tools/eryon_visual_assets.py"),
                        script.index("python3 tools/eryon_native_overworld.py"))
        self.assertLess(script.index("python3 tools/eryon_native_overworld.py"),
                        script.index("make -j"))

if __name__=="__main__":
    unittest.main()
