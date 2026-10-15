"""Verify map-script -> trainer/flag/species linkage across every registered Eryon map.

The engine and trainer-party parser are not executed by this source audit.
"""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return (ROOT / path).read_text(encoding="utf-8")


def scripts():
    worlds = json.loads(read("data/maps/map_groups.json"))["gMapGroup_Eryon"]
    for name in worlds:
        yield name, read("data/maps/" + name + "/scripts.inc")


class EryonScriptLinkage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.script_sources = list(scripts())
        cls.opponents = read("include/constants/opponents.h")
        cls.party = read("src/data/trainers.party")
        cls.flags = read("include/constants/flags.h")
        cls.species = read("include/constants/species.h")

    def test_all_registered_maps_are_included(self):
        self.assertEqual(len(self.script_sources), 42)
        self.assertEqual(len({name for name, _ in self.script_sources}), 42)

    def test_every_scripted_trainer_has_constant_and_party(self):
        valid = set(re.findall(
            r"(?m)^#define\s+(TRAINER_[A-Z0-9_]+)\b", self.opponents))
        teams = set(re.findall(
            r"(?m)^=== (TRAINER_[A-Z0-9_]+) ===$", self.party))
        inspected = 0
        for name, source in self.script_sources:
            for trainer in re.findall(
                r"(?m)^\s*trainerbattle_single\s+(TRAINER_[A-Z0-9_]+)\b",
                source,
            ):
                with self.subTest(map=name, trainer=trainer):
                    self.assertIn(trainer, valid)
                    self.assertIn(trainer, teams)
                inspected += 1
        self.assertGreaterEqual(inspected, 25)

    def test_every_persistent_eryon_script_flag_is_defined(self):
        defined = set(re.findall(
            r"(?m)^#define\s+(FLAG_ERYON_[A-Z0-9_]+)\b", self.flags))
        inspected = 0
        for name, source in self.script_sources:
            for flag in re.findall(
                r"(?m)^\s*(?:setflag|clearflag|goto_if_set|goto_if_unset)"
                r"\s+(FLAG_ERYON_[A-Z0-9_]+)\b",
                source,
            ):
                with self.subTest(map=name, flag=flag):
                    self.assertIn(flag, defined)
                inspected += 1
        self.assertGreaterEqual(inspected, 250)

    def test_scripted_wild_species_and_levels_are_valid(self):
        defined = set(re.findall(
            r"(?m)^\s*(SPECIES_[A-Z0-9_]+)\s*=", self.species))
        inspected = 0
        for name, source in self.script_sources:
            for species, level in re.findall(
                r"(?m)^\s*setwildbattle\s+(SPECIES_[A-Z0-9_]+)"
                r"\s*,\s*(\d+)\b",
                source,
            ):
                with self.subTest(map=name, species=species, level=level):
                    self.assertIn(species, defined)
                    self.assertGreaterEqual(int(level), 1)
                    self.assertLessEqual(int(level), 100)
                inspected += 1
        self.assertGreaterEqual(inspected, 5)

    def test_custom_trainer_ids_do_not_overlap(self):
        pairs = re.findall(
            r"(?m)^#define\s+(TRAINER_ERYON_[A-Z0-9_]+)\s+(\d+)\b",
            self.opponents,
        )
        self.assertGreaterEqual(len(pairs), 20)
        ids = [int(value) for _, value in pairs]
        self.assertEqual(len(ids), len(set(ids)))


if __name__ == "__main__":
    unittest.main()
