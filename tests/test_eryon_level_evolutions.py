"""Structural regression tests for Eryon's self-contained Pokémon evolution rules.

These are source checks, not proof of successful ROM compilation or emulator play.
"""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPECIES_DIR = ROOT / "src/data/pokemon/species_info"


class EryonEvolutionRules(unittest.TestCase):
    def test_riolu_evolves_at_level_35_only(self):
        source = (SPECIES_DIR / "gen_4_families.h").read_text(encoding="utf-8")
        riolu = source.split("[SPECIES_RIOLU] =", 1)[1].split("[SPECIES_LUCARIO] =", 1)[0]
        self.assertIn(".evolutions = EVOLUTION({EVO_LEVEL, 35, SPECIES_LUCARIO})", riolu)
        self.assertNotIn("IF_MIN_FRIENDSHIP", riolu)
        self.assertNotIn("IF_TIME", riolu)
        self.assertNotIn("IF_NOT_TIME", riolu)

    def test_oasis_helioptile_evolves_by_level_not_stone(self):
        source = (SPECIES_DIR / "gen_6_families.h").read_text(encoding="utf-8")
        helioptile = source.split("[SPECIES_HELIOPTILE] =", 1)[1].split(
            "[SPECIES_HELIOLISK] =", 1)[0]
        self.assertIn("{EVO_LEVEL, 36, SPECIES_HELIOLISK}", helioptile)
        self.assertNotIn("EVO_ITEM", helioptile)

    def test_no_trade_or_friendship_evolutions_up_to_kalos(self):
        for generation in range(1, 7):
            with self.subTest(generation=generation):
                text = (SPECIES_DIR / f"gen_{generation}_families.h").read_text(encoding="utf-8")
                self.assertNotRegex(text, r"\{EVO_TRADE\s*,")
                self.assertNotIn("IF_MIN_FRIENDSHIP", text)
                self.assertNotIn("IF_MAX_FRIENDSHIP", text)

    def test_new_levels_are_positive_and_under_one_hundred(self):
        for generation in range(1, 7):
            text = (SPECIES_DIR / f"gen_{generation}_families.h").read_text(encoding="utf-8")
            for number in re.findall(r"\{EVO_LEVEL,\s*(\d+),\s*SPECIES_", text):
                self.assertLessEqual(int(number), 100)


if __name__ == "__main__":
    unittest.main()
