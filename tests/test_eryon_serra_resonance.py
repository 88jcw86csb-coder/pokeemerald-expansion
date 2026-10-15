"""Serra dos Cristais: connected terrain and three-stage Eclipse signal investigation.

Run from the repository root:
    python3 -m unittest discover -s tests -p 'test_eryon_serra_resonance.py' -v

Structural checks; they do not substitute for compiling the ROM or an
end-to-end GBA/Delta emulator playthrough.
"""
import json
import re
import unittest
from collections import deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAPS = ROOT / "data/maps"
SERRA = "Eryon_SerraDosCristais"
W, H = 48, 44
NORTH = "FLAG_ERYON_SERRA_NORTH_CRYSTAL_CALIBRATED"
SOUTH = "FLAG_ERYON_SERRA_SOUTH_CRYSTAL_CALIBRATED"
DISABLED = "FLAG_ERYON_SERRA_ECLIPSE_SIGNAL_DISABLED"
REWARD = "FLAG_ERYON_SERRA_SURVEY_REWARD_CLAIMED"

STATIONS = {
    "EryonSerra_EventScript_NorthCrystalSeal": (40, 11),
    "EryonSerra_EventScript_SouthCrystalSeal": (9, 34),
    "EryonSerra_EventScript_EclipseResonanceCore": (33, 20),
}


def neighbors(point):
    x, y = point
    return ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1))


def script_body(contents, label):
    match = re.search(
        rf"(?ms)^{re.escape(label)}::\s*\n(.*?)(?=^[A-Za-z_][A-Za-z_0-9]*::?\s*$|\Z)",
        contents,
    )
    if not match:
        raise AssertionError(f"Missing script label: {label}")
    return match.group(1)


