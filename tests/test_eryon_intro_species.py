"""Eryon's intro should reveal its actual starter, not Emerald's Lotad."""
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]

class EryonIntroSpeciesTest(unittest.TestCase):
    def test_opening_professor_displays_riolu(self):
        code=(ROOT/"src/main_menu.c").read_text(encoding="utf-8")
        self.assertIn("CreateMonPicSprite_Affine(SPECIES_RIOLU",code)
        self.assertNotIn("CreateMonPicSprite_Affine(SPECIES_LOTAD",code)

    def test_intro_professor_is_elya_and_not_birch(self):
        text=(ROOT/"data/text/birch_speech.inc").read_text(encoding="utf-8")
        self.assertIn("Meu nome e ELYA",text)
        gfx=(ROOT/"src/data/graphics/trainers.h").read_text(encoding="utf-8")
        self.assertIn("gTrainerFrontPic_EryonElya",gfx)
        source=(ROOT/"src/main_menu.c").read_text(encoding="utf-8")
        self.assertIn("CreateTrainerSprite(TRAINER_PIC_ERYON_ELYA",source)

if __name__=="__main__":
    unittest.main()
