"""Static checks for the optional Star Grotto Eclipse relay."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CAVE = ROOT / "data/maps/Eryon_GrutaDasEstrelas"
CITY = ROOT / "data/maps/Eryon_CidadeDaLiga"


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


if __name__ == "__main__":
    unittest.main()
