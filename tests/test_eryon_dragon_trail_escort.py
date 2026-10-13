"""Dragon Trail Eclipse escort, side lookout, map collision and story checks.

Run in project checkout:
python3 -m unittest discover -s tests -p 'test_eryon_dragon_trail_escort.py'
Structural checks only; compilation and GBA gameplay still require separate validation.
"""
import json
import re
import unittest
from collections import deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAPS = ROOT / "data/maps"
TRAIL = MAPS / "Eryon_TrilhaDosDragoes"
W, H = 48, 44
TRAINER = "TRAINER_ERYON_DRAGON_TRAIL_COURIER"
DEFEATED = "FLAG_ERYON_DRAGON_TRAIL_COURIER_DEFEATED"
LOOTED = "FLAG_ERYON_DRAGON_TRAIL_LOOKOUT_REWARD"


def neighbors(position):
    x, y = position
    return (x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)


class DragonTrailEscortContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.map = json.loads((TRAIL / "map.json").read_text(encoding="utf-8"))
        cls.scripts = (TRAIL / "scripts.inc").read_text(encoding="utf-8")
        raw = (ROOT / "data/layouts/Eryon_TrilhaDosDragoes/map.bin").read_bytes()
        assert len(raw) == W * H * 2, "Unexpected Dragon Trail layout size"
        cls.floor = {
            (x, y)
            for y in range(H)
            for x in range(W)
            if ((int.from_bytes(raw[2*(y*W+x):2*(y*W+x)+2], "little") >> 10) & 3) == 0
        }

    def test_two_exits_and_side_plateau_are_accessible(self):
        npc_positions = {(obj["x"], obj["y"]) for obj in self.map["object_events"]}
        origin = self.map["warp_events"][0]
        start = origin["x"], origin["y"]
        reachable = {start}
        queue = deque([start])
        while queue:
            for target in neighbors(queue.popleft()):
                if target in self.floor and target not in npc_positions and target not in reachable:
                    reachable.add(target)
                    queue.append(target)
        for warp in self.map["warp_events"]:
            self.assertIn((warp["x"], warp["y"]), reachable)
        for obj in self.map["object_events"]:
            self.assertIn((obj["x"], obj["y"]), self.floor)
            self.assertTrue(any(p in reachable for p in neighbors((obj["x"], obj["y"]))),
                            f"Inaccessible NPC: {obj['script']}")
        for event in self.map["bg_events"]:
            self.assertTrue(any(p in reachable for p in neighbors((event["x"], event["y"]))),
                            f"Inaccessible interaction: {event['script']}")
        self.assertGreaterEqual(len(self.floor), 480, "Southern plateau has disappeared")

    def test_new_researcher_and_lookout_really_exist_on_map(self):
        npcs = [obj for obj in self.map["object_events"]
                if obj["script"] == "EryonDragoes_EventScript_CliffResearcher"]
        caches = [event for event in self.map["bg_events"]
                  if event["script"] == "EryonDragoes_EventScript_SummitCache"]
        self.assertEqual(len(npcs), 1)
        self.assertEqual(len(caches), 1)
        self.assertEqual((npcs[0]["x"], npcs[0]["y"]), (29, 34))
        self.assertEqual((caches[0]["x"], caches[0]["y"]), (44, 35))
        self.assertIn("EryonDragoes_EventScript_CliffResearcher::", self.scripts)
        self.assertIn("EryonDragoes_EventScript_SummitCache::", self.scripts)

    def test_trainer_is_safe_for_existing_save_flags(self):
        flags = (ROOT / "include/constants/flags.h").read_text(encoding="utf-8")
        opponents = (ROOT / "include/constants/opponents.h").read_text(encoding="utf-8")
        engine = (ROOT / "src/battle_setup.c").read_text(encoding="utf-8")
        party = (ROOT / "src/data/trainers.party").read_text(encoding="utf-8")
        self.assertIn(f"#define {DEFEATED} 0x46", flags)
        self.assertIn(f"#define {LOOTED} 0x47", flags)
        self.assertIn(f"#define {TRAINER} 874", opponents)
        self.assertIn("#define TRAINERS_COUNT_EMERALD     875", opponents)
        self.assertIn(f"if (trainerId == {TRAINER})", engine)
        self.assertIn(f"return {DEFEATED};", engine)
        self.assertEqual(len(re.findall(rf"(?m)^=== {TRAINER} ===$", party)), 1)
        trainer_party = party.split(f"=== {TRAINER} ===", 1)[1]
        for species, level in (("Sneasel", 43), ("Skarmory", 44), ("Noivern", 46)):
            self.assertRegex(trainer_party, rf"(?m)^{species}\nLevel: {level}$")

    def test_battle_optional_and_reward_is_once_only(self):
        self.assertIn(
            "goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1, "
            "EryonDragoes_EventScript_CourierBattleOffer", self.scripts)
        self.assertIn(
            f"goto_if_set {DEFEATED}, EryonDragoes_EventScript_CourierAfterBattle",
            self.scripts)
        self.assertIn(f"trainerbattle_single {TRAINER},", self.scripts)
        self.assertIn("MSGBOX_YESNO", self.scripts)
        self.assertIn(
            f"goto_if_unset {DEFEATED}, EryonDragoes_EventScript_CacheLocked",
            self.scripts)
        self.assertIn("giveitem ITEM_DRAGON_FANG", self.scripts)
        self.assertIn(
            "goto_if_eq VAR_RESULT, FALSE, EryonDragoes_EventScript_CacheBagFull",
            self.scripts)
        self.assertIn(f"setflag {LOOTED}", self.scripts)

    def test_story_follows_player_to_village_and_sanctuary(self):
        for area, label in (
            ("Eryon_VilaDoPico", "EryonPico_EventScript_MessengerEscortBeaten"),
            ("Eryon_Drakonia", "EryonDrakonia_EventScript_CourierEscortBeaten"),
        ):
            with self.subTest(area=area):
                script = (MAPS / area / "scripts.inc").read_text(encoding="utf-8")
                self.assertIn(f"goto_if_set {DEFEATED}, {label}", script)
                self.assertIn(label + "::", script)


if __name__ == "__main__":
    unittest.main()
