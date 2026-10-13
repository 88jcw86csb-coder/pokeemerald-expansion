#!/usr/bin/env python3
"""Eryon League City and eight-fight qualifier tournament static regression.

Battle results / money penalties require emulator testing. This test protects
map connections, room ownership, badge gate, phase order, flag mapping and
restart-on-reentry, not real-time battle behavior.
"""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAPS = ["Eryon_CidadeDaLiga", "Eryon_LigaRecepcao",
        "Eryon_LigaClassificatoria", "Eryon_LigaRecuperacao"]


class EryonLeagueTournamentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.maps = {
            n: json.loads((ROOT / "data/maps" / n / "map.json").read_text(
                encoding="utf-8")) for n in MAPS
        }
        cls.layouts = {
            entry["id"]: entry for entry in json.loads(
                (ROOT / "data/layouts/layouts.json").read_text(
                    encoding="utf-8"))["layouts"]
        }

    def test_full_size_city_has_centered_league_entrance(self):
        city = self.maps["Eryon_CidadeDaLiga"]
        layout = self.layouts[city["layout"]]
        self.assertEqual((layout["width"], layout["height"]), (96, 72))
        self.assertEqual(city["warp_events"][1]["x"], 48)
        self.assertEqual(city["warp_events"][1]["y"], 36)
        self.assertEqual(city["warp_events"][0]["dest_map"],
                         "MAP_ERYON_CAMINHO_DA_LIGA")
        self.assertEqual(city["warp_events"][1]["dest_map"],
                         self.maps["Eryon_LigaRecepcao"]["id"])
        self.assertEqual(self.maps["Eryon_LigaRecepcao"]["warp_events"][0]["dest_map"],
                         city["id"])
        for data in self.maps.values():
            lay = self.layouts[data["layout"]]
            self.assertEqual((ROOT / lay["blockdata_filepath"]).stat().st_size,
                             lay["width"] * lay["height"] * 2)

    def test_eight_distinct_sprites_and_ordered_battles(self):
        hall = self.maps["Eryon_LigaClassificatoria"]
        objects = hall["object_events"]
        challengers = [x for x in objects if re.fullmatch(
            r"EryonLigaQual_EventScript_Fighter[1-8]", x["script"]
        )]
        self.assertEqual(len(challengers), 8)
        self.assertEqual(len({x["graphics_id"] for x in challengers}), 8)
        self.assertEqual(len({(x["x"], x["y"]) for x in challengers}), 8)
        script = (ROOT / "data/maps/Eryon_LigaClassificatoria/scripts.inc").read_text(
            encoding="utf-8"
        )
        for n in range(1, 9):
            with self.subTest(round=n):
                self.assertIn(
                    f"trainerbattle_single TRAINER_ERYON_QUALIFIER_{n}", script
                )
                self.assertIn(
                    f"EryonLigaQual_EventScript_Fighter{n}::", script
                )
                self.assertIn(f"setflag FLAG_ERYON_QUALIFIER_ROUND_{n}", script)
                self.assertIn(
                    f"cleartrainerflag TRAINER_ERYON_QUALIFIER_{n}", script
                )
                self.assertIn(
                    f"clearflag FLAG_ERYON_QUALIFIER_ROUND_{n}", script
                )
                if n > 1:
                    self.assertIn(
                        f"goto_if_unset FLAG_ERYON_QUALIFIER_ROUND_{n-1},"
                        " EryonLigaQual_EventScript_Locked", script
                    )
        self.assertIn("map_script MAP_SCRIPT_ON_TRANSITION", script)
        self.assertIn("goto_if_set FLAG_ERYON_QUALIFIED", script)
        self.assertIn("setflag FLAG_ERYON_QUALIFIED", script)
        self.assertIn("warp MAP_ERYON_LIGA_RECUPERACAO", script)
        # No walkable auto-warp from the lobby bypasses the registrar.
        self.assertEqual(len(hall["warp_events"]), 0)

    def test_badges_and_recovery_before_elite_four(self):
        lobby = (ROOT / "data/maps/Eryon_LigaRecepcao/scripts.inc").read_text(
            encoding="utf-8"
        )
        for n in range(1, 9):
            self.assertIn(f"goto_if_unset FLAG_BADGE0{n}_GET", lobby)
        self.assertIn("warp MAP_ERYON_LIGA_CLASSIFICATORIA", lobby)
        recovery = (ROOT / "data/maps/Eryon_LigaRecuperacao/scripts.inc").read_text(
            encoding="utf-8"
        )
        self.assertIn("special HealPlayerParty", recovery)
        self.assertIn("FLAG_ERYON_QUALIFIED", recovery)
        self.assertEqual(self.maps["Eryon_LigaRecuperacao"]["warp_events"], [])

    def test_eight_trainers_have_unique_ids_and_normal_money_loss(self):
        constants = (ROOT / "include/constants/opponents.h").read_text(
            encoding="utf-8"
        )
        parties = (ROOT / "src/data/trainers.party").read_text(
            encoding="utf-8"
        )
        for n in range(1, 9):
            with self.subTest(trainer=n):
                self.assertRegex(constants, rf"(?m)^#define\s+TRAINER_ERYON_QUALIFIER_{n}\s+{863+n}\s*$")
                self.assertIn(f"=== TRAINER_ERYON_QUALIFIER_{n} ===", parties)
        flags = (ROOT / "include/constants/flags.h").read_text(
            encoding="utf-8"
        )
        for n in range(1, 9):
            self.assertRegex(flags, rf"(?m)^#define\s+FLAG_ERYON_QUALIFIER_TRAINER_{n}\s+0x{0x2B+n:02X}\b")
            self.assertRegex(flags, rf"(?m)^#define\s+FLAG_ERYON_QUALIFIER_ROUND_{n}\s+0x{0x33+n:02X}\b")
        self.assertIn("FLAG_ERYON_QUALIFIED", flags)
        self.assertIn("(TRAINER_FLAGS_START + 864 - 1)", flags)
        engine = (ROOT / "src/battle_setup.c").read_text(
            encoding="utf-8"
        )
        self.assertIn("GetEryonTrainerFlagId", engine)
        self.assertIn("GetEryonTrainerFlagId(trainerId)", engine)
        # Use native trainer battle whiteout (money loss), not custom fake penalty.
        hall = (ROOT / "data/maps/Eryon_LigaClassificatoria/scripts.inc").read_text(
            encoding="utf-8"
        )
        self.assertIn("trainerbattle_single", hall)
        self.assertNotIn("dowildbattle", hall)


if __name__ == "__main__":
    unittest.main()
