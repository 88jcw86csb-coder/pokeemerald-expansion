"""Static contracts for the optional Eclipse resolution at Drakonia."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CITY = ROOT / "data/maps/Eryon_Drakonia"
FLAGS = ROOT / "include/constants/flags.h"


class EclipseFinaleContract(unittest.TestCase):
    def test_finale_is_registered_once_at_east_terminal(self):
        map_data = json.loads((CITY / "map.json").read_text())
        events = [e for e in map_data["bg_events"]
                  if e["script"] == "EryonDrakonia_EventScript_EclipseFinale"]
        self.assertEqual([(e["x"], e["y"]) for e in events], [(55, 28)])
        coordinates = [(e["x"], e["y"]) for e in
                       (map_data["object_events"] + map_data["bg_events"] + map_data["warp_events"])]
        self.assertEqual(len(coordinates), len(set(coordinates)))

    def test_finale_requires_all_three_existing_accomplishments(self):
        script = (CITY / "scripts.inc").read_text()
        entry = script.split("EryonDrakonia_EventScript_EclipseFinale::", 1)[1].split(
            "EryonDrakonia_EventScript_EclipseFinaleAgent::", 1)[0]
        conditions = ["FLAG_ERYON_DRAKONIA_ECLIPSE_DEFEATED",
                      "FLAG_ERYON_STAR_GROTTO_RELAY_DISABLED",
                      "FLAG_ERYON_ECLIPSE_EVIDENCE_REPORTED"]
        for flag in conditions:
            self.assertIn("goto_if_unset " + flag, entry)
        self.assertIn("MSGBOX_YESNO", entry)
        self.assertIn("setflag FLAG_ERYON_ECLIPSE_NETWORK_SHUT_DOWN", entry)
        self.assertLess(entry.index("MSGBOX_YESNO"),
                        entry.index("setflag FLAG_ERYON_ECLIPSE_NETWORK_SHUT_DOWN"))
        self.assertNotIn("FLAG_BADGE", entry)
        self.assertNotIn("warp ", entry)

    def test_finale_flag_and_city_epilogue(self):
        constants = FLAGS.read_text()
        self.assertIn("#define FLAG_ERYON_ECLIPSE_NETWORK_SHUT_DOWN", constants)
        script = (CITY / "scripts.inc").read_text()
        sage = script.split("EryonDrakonia_EventScript_Sage::", 1)[1].split(
            "EryonDrakonia_EventScript_SageClue::", 1)[0]
        self.assertIn("FLAG_ERYON_ECLIPSE_NETWORK_SHUT_DOWN", sage)
        self.assertIn("EryonDrakonia_EventScript_SageNetworkRestored::", script)


    def test_league_capital_resonance_board_is_unique_and_walkable(self):
        city = json.loads((ROOT / "data/maps/Eryon_CidadeDaLiga/map.json").read_text())
        events = [e for e in city["bg_events"]
                  if e["script"] == "EryonCidadeLiga_EventScript_ResonanceBoard"]
        self.assertEqual([(e["x"], e["y"]) for e in events], [(50, 39)])
        positions = [(e["x"], e["y"]) for e in (
            city["object_events"] + city["bg_events"] + city["warp_events"])]
        self.assertEqual(len(positions), len(set(positions)))
        terrain = (ROOT / "docs/eryon/liga_eryon_terrain_plan.txt").read_text().splitlines()[3:]
        self.assertEqual(terrain[39][50], ".")
        self.assertTrue(any(terrain[y][x] == "."
                            for x, y in [(49, 39), (51, 39), (50, 38), (50, 40)]))
        self.assertEqual([(w["x"], w["y"]) for w in city["warp_events"]],
                         [(0, 36), (48, 36)])

    def test_league_capital_reacts_to_eclipse_shutdown_without_gating_tournament(self):
        source = (ROOT / "data/maps/Eryon_CidadeDaLiga/scripts.inc").read_text()
        for entry in ("ReporterPeace", "ReporterChampionPeace", "InvestigatorPeace",
                      "ResonanceDelegatePeace", "ResonanceDelegateChampionPeace"):
            self.assertIn("EryonCidadeLiga_EventScript_" + entry + "::", source)
        investigator = source.split("EryonCidadeLiga_EventScript_Investigator::", 1)[1].split(
            "EryonCidadeLiga_EventScript_InvestigatorQualified::", 1)[0]
        self.assertLess(investigator.index("EryonCidadeLiga_EventScript_InvestigatorScoutRewardCheck"),
                        investigator.index("EryonCidadeLiga_EventScript_InvestigatorPeace"))
        board = source.split("EryonCidadeLiga_EventScript_ResonanceBoard::", 1)[1]
        self.assertIn("goto_if_set FLAG_ERYON_ECLIPSE_EVIDENCE_REPORTED", board)
        self.assertIn("goto_if_set FLAG_ERYON_ECLIPSE_NETWORK_SHUT_DOWN", board)
        self.assertIn("goto_if_set FLAG_ERYON_CHAMPION_CROWNED", board)
        self.assertNotIn("setflag ", board)
        self.assertNotIn("warp ", board)
        self.assertNotIn("trainerbattle", board)
        lobby = (ROOT / "data/maps/Eryon_LigaRecepcao/scripts.inc").read_text()
        self.assertIn("warp MAP_ERYON_LIGA_CLASSIFICATORIA", lobby)
        self.assertNotIn("FLAG_ERYON_ECLIPSE_NETWORK_SHUT_DOWN", lobby)


if __name__ == "__main__":
    unittest.main()
