#!/usr/bin/env python3
"""Regression checks for Eryon's nine new wild habitats and river side quest.

Structural checks only: collision-free blocks are not proof that GBA
metatile behavior actually triggers random encounters. Test on Delta.
"""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {
    "MAP_ERYON_ROTA03": (11, 16, {"MAREEP", "ELECTRIKE", "TAILLOW", "MAGNEMITE", "HELIOPTILE", "EMOLGA"}),
    "MAP_ERYON_SERRA_DOS_CRISTAIS": (15, 21, {"GEODUDE", "ROGGENROLA", "ZUBAT", "ARON", "SABLEYE", "CARBINK"}),
    "MAP_ERYON_PASSAGEM_ROCHOSA": (19, 25, {"MACHOP", "ONIX", "WOOBAT", "NOSEPASS", "MAWILE", "AXEW"}),
    "MAP_ERYON_ESTRADA_ORIENTAL": (23, 29, {"SANDILE", "NUMEL", "DODUO", "TRAPINCH", "SKIDDO", "ABSOL"}),
    "MAP_ERYON_VALE_DOS_VENTOS": (27, 33, {"HOPPIP", "SWABLU", "YANMA", "GLIGAR", "HAWLUCHA", "NOIBAT"}),
    "MAP_ERYON_ROTA_DAS_CACHOEIRAS": (30, 36, {"POLIWAG", "BUIZEL", "LOTAD", "CORPHISH", "CLAUNCHER", "DUCKLETT"}),
    "MAP_ERYON_DESERTO_DE_SOLARIS": (34, 40, {"SANDSHREW", "CACNEA", "DWEBBLE", "SIGILYPH", "HELIOPTILE", "GIBLE"}),
    "MAP_ERYON_FLORESTA_DOS_ECOS": (38, 44, {"PHANTUMP", "PUMPKABOO", "FOONGUS", "ZORUA", "KARRABLAST", "LARVESTA"}),
    "MAP_ERYON_CAMINHO_DA_LIGA": (44, 52, {"GOLBAT", "GRAVELER", "GURDURR", "ZWEILOUS", "GABITE", "BAGON"}),
}
OPENING = {
    "MAP_ERYON_ROTA01", "MAP_ERYON_BOSQUE_DE_LUMINA", "MAP_ERYON_ROTA02"
}
FLAG_SAMPLE = "FLAG_ERYON_RIVER_SAMPLE_RECORDED"
FLAG_REWARD = "FLAG_ERYON_RIVER_SAMPLE_REWARD_CLAIMED"
STORY = (
    ("Eryon_RotaDasCachoeiras", "bg_events", "EryonCachoeiras_EventScript_SamplingStation", 29, 22),
    ("Eryon_VilaDasAguas", "object_events", "EryonAguas_EventScript_RiverResearcher", 20, 14),
    ("Eryon_Ignivar", "bg_events", "EryonIgnivar_EventScript_RiverTransportBoard", 42, 28),
)


class EryonWildAndRiverTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        wild = json.loads((ROOT / "src/data/wild_encounters.json").read_text(encoding="utf-8"))
        cls.group = next(x for x in wild["wild_encounter_groups"] if x["label"] == "gWildMonHeaders")
        cls.by_map = {e["map"]: e for e in cls.group["encounters"]}
        cls.species = dict(
            (key, int(value)) for key, value in re.findall(
                r"(?m)^\s*(SPECIES_[A-Z0-9_]+)\s*=\s*(\d+)\s*,?",
                (ROOT / "include/constants/species.h").read_text(encoding="utf-8")
            )
        )

    def test_nine_new_land_tables_are_unique_and_balanced(self):
        # Vanilla groups intentionally reuse maps for alternate game versions.
        # Eryon itself must never duplicate a map header or encounter label.
        eryon_entries = [e for e in self.group["encounters"]
                         if e["map"].startswith("MAP_ERYON_")]
        all_maps = [e["map"] for e in eryon_entries]
        labels = [e["base_label"] for e in eryon_entries]
        self.assertEqual(len(all_maps), len(set(all_maps)), "Duplicate encounter map")
        self.assertEqual(len(labels), len(set(labels)), "Duplicate encounter base label")
        self.assertTrue(OPENING <= self.by_map.keys())
        self.assertEqual(len(self.group["fields"][0]["encounter_rates"]), 12)
        for map_id, (low, high, expected) in EXPECTED.items():
            with self.subTest(map=map_id):
                table = self.by_map[map_id]["land_mons"]
                self.assertGreaterEqual(table["encounter_rate"], 10)
                self.assertLessEqual(table["encounter_rate"], 30)
                self.assertEqual(len(table["mons"]), 12)
                actual = set()
                for slot in table["mons"]:
                    species = slot["species"]
                    actual.add(species.removeprefix("SPECIES_"))
                    self.assertIn(species, self.species)
                    self.assertLessEqual(self.species[species], 721)
                    self.assertGreaterEqual(slot["min_level"], low)
                    self.assertLessEqual(slot["max_level"], high)
                    self.assertLessEqual(slot["min_level"], slot["max_level"])
                self.assertEqual(actual, expected)
                self.assertEqual(table["mons"][-1]["max_level"], high)

    def test_river_quest_flags_use_reserved_save_slots(self):
        header = (ROOT / "include/constants/flags.h").read_text(encoding="utf-8")
        for label, word in ((FLAG_SAMPLE, "0x4A0"), (FLAG_REWARD, "0x4A1")):
            self.assertRegex(header, rf"(?m)^#define\s+{label}\s+{word}\b")
        self.assertNotIn("#define FLAG_UNUSED_0x4A0", header)
        self.assertNotIn("#define FLAG_UNUSED_0x4A1", header)

    def test_story_landmarks_are_registered_and_collision_free(self):
        layouts = json.loads((ROOT / "data/layouts/layouts.json").read_text(encoding="utf-8"))
        by_id = {x["id"]: x for x in layouts["layouts"]}
        for name, kind, symbol, x, y in STORY:
            with self.subTest(map=name):
                folder = ROOT / "data/maps" / name
                info = json.loads((folder / "map.json").read_text(encoding="utf-8"))
                located = [e for e in info[kind] if e["script"] == symbol]
                self.assertEqual(len(located), 1)
                self.assertEqual((located[0]["x"], located[0]["y"]), (x, y))
                script = (folder / "scripts.inc").read_text(encoding="utf-8")
                self.assertIn(symbol + "::", script)
                layout = by_id[info["layout"]]
                raw = (ROOT / layout["blockdata_filepath"]).read_bytes()
                idx = 2 * (y * layout["width"] + x)
                block = int.from_bytes(raw[idx:idx+2], "little")
                self.assertEqual(block & 0x0C00, 0, "Blocked quest event tile")

    def test_sample_is_optional_and_saved_once(self):
        route = (ROOT / "data/maps/Eryon_RotaDasCachoeiras/scripts.inc").read_text(encoding="utf-8")
        self.assertIn("goto_if_set " + FLAG_SAMPLE, route)
        self.assertIn("goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND", route)
        self.assertIn("MSGBOX_YESNO", route)
        offer = route.split("EryonCachoeiras_EventScript_SamplingOffer::", 1)[1]
        offer = offer.split("EryonCachoeiras_EventScript_SamplingDecline::", 1)[0]
        self.assertIn("setflag " + FLAG_SAMPLE, offer)
        self.assertIn("goto_if_eq VAR_RESULT, NO", offer)

    def test_mystic_water_is_claimed_only_after_successful_inventory_add(self):
        village = (ROOT / "data/maps/Eryon_VilaDasAguas/scripts.inc").read_text(encoding="utf-8")
        check = village.split("EryonAguas_EventScript_RiverResearcher::", 1)[1]
        check = check.split("EryonAguas_EventScript_RiverResearcherWaiting::", 1)[0]
        self.assertIn("goto_if_unset " + FLAG_SAMPLE, check)
        self.assertIn("goto_if_set " + FLAG_REWARD, check)
        self.assertIn("giveitem ITEM_MYSTIC_WATER", check)
        self.assertLess(check.index("giveitem ITEM_MYSTIC_WATER"),
                        check.index("goto_if_eq VAR_RESULT, FALSE"))
        self.assertLess(check.index("goto_if_eq VAR_RESULT, FALSE"),
                        check.index("setflag " + FLAG_REWARD))
        city = (ROOT / "data/maps/Eryon_Ignivar/scripts.inc").read_text(encoding="utf-8")
        self.assertIn("goto_if_set " + FLAG_SAMPLE, city)


if __name__ == "__main__":
    unittest.main()
