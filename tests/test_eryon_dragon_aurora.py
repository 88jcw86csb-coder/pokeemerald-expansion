"""Aurora Terrace source/map regression for the existing Dragon Trail.

Static structure only; compilation and a real GBA emulator are separate gates.
"""
import json
import unittest
from collections import deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAP = ROOT / "data/maps/Eryon_TrilhaDosDragoes"
W, H = 48, 44


class DragonAuroraRegression(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.world = json.loads((MAP / "map.json").read_text(encoding="utf-8"))
        cls.script = (MAP / "scripts.inc").read_text(encoding="utf-8")
        cls.rows = (ROOT / "docs/eryon/trilha_dos_dragoes_terrain_plan.txt").read_text(
            encoding="utf-8").splitlines()[4:48]
        cls.binary = (ROOT / "data/layouts/Eryon_TrilhaDosDragoes/map.bin").read_bytes()

    def test_binary_collision_matches_all_2112_authoritative_metatiles(self):
        self.assertEqual(len(self.rows), H)
        self.assertTrue(all(len(row) == W for row in self.rows))
        self.assertEqual(len(self.binary), W * H * 2)
        metatiles = {"#": 0x3C01, ".": 0x3001, ",": 0x3002, ":": 0x3003}
        for y, row in enumerate(self.rows):
            for x, symbol in enumerate(row):
                p = 2 * (y * W + x)
                self.assertEqual(int.from_bytes(self.binary[p:p+2], "little"),
                                 metatiles[symbol], (x, y))

    def test_original_warps_noibat_and_both_overlooks_remain_reachable(self):
        warps = [(e["x"], e["y"]) for e in self.world["warp_events"]]
        self.assertEqual(warps, [(0, 22), (47, 22)])
        walkable = {(x, y) for y, row in enumerate(self.rows)
                    for x, c in enumerate(row) if c != "#"}
        fixed_npcs = {(e["x"], e["y"]) for e in self.world["object_events"]}
        visited = {warps[0]}
        queue = deque([warps[0]])
        while queue:
            x, y = queue.popleft()
            for q in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
                if q in walkable and q not in fixed_npcs and q not in visited:
                    visited.add(q)
                    queue.append(q)
        for location in (*warps, (30, 8), (44, 35),
                         (42, 9), (43, 11), (44, 13)):
            self.assertIn(location, visited)
        for npc in self.world["object_events"]:
            x, y = npc["x"], npc["y"]
            self.assertTrue(any((x+dx, y+dy) in visited for dx, dy
                                in ((1, 0), (-1, 0), (0, 1), (0, -1))))

    def test_unique_new_and_preserved_old_events(self):
        objects = (self.world["object_events"] + self.world["bg_events"] +
                   self.world["warp_events"])
        coords = [(e["x"], e["y"]) for e in objects]
        self.assertEqual(len(coords), len(set(coords)))
        for name, pos in (
            ("NoibatNest", (30, 8)),
            ("SummitCache", (44, 35)),
            ("AuroraCrystalArray", (42, 9)),
            ("CarbinkChamber", (43, 11)),
            ("AuroraSupplies", (44, 13)),
        ):
            label = "EryonDragoes_EventScript_" + name
            points = [e for e in self.world["bg_events"] if e["script"] == label]
            self.assertEqual([(e["x"], e["y"]) for e in points], [pos])
            self.assertEqual(self.script.count(label + "::"), 1)

    def test_carbink_outcomes_do_not_consume_fled_or_declined_encounters(self):
        source = self.script.split("EryonDragoes_EventScript_CarbinkChamber::", 1)[1].split(
            "EryonDragoes_EventScript_CarbinkResolved::", 1)[0]
        self.assertIn("goto_if_unset FLAG_ERYON_DRAGON_AURORA_ARRAY_READ", source)
        self.assertIn("setwildbattle SPECIES_CARBINK, 43", source)
        self.assertIn("dowildbattle", source)
        self.assertIn("specialvar VAR_RESULT, GetBattleOutcome", source)
        for outcome in ("B_OUTCOME_CAUGHT", "B_OUTCOME_WON"):
            self.assertIn(outcome + ", EryonDragoes_EventScript_CarbinkResolved", source)
        for outcome in ("B_OUTCOME_RAN", "B_OUTCOME_PLAYER_TELEPORTED"):
            self.assertIn(outcome + ", EryonDragoes_EventScript_CarbinkEscaped", source)
        self.assertNotIn("setflag FLAG_ERYON_DRAGON_CARBINK_RESOLVED", source)

    def test_one_time_reward_is_bag_safe_and_flags_are_distinct(self):
        flags = (ROOT / "include/constants/flags.h").read_text()
        for suffix, number in (("AURORA_ARRAY_READ", "4B6"),
                               ("CARBINK_RESOLVED", "4B7"),
                               ("AURORA_SUPPLIES_TAKEN", "4B8")):
            self.assertIn("FLAG_ERYON_DRAGON_" + suffix, flags)
            self.assertNotIn("FLAG_UNUSED_0x" + number, flags)
        source = self.script.split("EryonDragoes_EventScript_AuroraSupplies::", 1)[1].split(
            "EryonDragoes_EventScript_AuroraSuppliesLocked::", 1)[0]
        self.assertIn("giveitem ITEM_MAX_ETHER", source)
        self.assertIn("goto_if_unset FLAG_ERYON_DRAGON_CARBINK_RESOLVED", source)
        self.assertLess(source.index("goto_if_eq VAR_RESULT, FALSE"),
                        source.index("setflag FLAG_ERYON_DRAGON_AURORA_SUPPLIES_TAKEN"))

    def test_cities_record_both_encounters_without_changing_gym_or_eclipse(self):
        pico = (ROOT / "data/maps/Eryon_VilaDoPico/scripts.inc").read_text()
        drak = (ROOT / "data/maps/Eryon_Drakonia/scripts.inc").read_text()
        for source, name in ((pico, "EryonPico"), (drak, "EryonDrakonia")):
            self.assertIn("goto_if_set FLAG_ERYON_DRAGON_CARBINK_RESOLVED, "
                          + name + "_EventScript_", source)
            self.assertIn("goto_if_set FLAG_ERYON_DRAGON_TRAIL_NOIBAT_RESOLVED, "
                          + name + "_EventScript_", source)
        self.assertIn("EryonPico_EventScript_GeologistAuroraAndNoibat::", pico)
        self.assertIn("EryonDrakonia_EventScript_ResearcherAuroraAndNoibat::", drak)
        self.assertIn("trainerbattle_single TRAINER_ERYON_GYM_DRAKONIA", drak)
        self.assertIn("setflag FLAG_BADGE08_GET", drak)
        self.assertIn("EryonDrakonia_EventScript_EclipseFinale::", drak)

    def test_carbink_has_normal_species_exp_without_new_exp_calculation(self):
        species = (ROOT / "src/data/pokemon/species_info/gen_6_families.h").read_text()
        data = species.split("[SPECIES_CARBINK] =", 1)[1].split("[SPECIES_", 1)[0]
        self.assertIn(".expYield = 100", data)
        engine = (ROOT / "src/battle_script_commands.c").read_text()
        self.assertIn("Cmd_getexp", engine)


if __name__ == "__main__":
    unittest.main()
