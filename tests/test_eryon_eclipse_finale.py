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


    def test_eclipse_peace_reaches_cave_road_and_mountain_village(self):
        cave = (ROOT / "data/maps/Eryon_GrutaDasEstrelas/scripts.inc").read_text()
        road = (ROOT / "data/maps/Eryon_CaminhoDaLiga/scripts.inc").read_text()
        pico = (ROOT / "data/maps/Eryon_VilaDoPico/scripts.inc").read_text()
        for script, branch in (
            (cave, "EryonEstrelas_EventScript_AstronomerPeace"),
            (cave, "EryonEstrelas_EventScript_ArchivistPeace"),
            (road, "EryonLigaCaminho_EventScript_ScoutWitnessPeace"),
            (pico, "EryonPico_EventScript_NoticeAfterPeace"),
        ):
            self.assertIn("goto_if_set FLAG_ERYON_ECLIPSE_NETWORK_SHUT_DOWN, " + branch, script)
            self.assertEqual(script.count(branch + "::"), 1)
        for script, branch in (
            (cave, "EryonEstrelas_EventScript_AstronomerChampionPeace"),
            (road, "EryonLigaCaminho_EventScript_ScoutWitnessChampionPeace"),
        ):
            self.assertIn("goto_if_set FLAG_ERYON_ECLIPSE_NETWORK_SHUT_DOWN, " + branch, script)
            self.assertIn(branch + "::", script)
        # Old prerequisites still decide the finale, and no earlier progress
        # flag is changed by these new, informational epilogue branches.
        for script, branch in (
            (cave, "EryonEstrelas_EventScript_ArchivistPeace"),
            (road, "EryonLigaCaminho_EventScript_ScoutWitnessPeace"),
            (pico, "EryonPico_EventScript_NoticeAfterPeace"),
        ):
            content = script.split(branch + "::", 1)[1].split("\n\tend", 1)[0]
            self.assertNotIn("setflag ", content)
            self.assertNotIn("trainerbattle", content)
            self.assertNotIn("warp ", content)



    def test_eclipse_finale_returns_home_to_elya_kael_and_first_forest(self):
        home = (ROOT / "data/maps/Eryon_VilaAurora/scripts.inc").read_text()
        forest = (ROOT / "data/maps/Eryon_BosqueDeLumina/scripts.inc").read_text()
        verd = (ROOT / "data/maps/Eryon_Verdelume/scripts.inc").read_text()
        for source, from_label, to_label in (
            (home, "EryonVilaAurora_EventScript_ElyaAfterStarter",
             "EryonVilaAurora_EventScript_ElyaAfterEclipse"),
            (home, "EryonVilaAurora_EventScript_VillageNotice",
             "EryonVilaAurora_EventScript_VillageNoticePeace"),
            (forest, "EryonBosque_EventScript_AncientStone",
             "EryonBosque_EventScript_StoneRestored"),
            (verd, "EryonVerdelume_EventScript_KaelAfterBattle",
             "EryonVerdelume_EventScript_KaelAfterPeace"),
        ):
            script = source.split(from_label + "::", 1)[1].split("\n\tend", 1)[0]
            self.assertIn("goto_if_set FLAG_ERYON_ECLIPSE_NETWORK_SHUT_DOWN, "
                          + to_label, script)
            self.assertEqual(source.count(to_label + "::"), 1)
            epilogue = source.split(to_label + "::", 1)[1].split("\n\tend", 1)[0]
            self.assertNotIn("setflag ", epilogue)
            self.assertNotIn("trainerbattle", epilogue)
            self.assertNotIn("\n\twarp ", epilogue)
        self.assertIn("goto EryonVilaAurora_EventScript_ElyaHealOffer",
                      home.split("EryonVilaAurora_EventScript_ElyaAfterEclipse::", 1)[1])
        early = home.split("EryonVilaAurora_EventScript_ElyaAfterStarter::", 1)[1].split(
            "EryonVilaAurora_EventScript_ElyaAfterBadge::", 1)[0]
        self.assertLess(early.index("VAR_ERYON_CAPTURE_KIT_RECEIVED"),
                        early.index("FLAG_ERYON_ECLIPSE_NETWORK_SHUT_DOWN"))
        self.assertIn("givemon SPECIES_RIOLU, 5", home)
        self.assertIn("setflag FLAG_BADGE01_GET", verd)


    def test_gym_leaders_acknowledge_final_eclipse_shutdown_without_new_gates(self):
        cities = ("Verdelume", "Neonara", "Frostheim", "Arkhara",
                  "Umbra", "Ignivar", "Lunaris", "Drakonia")
        for city in cities:
            with self.subTest(city=city):
                source = (ROOT / "data/maps" / ("Eryon_" + city)
                          / "scripts.inc").read_text(encoding="utf-8")
                if city == "Verdelume":
                    after = "EryonVerdelume_EventScript_KaelAfterBattle"
                    peace = "EryonVerdelume_EventScript_KaelAfterPeace"
                else:
                    after = "Eryon" + city + "_EventScript_GymAfter"
                    peace = "Eryon" + city + "_EventScript_GymAfterEclipse"
                after_script = source.split(after + "::", 1)[1].split(
                    "\n\tend", 1)[0]
                self.assertIn(
                    "goto_if_set FLAG_ERYON_ECLIPSE_NETWORK_SHUT_DOWN, " + peace,
                    after_script,
                )
                self.assertEqual(source.count(peace + "::"), 1)
                dialogue = source.split(peace + "::", 1)[1].split(
                    "\n\tend", 1)[0]
                self.assertIn("msgbox ", dialogue)
                self.assertNotIn("setflag ", dialogue)
                self.assertNotIn("trainerbattle", dialogue)
                self.assertNotIn("\n\twarp ", dialogue)
                self.assertIn("trainerbattle_single TRAINER_ERYON_", source)
        for city, badge in (("Neonara", 2), ("Frostheim", 3),
                            ("Arkhara", 4), ("Umbra", 5), ("Ignivar", 6),
                            ("Lunaris", 7), ("Drakonia", 8)):
            source = (ROOT / "data/maps" / ("Eryon_" + city)
                      / "scripts.inc").read_text(encoding="utf-8")
            self.assertIn(f"setflag FLAG_BADGE{badge:02d}_GET", source)

if __name__ == "__main__":
    unittest.main()
