"""Guard the five original battle portraits in Eryon's League.

Only trainer portraits change. Teams, levels, flags, map scripts, and the
original eight gym leader identities remain independent.
"""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
CAST = {
    "TRAINER_ERYON_ELITE_1": "Aria",
    "TRAINER_ERYON_ELITE_2": "Bastian",
    "TRAINER_ERYON_ELITE_3": "Selene",
    "TRAINER_ERYON_ELITE_4": "Darius",
    "TRAINER_ERYON_CHAMPION": "Aurelio",
}


class EryonLeaguePortraitContract(unittest.TestCase):
    def test_all_five_have_dedicated_gba_graphic_references(self):
        party = (ROOT/"src/data/trainers.party").read_text(encoding="utf-8")
        enums = (ROOT/"include/constants/trainers.h").read_text(encoding="utf-8")
        graphics = (ROOT/"src/data/graphics/trainers.h").read_text(encoding="utf-8")
        for trainer,name in CAST.items():
            with self.subTest(name=name):
                section = party.split(f"=== {trainer} ===",1)[1].split("\n===",1)[0]
                self.assertIn(f"Pic: Eryon {name}",section)
                self.assertGreaterEqual(len(re.findall(r"(?m)^Level: \d+",section)),4)
                macro = "TRAINER_PIC_ERYON_"+name.upper()
                self.assertIn(f"    {macro},",enums)
                self.assertIn(f"    [{macro}] =",graphics)
                self.assertIn(f"gTrainerFrontPic_Eryon{name}",graphics)
                self.assertIn(f"gTrainerPalette_Eryon{name}",graphics)
                self.assertIn(f"front_pics/eryon_{name.lower()}.png",graphics)
        self.assertIn("Name: AURELIO",party)
        self.assertIn("TRAINER_PIC_COUNT,",enums)


if __name__=="__main__":
    unittest.main()
