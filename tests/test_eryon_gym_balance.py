"""Gym level balance, safe badge flags, and traversable leader encounters.

Run from repository root:
    python3 -m unittest discover -s tests -p 'test_eryon_gym_balance.py' -v

Structural regression checks; a successful ROM compile and emulator play
are still needed to validate battle engine behavior.
"""
import json
import re
import unittest
from collections import deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAPS = ROOT / "data/maps"
LAYOUTS = ROOT / "data/layouts"
CITIES = ("Verdelume", "Neonara", "Frostheim", "Arkhara",
          "Umbra", "Ignivar", "Lunaris", "Drakonia")
GYM_TRAINERS = ["TRAINER_ERYON_KAEL"] + [
    f"TRAINER_ERYON_GYM_{city.upper()}" for city in CITIES[1:]
]
ACE_LEVELS = (18, 25, 31, 36, 41, 46, 51, 56)
BATTLE_NPCS = {
    "Verdelume": "EryonVerdelume_EventScript_Kael",
    "Frostheim": "EryonFrostheim_EventScript_Bjorn",
    "Arkhara": "EryonArkhara_EventScript_Tessa",
}


def blocks(text):
    pieces = re.split(r"(?m)^=== (TRAINER_[A-Z0-9_]+) ===\s*$", text)
    return {pieces[i]: pieces[i+1] for i in range(1, len(pieces)-1, 2)}


def neighbors(x, y):
    return ((x+1, y), (x-1, y), (x, y+1), (x, y-1))


