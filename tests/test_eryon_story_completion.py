"""Finale sequence contracts; structural checks, not emulator evidence."""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FLAGS = ROOT / "include/constants/flags.h"
CITY = ROOT / "data/maps/Eryon_CidadeDaLiga/scripts.inc"
ELITE = ROOT / "data/maps/Eryon_LigaEliteFour/scripts.inc"
DRAKONIA = ROOT / "data/maps/Eryon_Drakonia/scripts.inc"
HOME = ROOT / "data/maps/Eryon_VilaAurora/scripts.inc"
CEREMONY = "FLAG_ERYON_PEACE_CEREMONY_RECORDED"


def body(source, label):
    match = re.search(
        r"(?m)^" + re.escape(label) +
        r"::\s*\n(.*?)(?=^[A-Za-z_][A-Za-z_0-9]*::?\s*$|\Z)",
        source, re.S | re.M)
    if not match:
        raise AssertionError(label)
    return match.group(1)


class EryonFinaleContinuityTests(unittest.TestCase):
    def test_one_time_public_ceremony_requires_champion_and_eclipse(self):
        flags = FLAGS.read_text(encoding="utf-8")
        self.assertRegex(flags, r"#define " + CEREMONY + r"\s+0x4BB")
        self.assertEqual(len(re.findall(r"(?m)^#define FLAG_\w+\s+0x4BB\b", flags)), 1)
        city = CITY.read_text(encoding="utf-8")
        board = body(city, "EryonCidadeLiga_EventScript_ResonanceBoard")
        restore = body(city, "EryonCidadeLiga_EventScript_ResonanceBoardRestored")
        ceremony = body(city, "EryonCidadeLiga_EventScript_PeaceCeremony")
        self.assertIn("FLAG_ERYON_ECLIPSE_NETWORK_SHUT_DOWN", board)
        self.assertIn("FLAG_ERYON_CHAMPION_CROWNED", restore)
        self.assertIn("EryonCidadeLiga_EventScript_PeaceCeremony", restore)
        self.assertIn("goto_if_set " + CEREMONY, ceremony)
        self.assertIn("MSGBOX_YESNO", ceremony)
        self.assertLess(ceremony.index("goto_if_eq VAR_RESULT, NO"), ceremony.index("setflag " + CEREMONY))
        self.assertEqual(ceremony.count("setflag " + CEREMONY), 1)
        self.assertNotIn("warp ", ceremony)
        self.assertNotIn("trainerbattle", ceremony)

    def test_champion_first_and_eclipse_first_both_resolve(self):
        elite = ELITE.read_text(encoding="utf-8")
        winner = body(elite, "EryonLigaElite_EventScript_Win5")
        self.assertIn("setflag FLAG_ERYON_CHAMPION_CROWNED", winner)
        self.assertIn("goto_if_set FLAG_ERYON_ECLIPSE_NETWORK_SHUT_DOWN", winner)
        self.assertNotIn("goto_if_unset FLAG_ERYON_ECLIPSE_NETWORK_SHUT_DOWN", winner)
        finale = body(DRAKONIA.read_text(encoding="utf-8"), "EryonDrakonia_EventScript_EclipseFinale")
        for needed in ("FLAG_ERYON_DRAKONIA_ECLIPSE_DEFEATED",
                       "FLAG_ERYON_STAR_GROTTO_RELAY_DISABLED",
                       "FLAG_ERYON_ECLIPSE_EVIDENCE_REPORTED"):
            self.assertIn("goto_if_unset " + needed, finale)
        self.assertIn("setflag FLAG_ERYON_ECLIPSE_NETWORK_SHUT_DOWN", finale)
        self.assertNotIn("FLAG_ERYON_CHAMPION_CROWNED", finale)

    def test_epilogue_after_milestones_is_readable_without_reset(self):
        city = CITY.read_text(encoding="utf-8")
        elite = ELITE.read_text(encoding="utf-8")
        drak = DRAKONIA.read_text(encoding="utf-8")
        home = HOME.read_text(encoding="utf-8")
        self.assertIn("goto_if_set " + CEREMONY + ", EryonLigaElite_EventScript_TrophyPeace", elite)
        self.assertIn("EryonVilaAurora_EventScript_ElyaChampionPeace::", home)
        self.assertIn("goto_if_set FLAG_ERYON_CHAMPION_CROWNED, EryonDrakonia_EventScript_FinalNetworkChampion", drak)
        self.assertIn("goto_if_set FLAG_ERYON_CHAMPION_CROWNED, EryonVilaAurora_EventScript_ElyaChampionPeace", home)
        for s in (body(city, "EryonCidadeLiga_EventScript_PeaceCeremony"),
                  body(elite, "EryonLigaElite_EventScript_TrophyPeace"),
                  body(home, "EryonVilaAurora_EventScript_ElyaChampionPeace")):
            self.assertNotIn("clearflag", s)
            self.assertNotIn("cleartrainerflag", s)


if __name__ == "__main__":
    unittest.main()
