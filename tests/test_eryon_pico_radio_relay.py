"""Optional Pico radio relay quest and map connectivity contract.

Run from repository root:
python3 -m unittest discover -s tests -p 'test_eryon_pico_radio_relay.py'

This checks saved flags, script structure and collision, not an emulator build.
"""
import json
import unittest
from collections import deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VILLAGE = ROOT / "data/maps/Eryon_VilaDoPico"
FLAG = "FLAG_ERYON_PICO_SIGNAL_REPAIRED"


def neighbors(x, y):
    return ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1))


class PicoRadioRelay(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.map = json.loads((VILLAGE / "map.json").read_text(encoding="utf-8"))
        cls.scripts = (VILLAGE / "scripts.inc").read_text(encoding="utf-8")
        width, height = 36, 30
        raw = (ROOT / "data/layouts/Eryon_VilaDoPico/map.bin").read_bytes()
        assert len(raw) == width * height * 2
        cls.floor = {
            (x, y)
            for y in range(height)
            for x in range(width)
            if ((int.from_bytes(raw[2*(y*width+x):2*(y*width+x)+2], "little") >> 10) & 3) == 0
        }

    def test_radio_relay_is_real_and_reachable(self):
        relay = [e for e in self.map["bg_events"]
                 if e["script"] == "EryonPico_EventScript_SignalRelay"]
        self.assertEqual(len(relay), 1)
        self.assertEqual((relay[0]["x"], relay[0]["y"]), (18, 5))
        blocked = {(n["x"], n["y"]) for n in self.map["object_events"]}
        entrance = self.map["warp_events"][0]
        start = (entrance["x"], entrance["y"])
        seen = {start}
        queue = deque([start])
        while queue:
            x, y = queue.popleft()
            for point in neighbors(x, y):
                if point in self.floor and point not in blocked and point not in seen:
                    seen.add(point)
                    queue.append(point)
        self.assertTrue(any(p in seen for p in neighbors(18, 5)))
        for warp in self.map["warp_events"]:
            self.assertIn((warp["x"], warp["y"]), seen)
        for npc in self.map["object_events"]:
            self.assertTrue(any(p in seen for p in neighbors(npc["x"], npc["y"])))
        for event in self.map["bg_events"]:
            self.assertTrue(any(p in seen for p in neighbors(event["x"], event["y"])))

    def test_repair_requires_manifest_and_can_be_declined(self):
        script = self.scripts
        flags = (ROOT / "include/constants/flags.h").read_text(encoding="utf-8")
        self.assertIn(f"#define {FLAG} 0x4A", flags)
        self.assertIn(
            "goto_if_unset FLAG_ERYON_DRAGON_TRAIL_MANIFEST_READ, "
            "EryonPico_EventScript_SignalRelayUnidentified", script)
        self.assertIn("MSGBOX_YESNO", script)
        self.assertIn(
            "goto_if_eq VAR_RESULT, NO, EryonPico_EventScript_SignalRelayDecline",
            script)
        self.assertIn(f"setflag {FLAG}", script)
        self.assertIn(
            f"goto_if_set {FLAG}, EryonPico_EventScript_SignalRelayRestored",
            script)

    def test_radio_operator_and_drakonia_acknowledge_repair(self):
        self.assertIn(
            f"goto_if_set {FLAG}, EryonPico_EventScript_RadioRepaired",
            self.scripts)
        drakonia = (ROOT / "data/maps/Eryon_Drakonia/scripts.inc").read_text(encoding="utf-8")
        self.assertIn(
            f"goto_if_set {FLAG}, EryonDrakonia_EventScript_CourierSignalRestored",
            drakonia)
        self.assertIn("EryonDrakonia_EventScript_CourierSignalRestored::", drakonia)


if __name__ == "__main__":
    unittest.main()
