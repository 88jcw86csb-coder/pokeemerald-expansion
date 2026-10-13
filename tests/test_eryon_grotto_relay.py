"""Static checks for the optional Star Grotto Eclipse relay."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CAVE = ROOT / "data/maps/Eryon_GrutaDasEstrelas"
CITY = ROOT / "data/maps/Eryon_CidadeDaLiga"
DRAKONIA = ROOT / "data/maps/Eryon_Drakonia"
LEAGUE_ROAD = ROOT / "data/maps/Eryon_CaminhoDaLiga"


class EryonRelayContract(unittest.TestCase):
    def test_console_is_on_map(self):
        data = json.loads((CAVE / "map.json").read_text(encoding="utf-8"))
        self.assertIn("EryonEstrelas_EventScript_RelayConsole",
                      [event["script"] for event in data["bg_events"]])

    def test_shutdown_requires_chart_and_is_persistent(self):
        script = (CAVE / "scripts.inc").read_text(encoding="utf-8")
        self.assertIn("goto_if_unset FLAG_ERYON_STAR_CHART_READ", script)
        self.assertIn("goto_if_set FLAG_ERYON_STAR_GROTTO_RELAY_DISABLED", script)
        self.assertIn("setflag FLAG_ERYON_STAR_GROTTO_RELAY_DISABLED", script)
        flags = (ROOT / "include/constants/flags.h").read_text(encoding="utf-8")
        self.assertIn("#define FLAG_ERYON_STAR_GROTTO_RELAY_DISABLED 0x3F", flags)

    def test_city_reacts_to_shutdown(self):
        script = (CITY / "scripts.inc").read_text(encoding="utf-8")
        self.assertIn("goto_if_set FLAG_ERYON_STAR_GROTTO_RELAY_DISABLED, "
                      "EryonCidadeLiga_EventScript_GuideRelayOff", script)
        self.assertIn("EryonCidadeLiga_EventScript_GuideRelayOff::", script)

    def test_neighboring_areas_react_to_shutdown(self):
        drakonia = (DRAKONIA / "scripts.inc").read_text(encoding="utf-8")
        road = (LEAGUE_ROAD / "scripts.inc").read_text(encoding="utf-8")
        self.assertIn("goto_if_set FLAG_ERYON_STAR_GROTTO_RELAY_DISABLED, EryonDrakonia_EventScript_ResearcherRelayOff", drakonia)
        self.assertIn("EryonDrakonia_EventScript_ResearcherRelayOff::", drakonia)
        self.assertIn("goto_if_set FLAG_ERYON_STAR_GROTTO_RELAY_DISABLED, EryonLigaCaminho_EventScript_ObserverRelayOff", road)
        self.assertIn("EryonLigaCaminho_EventScript_ObserverRelayOff::", road)

    def test_shutdown_unlocks_optional_party_healing(self):
        script = (CAVE / "scripts.inc").read_text(encoding="utf-8")
        start = script.index("EryonEstrelas_EventScript_RelayOff::")
        end = script.index("EryonEstrelas_EventScript_RelayLeave::", start)
        branch = script[start:end]
        self.assertIn("MSGBOX_YESNO", branch)
        self.assertIn("goto_if_eq VAR_RESULT, NO", branch)
        self.assertIn("special HealPlayerParty", branch)
        self.assertIn("EryonEstrelas_Text_RelayRestored:", script)


if __name__ == "__main__":
    unittest.main()