class EryonSerraResonance(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.map = json.loads((MAPS / SERRA / "map.json").read_text(encoding="utf-8"))
        cls.source = (MAPS / SERRA / "scripts.inc").read_text(encoding="utf-8")
        blockdata = (ROOT / "data/layouts" / SERRA / "map.bin").read_bytes()
        assert len(blockdata) == W * H * 2
        cls.walk = set()
        cls.rock = set()
        for y in range(H):
            for x in range(W):
                at = 2 * (y * W + x)
                value = int.from_bytes(blockdata[at:at + 2], "little")
                (cls.walk if ((value >> 10) & 3) == 0 else cls.rock).add((x, y))

    def test_serra_has_real_rocky_terrain_and_accessible_story(self):
        self.assertGreaterEqual(len(self.rock), 500,
                                "Serra should be a rocky route, not an empty field")
        # Serra is intentionally rocky (756/2112 floor tiles); requiring
        # 1500 floor tiles would erase real cliffs and ridge geometry.
        self.assertGreaterEqual(len(self.walk), 700)
        occupied = {(o["x"], o["y"]) for o in self.map["object_events"]}
        entrance = self.map["warp_events"][0]
        start = entrance["x"], entrance["y"]
        visited = {start}
        queue = deque([start])
        while queue:
            for tile in neighbors(queue.popleft()):
                if tile in self.walk and tile not in occupied and tile not in visited:
                    visited.add(tile)
                    queue.append(tile)
        # Every physical floor tile other than stationary NPCs must connect.
        self.assertEqual(self.walk - occupied, visited)
        self.assertEqual(len(self.map["warp_events"]), 4)
        for warp in self.map["warp_events"]:
            self.assertIn((warp["x"], warp["y"]), visited)
        for obj in self.map["object_events"]:
            point = obj["x"], obj["y"]
            self.assertIn(point, self.walk, obj["script"])
            self.assertTrue(any(p in visited for p in neighbors(point)), obj["script"])
        for event in self.map["bg_events"]:
            point = event["x"], event["y"]
            self.assertTrue(any(p in visited for p in neighbors(point)), event["script"])

    def test_all_three_stations_are_placed_and_defined(self):
        events = {o["script"]: (o["x"], o["y"]) for o in self.map["bg_events"]}
        for script, position in STATIONS.items():
            with self.subTest(script=script):
                self.assertEqual(events.get(script), position)
                self.assertIn(script + "::", self.source)

    def test_order_is_clue_then_third_badge_north_south_core(self):
        north = script_body(self.source, "EryonSerra_EventScript_NorthCrystalSeal")
        north_clue = script_body(self.source, "EryonSerra_EventScript_NorthClueFound")
        south = script_body(self.source, "EryonSerra_EventScript_SouthCrystalSeal")
        core = script_body(self.source, "EryonSerra_EventScript_EclipseResonanceCore")
        self.assertIn("goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1", north)
        self.assertIn("goto_if_unset FLAG_BADGE03_GET", north_clue)
        self.assertIn(f"goto_if_unset {NORTH}", south)
        self.assertIn(f"goto_if_unset {NORTH}", core)
        self.assertIn(f"goto_if_unset {SOUTH}", core)
        self.assertIn(f"setflag {NORTH}", north_clue)
        self.assertIn(f"setflag {SOUTH}", south)
        self.assertIn(f"setflag {DISABLED}", core)
        for script in (north_clue, south, core):
            self.assertIn("MSGBOX_YESNO", script)
            self.assertIn("closemessage", script)
        self.assertNotIn("warp ", self.source,
                         "Optional investigation must not change the route exits")

    def test_reward_is_optional_and_retryable_when_bag_is_full(self):
        flags = (ROOT / "include/constants/flags.h").read_text(encoding="utf-8")
        arkhara = (MAPS / "Eryon_Arkhara/scripts.inc").read_text(encoding="utf-8")
        for symbol, value in ((NORTH, 0x24), (SOUTH, 0x25),
                              (DISABLED, 0x26), (REWARD, 0x27)):
            self.assertIn(f"#define {symbol} 0x{value:X}", flags)
        geologist = script_body(arkhara, "EryonArkhara_EventScript_Geologist")
        reward = script_body(
            arkhara, "EryonArkhara_EventScript_GeologistResonance")
        self.assertIn(f"goto_if_set {DISABLED}", geologist)
        self.assertIn(f"goto_if_set {REWARD}", reward)
        self.assertIn("giveitem ITEM_PP_UP", reward)
        self.assertIn(
            "goto_if_eq VAR_RESULT, FALSE, EryonArkhara_EventScript_GeologistRewardFull",
            reward)
        self.assertLess(reward.index("goto_if_eq VAR_RESULT, FALSE"),
                        reward.index(f"setflag {REWARD}"))

    def test_frostheim_badge_three_unlocks_sierra_investigation_hints(self):
        frostheim = (MAPS / "Eryon_Frostheim/scripts.inc").read_text(
            encoding="utf-8")
        researcher = script_body(
            frostheim, "EryonFrostheim_EventScript_Researcher")
        self.assertIn(
            "goto_if_set FLAG_ERYON_SERRA_ECLIPSE_SIGNAL_DISABLED, "
            "EryonFrostheim_EventScript_ResearcherSerraQuiet", researcher)
        self.assertIn(
            "goto_if_set FLAG_BADGE03_GET, "
            "EryonFrostheim_EventScript_ResearcherSerraHint", researcher)
        self.assertIn("EryonFrostheim_EventScript_ResearcherSerraHint::",
                      frostheim)
        self.assertIn("EryonFrostheim_EventScript_ResearcherSerraQuiet::",
                      frostheim)

    def test_neighboring_maps_react_but_badge_four_is_still_available(self):
        passage = (MAPS / "Eryon_PassagemRochosa/scripts.inc").read_text(encoding="utf-8")
        arkhara = (MAPS / "Eryon_Arkhara/scripts.inc").read_text(encoding="utf-8")
        for symbol in ("EryonPassagem_EventScript_GuardSerraQuiet",
                       "EryonPassagem_EventScript_CrystalMarkSerraQuiet"):
            self.assertIn(symbol + "::", passage)
        for symbol in ("EryonArkhara_EventScript_EclipseCourierResonance",
                       "EryonArkhara_EventScript_TessaResonance"):
            self.assertIn(symbol + "::", arkhara)
        self.assertIn("trainerbattle_single TRAINER_ERYON_GYM_ARKHARA",
                      arkhara)
        self.assertIn("setflag FLAG_BADGE04_GET", arkhara)


if __name__ == "__main__":
    unittest.main()
