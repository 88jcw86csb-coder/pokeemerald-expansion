"""Regression contracts for Echo Forest north grove and the sixth-gym corridor.

This tests source and binary layout; it is not a ROM compile or emulator test.
"""
import json
import unittest
from collections import deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/maps/Eryon_FlorestaDosEcos"
WIDTH, HEIGHT = 48, 44


class ForestGroveTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.world = json.loads((BASE / "map.json").read_text(encoding="utf-8"))
        cls.script = (BASE / "scripts.inc").read_text(encoding="utf-8")
        cls.plan = (ROOT / "docs/eryon/floresta_dos_ecos_terrain_plan.txt").read_text(
            encoding="utf-8").splitlines()[4:48]
        cls.raw = (ROOT / "data/layouts/Eryon_FlorestaDosEcos/map.bin").read_bytes()

    def test_authoritative_plan_matches_real_binary_collision(self):
        self.assertEqual(len(self.plan), HEIGHT)
        self.assertTrue(all(len(r) == WIDTH for r in self.plan))
        self.assertEqual(len(self.raw), WIDTH * HEIGHT * 2)
        table = {"#": 0x3C01, ".": 0x3001, ",": 0x3002, ":": 0x3003}
        for y, row in enumerate(self.plan):
            for x, c in enumerate(row):
                i = 2 * (y * WIDTH + x)
                actual = int.from_bytes(self.raw[i:i + 2], "little")
                self.assertEqual(actual, table[c], (x, y))
                self.assertEqual(bool(actual & 0x0C00), c == "#", (x, y))

    def test_old_road_and_new_grove_reachable_with_npc_collision(self):
        walk = {(x, y) for y, row in enumerate(self.plan)
                for x, tile in enumerate(row) if tile != "#"}
        blocked = {(e["x"], e["y"]) for e in self.world["object_events"]}
        warps = [(e["x"], e["y"]) for e in self.world["warp_events"]]
        self.assertEqual(warps, [(0, 22), (47, 22)])
        seen = {warps[0]}
        todo = deque([warps[0]])
        while todo:
            x, y = todo.popleft()
            for pos in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                if pos in walk and pos not in blocked and pos not in seen:
                    seen.add(pos)
                    todo.append(pos)
        for pos in (*warps, (25, 7), (25, 13), (25, 16), (24, 17), (26, 17)):
            self.assertIn(pos, seen)
        for npc in self.world["object_events"]:
            x, y = npc["x"], npc["y"]
            self.assertTrue(any((x+dx, y+dy) in seen
                                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))))

    def test_new_events_are_unique_without_touching_warps(self):
        events = self.world["object_events"] + self.world["bg_events"] + self.world["warp_events"]
        positions = [(e["x"], e["y"]) for e in events]
        self.assertEqual(len(positions), len(set(positions)))
        for name, pos in (("CanopyLog", (25, 16)),
                          ("PhantumpNest", (24, 17)),
                          ("GroveCache", (26, 17))):
            label = "EryonEcos_EventScript_" + name
            actual = [(e["x"], e["y"]) for e in self.world["bg_events"]
                      if e["script"] == label]
            self.assertEqual(actual, [pos])
            self.assertEqual(self.script.count(label + "::"), 1)

    def test_wild_phantump_uses_normal_battle_result_and_retries(self):
        entry = self.script.split("EryonEcos_EventScript_PhantumpNest::", 1)[1].split(
            "EryonEcos_EventScript_PhantumpResolved::", 1)[0]
        self.assertIn("goto_if_unset FLAG_ERYON_FOREST_SIGNAL_LOG_READ", entry)
        self.assertIn("setwildbattle SPECIES_PHANTUMP, 40", entry)
        self.assertIn("dowildbattle", entry)
        self.assertIn("specialvar VAR_RESULT, GetBattleOutcome", entry)
        for code in ("B_OUTCOME_CAUGHT", "B_OUTCOME_WON"):
            self.assertIn(code + ", EryonEcos_EventScript_PhantumpResolved", entry)
        for code in ("B_OUTCOME_RAN", "B_OUTCOME_PLAYER_TELEPORTED"):
            self.assertIn(code + ", EryonEcos_EventScript_PhantumpEscaped", entry)
        self.assertNotIn("setflag FLAG_ERYON_FOREST_PHANTUMP_RESOLVED", entry)
        self.assertIn("setflag FLAG_ERYON_FOREST_PHANTUMP_RESOLVED",
                      self.script.split("EryonEcos_EventScript_PhantumpResolved::", 1)[1])

    def test_unique_flags_and_full_bag_reward_retry(self):
        flags = (ROOT / "include/constants/flags.h").read_text()
        for name, val in (("SIGNAL_LOG_READ", "0x4AC"),
                          ("PHANTUMP_RESOLVED", "0x4AD"),
                          ("GROVE_CACHE_TAKEN", "0x4AE")):
            self.assertIn("FLAG_ERYON_FOREST_" + name, flags)
            self.assertNotIn("FLAG_UNUSED_" + val, flags)
        item = self.script.split("EryonEcos_EventScript_GroveCache::", 1)[1].split(
            "EryonEcos_EventScript_GroveCacheSealed::", 1)[0]
        self.assertIn("goto_if_unset FLAG_ERYON_FOREST_PHANTUMP_RESOLVED", item)
        self.assertIn("giveitem ITEM_DUSK_BALL", item)
        self.assertLess(item.index("goto_if_eq VAR_RESULT, FALSE"),
                        item.index("setflag FLAG_ERYON_FOREST_GROVE_CACHE_TAKEN"))

    def test_narrative_reaches_cities_without_changing_gym(self):
        city = (ROOT / "data/maps/Eryon_Ignivar/scripts.inc").read_text()
        village = (ROOT / "data/maps/Eryon_AldeiaDosEcos/scripts.inc").read_text()
        self.assertIn("FLAG_ERYON_FOREST_PHANTUMP_RESOLVED, EryonIgnivar_EventScript_EngineerGroveSafe", city)
        self.assertIn("FLAG_ERYON_FOREST_PHANTUMP_RESOLVED, EryonAldeia_EventScript_WitnessGroveSafe", village)
        self.assertIn("FLAG_ERYON_FOREST_SIGNAL_LOG_READ, EryonAldeia_EventScript_WitnessCanopyLog", village)
        self.assertIn("trainerbattle_single TRAINER_ERYON_GYM_IGNIVAR", city)
        self.assertIn("setflag FLAG_BADGE06_GET", city)

    def test_phantump_has_only_level_evolution(self):
        gen6 = (ROOT / "src/data/pokemon/species_info/gen_6_families.h").read_text()
        data = gen6.split("[SPECIES_PHANTUMP] =", 1)[1].split(
            "[SPECIES_TREVENANT] =", 1)[0]
        self.assertIn(".evolutions = EVOLUTION({EVO_LEVEL, 36, SPECIES_TREVENANT})", data)
        self.assertNotIn("EVO_ITEM", data)
        self.assertNotIn("EVO_TRADE", data)


if __name__ == "__main__":
    unittest.main()
