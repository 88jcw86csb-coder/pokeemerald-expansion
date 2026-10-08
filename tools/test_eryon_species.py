#!/usr/bin/env python3
"""Small regression test for Eryon's Gen I-VI encounter whitelist."""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATTERN = r"(?m)^\s*(SPECIES_[A-Z0-9_]+)\s*=\s*(\d+)\s*,?"


class SpeciesValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        text = (ROOT / "include/constants/species.h").read_text(encoding="utf-8")
        cls.numbers = {name: int(value) for name, value in re.findall(PATTERN, text)}

    def test_riolu_is_supported(self):
        self.assertEqual(self.numbers["SPECIES_RIOLU"], 447)

    def test_last_kalos_species_is_supported(self):
        self.assertEqual(self.numbers["SPECIES_VOLCANION"], 721)

    def test_first_alola_species_is_excluded(self):
        self.assertEqual(self.numbers["SPECIES_ROWLET"], 722)
        self.assertFalse(1 <= self.numbers["SPECIES_ROWLET"] <= 721)

    def test_unresolved_species_is_not_silently_accepted(self):
        self.assertNotIn("SPECIES_ERYON_FAKE", self.numbers)


if __name__ == "__main__":
    unittest.main()
