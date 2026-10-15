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


if __name__ == "__main__":
    unittest.main()
