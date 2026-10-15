"""Registered Moonfall Sanctuary in Eryon's Lunar Trail.

Source and collision checks only; battle/EXP and save persistence require emulator tests.
"""
import json
import re
import unittest
from collections import deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROUTE = ROOT / "data/maps/Eryon_TrilhaLunar"
W, H = 48, 44


class MoonfallSanctuary(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.area = json.loads((ROUTE / "map.json").read_text(encoding="utf-8"))
        cls.script = (ROUTE / "scripts.inc").read_text(encoding="utf-8")
        cls.plan = (ROOT / "docs/eryon/trilha_lunar_terrain_plan.txt").read_text(
            encoding="utf-8").splitlines()[4:48]
        cls.binary = (ROOT / "data/layouts/Eryon_TrilhaLunar/map.bin").read_bytes()

    def test_terrain_binary_matches_collision_palette(self):
        self.assertEqual(len(self.plan), H)
        self.assertTrue(all(len(row) == W for row in self.plan))
        self.assertEqual(len(self.binary), W * H * 2)
        tiles = {"#": 0x3C01, ".": 0x3001, ",": 0x3002, ":": 0x3003}
        for y, line in enumerate(self.plan):
            for x, symbol in enumerate(line):
                value = int.from_bytes(self.binary[2*(W*y+x):2*(W*y+x)+2], "little")
                self.assertEqual(value, tiles[symbol], (x, y))

    def test_both_warps_and_new_events_accessible_without_moving_npcs(self):
        blocked = {(e["x"], e["y"]) for e in self.area["object_events"]}
        floor = {(x, y) for y, row in enumerate(self.plan)
                 for x, tile in enumerate(row) if tile != "#"}
        warps = [(w["x"], w["y"]) for w in self.area["warp_events"]]
        self.assertEqual(warps, [(0, 22), (47, 22)])
        seen = {warps[0]}
        pending = deque([warps[0]])
        while pending:
            x, y = pending.popleft()
            for target in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
                if target in floor and target not in blocked and target not in seen:
                    seen.add(target)
                    pending.append(target)
        for spot in (*warps, (14, 35), (17, 34), (19, 35), (20, 37)):
            self.assertIn(spot, seen)
        for npc in self.area["object_events"]:
            x, y = npc["x"], npc["y"]
            self.assertTrue(any((x+dx, y+dy) in seen for dx, dy
                                in ((1, 0), (-1, 0), (0, 1), (0, -1))))

    def test_new_events_have_unique_coordinates_and_definitions(self):
        points = self.area["object_events"] + self.area["bg_events"] + self.area["warp_events"]
        xy = [(p["x"], p["y"]) for p in points]
        self.assertEqual(len(xy), len(set(xy)))
        for suffix, xy in (("MoonfallArray", (17, 34)), ("InkayPool", (19, 35)),
                           ("MoonfallSupplies", (20, 37)), ("MoonfallRanger", (21, 34))):
            label = "EryonLunar_EventScript_" + suffix
            events = [e for e in points if e.get("script") == label]
            self.assertEqual([(e["x"], e["y"]) for e in events], [xy])
            self.assertEqual(self.script.count(label + "::"), 1)

    def test_kalos_inkay_battle_uses_standard_outcomes(self):
        source = self.script.split("EryonLunar_EventScript_InkayPool::", 1)[1].split(
            "EryonLunar_EventScript_InkayResolved::", 1)[0]
        self.assertIn("setwildbattle SPECIES_INKAY, 45", source)
        self.assertIn("dowildbattle", source)
        self.assertIn("specialvar VAR_RESULT, GetBattleOutcome", source)
        for result in ("B_OUTCOME_CAUGHT", "B_OUTCOME_WON"):
            self.assertIn(result + ", EryonLunar_EventScript_InkayResolved", source)
        for result in ("B_OUTCOME_RAN", "B_OUTCOME_PLAYER_TELEPORTED"):
            self.assertIn(result + ", EryonLunar_EventScript_InkayEscaped", source)
        self.assertNotIn("setflag FLAG_ERYON_LUNAR_INKAY_RESOLVED", source)
        gen6 = (ROOT / "src/data/pokemon/species_info/gen_6_families.h").read_text()
        inkay = gen6.split("[SPECIES_INKAY] =", 1)[1].split("[SPECIES_MALAMAR] =", 1)[0]
        self.assertIn("{EVO_LEVEL, 30, SPECIES_MALAMAR}", inkay)

    def test_item_reward_only_on_successful_bag_transfer(self):
        script = self.script.split("EryonLunar_EventScript_MoonfallSupplies::", 1)[1].split(
            "EryonLunar_EventScript_MoonfallSealed::", 1)[0]
        self.assertIn("giveitem ITEM_MAX_REVIVE", script)
        self.assertIn("goto_if_unset FLAG_ERYON_LUNAR_INKAY_RESOLVED", script)
        self.assertLess(script.index("goto_if_eq VAR_RESULT, FALSE"),
                        script.index("setflag FLAG_ERYON_LUNAR_SUPPLIES_TAKEN"))

    def test_ranger_registration_team_flags_and_exp_path(self):
        opponents = (ROOT / "include/constants/opponents.h").read_text()
        party = (ROOT / "src/data/trainers.party").read_text()
        battle = (ROOT / "src/battle_setup.c").read_text()
        flags = (ROOT / "include/constants/flags.h").read_text()
        self.assertIn("#define TRAINER_ERYON_LUNAR_RANGER 891", opponents)
        self.assertIn("#define TRAINERS_COUNT_EMERALD     892", opponents)
        self.assertIn("#define MAX_TRAINERS_COUNT_EMERALD 892", opponents)
        self.assertIn("return FLAG_ERYON_LUNAR_RANGER_DEFEATED;", battle)
        self.assertIn("#define FLAG_ERYON_LUNAR_RANGER_DEFEATED", flags)
        self.assertIn("trainerbattle_single TRAINER_ERYON_LUNAR_RANGER", self.script)
        team = party.split("=== TRAINER_ERYON_LUNAR_RANGER ===", 1)[1]
        self.assertIn("Lunatone\nLevel: 46", team)
        self.assertIn("Solrock\nLevel: 47", team)
        self.assertEqual(party.count("=== TRAINER_ERYON_LUNAR_RANGER ==="), 1)

    def test_lunaris_village_narrative_and_gym_preserved(self):
        city = (ROOT / "data/maps/Eryon_Lunaris/scripts.inc").read_text()
        village = (ROOT / "data/maps/Eryon_AldeiaDosEcos/scripts.inc").read_text()
        self.assertIn("FLAG_ERYON_LUNAR_INKAY_RESOLVED, EryonLunaris_EventScript_AstronomerInkay", city)
        self.assertIn("FLAG_ERYON_LUNAR_ARRAY_READ, EryonLunaris_EventScript_AstronomerMoonfall", city)
        self.assertIn("FLAG_ERYON_LUNAR_INKAY_RESOLVED, EryonAldeia_EventScript_ElderInkay", village)
        self.assertIn("trainerbattle_single TRAINER_ERYON_GYM_LUNARIS", city)
        self.assertIn("setflag FLAG_BADGE07_GET", city)


if __name__ == "__main__":
    unittest.main()
