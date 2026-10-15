"""Static regression checks for the Eryon League qualifying tournament.

Run from repository root:
    python3 -m unittest discover -s tests -p 'test_eryon_league_contract.py'

These tests check script structure only. They do not replace compilation or
in-game battle/save/whiteout tests.
"""
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
MAPS = ROOT / "data" / "maps"
QUAL = MAPS / "Eryon_LigaClassificatoria" / "scripts.inc"
RECOVER = MAPS / "Eryon_LigaRecuperacao" / "scripts.inc"
LOBBY = MAPS / "Eryon_LigaRecepcao" / "scripts.inc"
ELITE = MAPS / "Eryon_LigaEliteFour" / "scripts.inc"


def script_body(text, label):
    match = re.search(
        rf"(?m)^{re.escape(label)}::?\s*\n(.*?)(?=^[A-Za-z_][A-Za-z_0-9]*::?\s*$|\Z)",
        text,
        re.S | re.M,
    )
    if match is None:
        raise AssertionError(f"Missing event label: {label}")
    return match.group(1)


class EryonLeagueContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.qual = QUAL.read_text(encoding="utf-8")
        cls.recover = RECOVER.read_text(encoding="utf-8")
        cls.lobby = LOBBY.read_text(encoding="utf-8")
        cls.qual_map = json.loads((QUAL.parent / "map.json").read_text(encoding="utf-8"))
        cls.elite = ELITE.read_text(encoding="utf-8")

    def test_eight_npcs_and_distinct_script_entries(self):
        events = self.qual_map["object_events"]
        fighters = [
            e for e in events
            if e.get("script", "").startswith("EryonLigaQual_EventScript_Fighter")
        ]
        self.assertEqual(len(fighters), 8)
        self.assertEqual(
            {e["script"] for e in fighters},
            {f"EryonLigaQual_EventScript_Fighter{i}" for i in range(1, 9)},
        )
        self.assertEqual(len({(e["x"], e["y"]) for e in fighters}), 8)

    def test_progression_requires_previous_win(self):
        for i in range(1, 9):
            body = script_body(self.qual, f"EryonLigaQual_EventScript_Fighter{i}")
            self.assertIn(f"TRAINER_ERYON_QUALIFIER_{i}", body)
            self.assertIn(f"FLAG_ERYON_QUALIFIER_ROUND_{i}", body)
            self.assertIn(f"EryonLigaQual_EventScript_Win{i}", body)
            if i > 1:
                self.assertIn(
                    f"goto_if_unset FLAG_ERYON_QUALIFIER_ROUND_{i-1}, "
                    "EryonLigaQual_EventScript_Locked",
                    body,
                )
            win = script_body(self.qual, f"EryonLigaQual_EventScript_Win{i}")
            self.assertIn(f"setflag FLAG_ERYON_QUALIFIER_ROUND_{i}", win)

    def test_reentry_resets_unqualified_run_and_trainer_flags(self):
        body = script_body(self.qual, "EryonLigaQual_OnTransition")
        self.assertIn("goto_if_set FLAG_ERYON_QUALIFIED", body)
        for i in range(1, 9):
            self.assertIn(f"clearflag FLAG_ERYON_QUALIFIER_ROUND_{i}", body)
            self.assertIn(f"cleartrainerflag TRAINER_ERYON_QUALIFIER_{i}", body)

    def test_eighth_win_unlocks_recovery(self):
        body = script_body(self.qual, "EryonLigaQual_EventScript_Win8")
        self.assertIn("setflag FLAG_ERYON_QUALIFIED", body)
        self.assertIn("warp MAP_ERYON_LIGA_RECUPERACAO", body)
        heal = script_body(self.recover, "EryonLigaRecover_EventScript_Heal")
        self.assertIn("special HealPlayerParty", heal)
        self.assertIn("goto_if_unset FLAG_ERYON_QUALIFIED", heal)

    def test_registration_requires_all_badges(self):
        body = script_body(self.lobby, "EryonLigaLobby_EventScript_Register")
        for i in range(1, 9):
            self.assertIn(f"FLAG_BADGE{i:02d}_GET", body)
        self.assertIn("warp MAP_ERYON_LIGA_CLASSIFICATORIA", body)

    def test_elite_reentry_resets_both_progress_and_trainer_flags(self):
        body = script_body(self.elite, "EryonLigaElite_OnTransition")
        # A completed championship is persistent and must not be cleared.
        guard = "goto_if_set FLAG_ERYON_CHAMPION_CROWNED"
        self.assertIn(guard, body)
        self.assertLess(body.index(guard),
                        body.index("clearflag FLAG_ERYON_ELITE_TRAINER_1_DEFEATED"))
        # Losing or voluntarily leaving the gallery must reset EVERY round.
        for i in range(1, 5):
            self.assertIn(f"clearflag FLAG_ERYON_ELITE_TRAINER_{i}_DEFEATED", body)
            self.assertIn(f"cleartrainerflag TRAINER_ERYON_ELITE_{i}", body)
        self.assertIn("clearflag FLAG_ERYON_CHAMPION_TRAINER_DEFEATED", body)
        self.assertIn("cleartrainerflag TRAINER_ERYON_CHAMPION", body)
        self.assertNotIn("clearflag FLAG_ERYON_QUALIFIED", body)
        self.assertNotIn("clearflag FLAG_ERYON_CHAMPION_CROWNED", body)
        self.assertNotIn("FLAG_ERYON_QUALIFIER_ROUND_", body)

    def test_elite_rounds_still_require_order_and_confirm_champion(self):
        for i in range(1, 5):
            body = script_body(self.elite, f"EryonLigaElite_EventScript_Win{i}")
            self.assertIn(f"setflag FLAG_ERYON_ELITE_TRAINER_{i}_DEFEATED", body)
            if i > 1:
                fighter = ["", "Aria", "Bastian", "Selene", "Darius"][i]
                gate = script_body(self.elite, f"EryonLigaElite_EventScript_{fighter}")
                self.assertIn(
                    f"goto_if_unset FLAG_ERYON_ELITE_TRAINER_{i-1}_DEFEATED",
                    gate,
                )
        champion = script_body(self.elite, "EryonLigaElite_EventScript_Champion")
        self.assertIn("goto_if_unset FLAG_ERYON_ELITE_TRAINER_4_DEFEATED", champion)
        win = script_body(self.elite, "EryonLigaElite_EventScript_Win5")
        self.assertIn("setflag FLAG_ERYON_CHAMPION_TRAINER_DEFEATED", win)
        self.assertIn("setflag FLAG_ERYON_CHAMPION_CROWNED", win)

    def test_trainer_flag_mapping_is_explicit(self):
        battle_setup = (ROOT / "src" / "battle_setup.c").read_text(encoding="utf-8")
        self.assertIn("static u16 GetEryonTrainerFlagId(u16 trainerId)", battle_setup)
        self.assertIn("FLAG_ERYON_QUALIFIER_TRAINER_1 + trainerId", battle_setup)
        self.assertIn("return GetEryonTrainerFlagId(TRAINER_BATTLE_PARAM.opponentA)", battle_setup)


if __name__ == "__main__":
    unittest.main()
