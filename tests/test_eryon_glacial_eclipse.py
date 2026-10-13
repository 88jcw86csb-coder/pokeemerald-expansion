"""Real optional Eclipse battle and north-side laboratory cache on Glacial Trail.

Run from checkout:
    python3 -m unittest discover -s tests -p 'test_eryon_glacial_eclipse.py' -v

This is a static contract: a compiled ROM and emulator battles are still needed.
"""
import json
import re
import unittest
from collections import deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRAIL = ROOT / "data/maps/Eryon_TrilhaGlacial"
FROSTHEIM = ROOT / "data/maps/Eryon_Frostheim"
BATTLE = "TRAINER_ERYON_GLACIAL_ECLIPSE_RESEARCHER"
FLAG = "FLAG_ERYON_GLACIAL_ECLIPSE_RESEARCHER_DEFEATED"
REWARD_FLAG = "FLAG_ERYON_GLACIAL_ECLIPSE_SAMPLE_TAKEN"


def adj(p):
    x, y = p
    return ((x+1, y), (x-1, y), (x, y+1), (x, y-1))


class EryonGlacialEclipse(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.map = json.loads((TRAIL / "map.json").read_text(encoding="utf-8"))
        cls.source = (TRAIL / "scripts.inc").read_text(encoding="utf-8")
        data = (ROOT / "data/layouts/Eryon_TrilhaGlacial/map.bin").read_bytes()
        assert len(data) == 48*44*2
        cls.walk = set()
        for y in range(44):
            for x in range(48):
                i = 2*(y*48+x)
                cell = int.from_bytes(data[i:i+2], "little")
                if ((cell >> 10) & 3) == 0:
                    cls.walk.add((x, y))

    def test_battle_optional_and_matches_gym_three_difficulty(self):
        flags = (ROOT / "include/constants/flags.h").read_text(encoding="utf-8")
        opponents = (ROOT / "include/constants/opponents.h").read_text(encoding="utf-8")
        setup = (ROOT / "src/battle_setup.c").read_text(encoding="utf-8")
        party = (ROOT / "src/data/trainers.party").read_text(encoding="utf-8")
        self.assertIn(f"#define {FLAG} 0x22", flags)
        self.assertIn(f"#define {REWARD_FLAG} 0x23", flags)
        self.assertIn(f"#define {BATTLE} 887", opponents)
        self.assertGreaterEqual(
            int(re.search(r"(?m)^#define TRAINERS_COUNT_EMERALD\s+(\d+)", opponents).group(1)),
            888,
        )
        self.assertIn(f"if (trainerId == {BATTLE})", setup)
        self.assertIn(f"return {FLAG};", setup)
        self.assertEqual(len(re.findall(rf"(?m)^=== {BATTLE} ===$", party)), 1)
        team = party.split(f"=== {BATTLE} ===", 1)[1]
        for species, level in (("Sneasel", 27), ("Snorunt", 28), ("Glalie", 29)):
            self.assertRegex(team, rf"(?m)^{species}\nLevel: {level}$")
        self.assertIn("goto_if_set FLAG_BADGE02_GET, "
                      "EryonTrilhaGlacial_EventScript_ResearcherBattleOffer",
                      self.source)
        self.assertIn("MSGBOX_YESNO", self.source)
        self.assertIn("goto_if_eq VAR_RESULT, NO, "
                      "EryonTrilhaGlacial_EventScript_ResearcherDecline",
                      self.source)
        self.assertIn(f"trainerbattle_single {BATTLE},", self.source)

    def test_lab_sample_is_reachable_and_full_bag_safe(self):
        cache = [o for o in self.map["bg_events"]
                 if o["script"] == "EryonTrilhaGlacial_EventScript_EclipseIceSample"]
        self.assertEqual(len(cache), 1)
        self.assertEqual((cache[0]["x"], cache[0]["y"]), (35, 12))
        blocked = {(o["x"], o["y"]) for o in self.map["object_events"]}
        start = (self.map["warp_events"][0]["x"],
                 self.map["warp_events"][0]["y"])
        visited = {start}
        queue = deque([start])
        while queue:
            for n in adj(queue.popleft()):
                if n in self.walk and n not in blocked and n not in visited:
                    visited.add(n)
                    queue.append(n)
        self.assertTrue(any(n in visited for n in adj((35, 12))))
        for warp in self.map["warp_events"]:
            self.assertIn((warp["x"], warp["y"]), visited)
        self.assertIn(
            f"goto_if_unset {FLAG}, EryonTrilhaGlacial_EventScript_IceSampleSealed",
            self.source)
        self.assertIn("giveitem ITEM_NEVER_MELT_ICE", self.source)
        self.assertIn(
            "goto_if_eq VAR_RESULT, FALSE, "
            "EryonTrilhaGlacial_EventScript_IceSampleFull", self.source)
        self.assertIn(f"setflag {REWARD_FLAG}", self.source)

    def test_frostheim_acknowledges_victory_and_gym_is_not_broken(self):
        script = (FROSTHEIM / "scripts.inc").read_text(encoding="utf-8")
        self.assertIn(
            f"goto_if_set {FLAG}, EryonFrostheim_EventScript_ResearcherEclipseDefeated",
            script)
        self.assertIn("EryonFrostheim_EventScript_ResearcherEclipseDefeated::", script)
        self.assertIn(
            "goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1, "
            "EryonFrostheim_EventScript_GymOffer",
            script)
        self.assertIn("trainerbattle_single TRAINER_ERYON_GYM_FROSTHEIM", script)
        self.assertNotIn(
            "goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1, "
            "EryonFrostheim_EventScript_BjornAfterClue", script)


if __name__ == "__main__":
    unittest.main()
