"""Drakonia Eclipse showdown gameplay contract and accessible optional depot.

Run from repository root:
    python3 -m unittest discover -s tests -p 'test_eryon_drakonia_showdown.py'

Structural + collision tests. In-emulator gameplay and full compilation are separate.
"""
import json
import re
import unittest
from collections import deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAPS = ROOT / "data/maps"
WIDTH, HEIGHT = 64, 56
TRAINER = "TRAINER_ERYON_DRAKONIA_ECLIPSE"
BATTLE_FLAG = "FLAG_ERYON_DRAKONIA_ECLIPSE_DEFEATED"
CACHE_FLAG = "FLAG_ERYON_DRAKONIA_DEPOT_SUPPLIES_TAKEN"


def adjacent(point):
    x, y = point
    return (x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)


class EryonDrakoniaShowdown(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        folder = MAPS / "Eryon_Drakonia"
        cls.map = json.loads((folder / "map.json").read_text(encoding="utf-8"))
        cls.scripts = (folder / "scripts.inc").read_text(encoding="utf-8")
        raw = (ROOT / "data/layouts/Eryon_Drakonia/map.bin").read_bytes()
        assert len(raw) == WIDTH * HEIGHT * 2
        cls.walkable = set()
        for y in range(HEIGHT):
            for x in range(WIDTH):
                index = 2 * (y * WIDTH + x)
                word = int.from_bytes(raw[index:index + 2], "little")
                if ((word >> 10) & 3) == 0:
                    cls.walkable.add((x, y))

    def test_depot_reachable_with_stationary_characters(self):
        events = [e for e in self.map["bg_events"]
                  if e["script"] == "EryonDrakonia_EventScript_EclipseDepot"]
        self.assertEqual(len(events), 1)
        depot = events[0]["x"], events[0]["y"]
        self.assertEqual(depot, (59, 36))
        occupied = {(n["x"], n["y"]) for n in self.map["object_events"]}
        start = (self.map["warp_events"][0]["x"], self.map["warp_events"][0]["y"])
        reached = {start}
        queue = deque([start])
        while queue:
            for tile in adjacent(queue.popleft()):
                if tile in self.walkable and tile not in occupied and tile not in reached:
                    reached.add(tile)
                    queue.append(tile)
        self.assertTrue(any(p in reached for p in adjacent(depot)))
        for exit in self.map["warp_events"]:
            self.assertIn((exit["x"], exit["y"]), reached)

    def test_dedicated_trainer_uses_safe_flag(self):
        flags = (ROOT / "include/constants/flags.h").read_text(encoding="utf-8")
        opponents = (ROOT / "include/constants/opponents.h").read_text(encoding="utf-8")
        engine = (ROOT / "src/battle_setup.c").read_text(encoding="utf-8")
        party = (ROOT / "src/data/trainers.party").read_text(encoding="utf-8")
        self.assertIn(f"#define {BATTLE_FLAG} 0x44", flags)
        self.assertIn(f"#define {CACHE_FLAG} 0x45", flags)
        self.assertIn(f"#define {TRAINER} 873", opponents)
        self.assertIn("#define TRAINERS_COUNT_EMERALD     874", opponents)
        self.assertIn(f"if (trainerId == {TRAINER})", engine)
        self.assertIn(f"return {BATTLE_FLAG};", engine)
        self.assertEqual(len(re.findall(rf"(?m)^=== {TRAINER} ===$", party)), 1)
        battle_party = party.split(f"=== {TRAINER} ===", 1)[1]
        for species, level in (("Heliolisk", 47), ("Honchkrow", 48), ("Bisharp", 50)):
            self.assertRegex(battle_party, rf"(?m)^{species}\nLevel: {level}$")

    def test_battle_optional_after_mountain_clue(self):
        source = self.scripts
        self.assertIn(
            "goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1, "
            "EryonDrakonia_EventScript_AgentBattleOffer", source)
        self.assertIn(
            "goto_if_set FLAG_ERYON_DRAKONIA_ECLIPSE_DEFEATED, "
            "EryonDrakonia_EventScript_AgentAfterBattle", source)
        self.assertIn(f"trainerbattle_single {TRAINER},", source)
        self.assertIn(
            "goto_if_eq VAR_RESULT, NO, EryonDrakonia_EventScript_AgentDecline",
            source)

    def test_depot_reward_once_and_full_bag_retry(self):
        script = self.scripts
        self.assertIn(
            "goto_if_unset FLAG_ERYON_DRAKONIA_ECLIPSE_DEFEATED, "
            "EryonDrakonia_EventScript_DepotSealed", script)
        self.assertIn("giveitem ITEM_MAX_REVIVE", script)
        self.assertIn(
            "goto_if_eq VAR_RESULT, FALSE, EryonDrakonia_EventScript_DepotBagFull",
            script)
        self.assertIn(f"setflag {CACHE_FLAG}", script)

    def test_village_and_capital_react_to_victory(self):
        village = (MAPS / "Eryon_VilaDoPico/scripts.inc").read_text(encoding="utf-8")
        capital = (MAPS / "Eryon_CidadeDaLiga/scripts.inc").read_text(encoding="utf-8")
        self.assertIn(
            "goto_if_set FLAG_ERYON_DRAKONIA_ECLIPSE_DEFEATED, "
            "EryonPico_EventScript_RadioCommanderDefeated", village)
        self.assertIn(
            "goto_if_set FLAG_ERYON_DRAKONIA_ECLIPSE_DEFEATED, "
            "EryonCidadeLiga_EventScript_ReporterDrakonia", capital)


if __name__ == "__main__":
    unittest.main()