class EryonGymBalance(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.party = blocks(
            (ROOT / "src/data/trainers.party").read_text(encoding="utf-8"))
        cls.flags = (
            ROOT / "include/constants/flags.h").read_text(encoding="utf-8")
        cls.opponents = (
            ROOT / "include/constants/opponents.h").read_text(encoding="utf-8")
        cls.engine = (
            ROOT / "src/battle_setup.c").read_text(encoding="utf-8")
        cls.layouts = {
            x["id"]: (x["width"], x["height"])
            for x in json.loads(
                (LAYOUTS / "layouts.json").read_text(encoding="utf-8"))["layouts"]
        }

    def test_every_eryon_trainer_name_fits_gba_limit(self):
        constants = (ROOT / "include/constants/global.h").read_text(encoding="utf-8")
        limit = int(re.search(r"(?m)^#define TRAINER_NAME_LENGTH\\s+(\\d+)", constants).group(1))
        for trainer, team in self.party.items():
            if not trainer.startswith("TRAINER_ERYON_"):
                continue
            name = re.search(r"(?m)^Name:\\s*(.+)$", team).group(1).strip()
            self.assertLessEqual(len(name), limit, f"{trainer} name is too long")

    def test_gym_levels_rise_without_large_spikes(self):
        for i, (city, trainer, ace) in enumerate(
                zip(CITIES, GYM_TRAINERS, ACE_LEVELS), 1):
            with self.subTest(gym=i, city=city):
                self.assertIn(trainer, self.party)
                body = self.party[trainer]
                levels = [int(v) for v in re.findall(
                    r"(?m)^Level: (\d+)$", body)]
                self.assertTrue(levels, f"No usable Pokemon in {city}")
                self.assertEqual(max(levels), ace)
                self.assertLessEqual(max(levels)-min(levels), 3)
                self.assertGreaterEqual(len(levels), 2)
                self.assertLessEqual(len(levels), 4)
        for before, after in zip(ACE_LEVELS, ACE_LEVELS[1:]):
            self.assertGreater(after, before)
            self.assertLessEqual(after-before, 7)

    def test_all_eight_gym_challenges_registered_and_accessible(self):
        for badge, city in enumerate(CITIES, 1):
            with self.subTest(badge=badge, city=city):
                folder = MAPS / f"Eryon_{city}"
                world = json.loads(
                    (folder / "map.json").read_text(encoding="utf-8"))
                source = (folder / "scripts.inc").read_text(encoding="utf-8")
                width, height = self.layouts[world["layout"]]
                data = (LAYOUTS / f"Eryon_{city}/map.bin").read_bytes()
                self.assertEqual(len(data), width*height*2)
                walk = set()
                for y in range(height):
                    for x in range(width):
                        pos = 2*(y*width+x)
                        tile = int.from_bytes(data[pos:pos+2], "little")
                        if ((tile >> 10) & 3) == 0:
                            walk.add((x, y))
                occupied = {(o["x"], o["y"])
                            for o in world["object_events"]}
                start = (world["warp_events"][0]["x"],
                         world["warp_events"][0]["y"])
                seen = {start}
                queue = deque([start])
                while queue:
                    x, y = queue.popleft()
                    for point in neighbors(x, y):
                        if point in walk and point not in occupied and point not in seen:
                            seen.add(point)
                            queue.append(point)
                self.assertTrue(all((w["x"], w["y"]) in seen
                                    for w in world["warp_events"]))
                npc_label = BATTLE_NPCS.get(
                    city, f"Eryon{city}_EventScript_GymLeader")
                npcs = [o for o in world["object_events"]
                        if o["script"] == npc_label]
                self.assertEqual(len(npcs), 1, f"Missing Gym NPC: {city}")
                leader = npcs[0]
                self.assertIn((leader["x"], leader["y"]), walk)
                self.assertTrue(any(p in seen
                                    for p in neighbors(leader["x"], leader["y"])))
                trainer = GYM_TRAINERS[badge - 1]
                self.assertIn(f"trainerbattle_single {trainer}", source)
                flag = f"FLAG_BADGE{badge:02d}_GET"
                self.assertIn(f"setflag {flag}", source)

    def test_new_trainers_share_badge_flag_not_system_overlap(self):
        for badge, city in enumerate(CITIES[1:], 2):
            self.assertIn(
                f"#define TRAINER_ERYON_GYM_{city.upper()} {878+badge}",
                self.opponents)
        self.assertGreaterEqual(
            int(re.search(r"(?m)^#define TRAINERS_COUNT_EMERALD\s+(\d+)", self.opponents).group(1)),
            887,
        )
        self.assertIn(
            "return FLAG_BADGE02_GET + trainerId - TRAINER_ERYON_GYM_NEONARA",
            self.engine)
        self.assertIn(
            "if (trainerId >= TRAINER_ERYON_GYM_NEONARA "
            "&& trainerId <= TRAINER_ERYON_GYM_DRAKONIA)", self.engine)

    def test_exp_is_trainer_focused_and_still_scaled(self):
        battle = (ROOT / "include/config/battle.h").read_text(encoding="utf-8")
        items = (ROOT / "include/config/item.h").read_text(encoding="utf-8")
        self.assertRegex(battle,
                         r"(?m)^#define B_TRAINER_EXP_MULTIPLIER\s+GEN_6\b")
        self.assertRegex(battle,
                         r"(?m)^#define B_SCALED_EXP\s+GEN_LATEST\b")
        self.assertRegex(battle,
                         r"(?m)^#define B_SPLIT_EXP\s+GEN_LATEST\b")
        self.assertRegex(items,
                         r"(?m)^#define I_EXP_SHARE_ITEM\s+GEN_5\b")

    def test_league_starts_close_to_final_gym(self):
        for i in range(1, 9):
            levels = [int(v) for v in re.findall(
                r"(?m)^Level: (\d+)$",
                self.party[f"TRAINER_ERYON_QUALIFIER_{i}"])]
            self.assertEqual(levels, [57+i, 58+i, 59+i])
        elite_ranges = ((67, 69), (68, 70), (69, 71), (70, 72))
        for i, (low, high) in enumerate(elite_ranges, 1):
            levels = [int(v) for v in re.findall(
                r"(?m)^Level: (\d+)$",
                self.party[f"TRAINER_ERYON_ELITE_{i}"])]
            self.assertEqual((min(levels), max(levels)), (low, high))
        champion = [int(v) for v in re.findall(
            r"(?m)^Level: (\d+)$", self.party["TRAINER_ERYON_CHAMPION"])]
        self.assertEqual((min(champion), max(champion)), (72, 75))


if __name__ == "__main__":
    unittest.main()
