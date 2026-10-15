"""Glacial Ridge geometry, Eclipse caches and optional Kalos Bergmite quest.

Read-only source and binary assertions; these are not emulator tests.
"""
import json
import unittest
from collections import deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GLACIAL = ROOT / "data/maps/Eryon_TrilhaGlacial"
WIDTH, HEIGHT = 48, 44


class GlacialRiftRegression(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.world = json.loads((GLACIAL / "map.json").read_text(encoding="utf-8"))
        cls.scripts = (GLACIAL / "scripts.inc").read_text(encoding="utf-8")
        cls.rows = (ROOT / "docs/eryon/trilha_glacial_terrain_plan.txt").read_text(
            encoding="utf-8").splitlines()[4:48]
        cls.binary = (ROOT / "data/layouts/Eryon_TrilhaGlacial/map.bin").read_bytes()

    def test_actual_map_binary_matches_authoritative_collision_plan(self):
        self.assertEqual(len(self.rows), HEIGHT)
        self.assertTrue(all(len(row) == WIDTH for row in self.rows))
        self.assertEqual(len(self.binary), WIDTH * HEIGHT * 2)
        codes = {"#": 0x3C01, ".": 0x3001, ",": 0x3002, ":": 0x3003}
        for y, row in enumerate(self.rows):
            for x, c in enumerate(row):
                offset = 2 * (y * WIDTH + x)
                tile = int.from_bytes(self.binary[offset:offset + 2], "little")
                self.assertEqual(tile, codes[c], (x, y))
                self.assertEqual(bool((tile >> 10) & 3), c == "#", (x, y))

    def test_both_original_warps_lab_caches_and_rift_are_reachable(self):
        warps = [(e["x"], e["y"]) for e in self.world["warp_events"]]
        self.assertEqual(warps, [(0, 22), (47, 22)])
        npcs = {(e["x"], e["y"]) for e in self.world["object_events"]}
        walk = {(x, y) for y, row in enumerate(self.rows)
                for x, c in enumerate(row) if c != "#"}
        seen, todo = {warps[0]}, deque([warps[0]])
        while todo:
            x, y = todo.popleft()
            for p in ((x-1, y), (x+1, y), (x, y-1), (x, y+1)):
                if p in walk and p not in npcs and p not in seen:
                    seen.add(p)
                    todo.append(p)
        for point in (*warps, (35, 12), (39, 12),
                      (43, 10), (43, 14), (45, 15)):
            self.assertIn(point, seen)
        for npc in self.world["object_events"]:
            x, y = npc["x"], npc["y"]
            self.assertTrue(any((x + dx, y + dy) in seen for dx, dy in
                                ((1, 0), (-1, 0), (0, 1), (0, -1))))

    def test_no_duplicate_events_and_existing_caches_kept(self):
        events = self.world["object_events"] + self.world["bg_events"] + self.world["warp_events"]
        positions = [(e["x"], e["y"]) for e in events]
        self.assertEqual(len(positions), len(set(positions)))
        for name, pos in (
            ("ResearchSupplies", (39, 12)),
            ("EclipseIceSample", (35, 12)),
            ("IceRiftJournal", (43, 10)),
            ("BergmiteNest", (43, 14)),
            ("RiftSupplies", (45, 15)),
        ):
            label = "EryonTrilhaGlacial_EventScript_" + name
            signs = [e for e in self.world["bg_events"] if e["script"] == label]
            self.assertEqual([(e["x"], e["y"]) for e in signs], [pos])
            self.assertEqual(self.scripts.count(label + "::"), 1)

    def test_battle_save_flags_and_retry_after_escape(self):
        entry = self.scripts.split("EryonTrilhaGlacial_EventScript_BergmiteNest::", 1)[1].split(
            "EryonTrilhaGlacial_EventScript_BergmiteResolved::", 1)[0]
        self.assertIn("goto_if_unset FLAG_ERYON_GLACIAL_RIFT_LOG_READ", entry)
        self.assertIn("setwildbattle SPECIES_BERGMITE, 29", entry)
        self.assertIn("dowildbattle", entry)
        self.assertIn("specialvar VAR_RESULT, GetBattleOutcome", entry)
        for result in ("B_OUTCOME_CAUGHT", "B_OUTCOME_WON"):
            self.assertIn(result + ", EryonTrilhaGlacial_EventScript_BergmiteResolved", entry)
        for result in ("B_OUTCOME_RAN", "B_OUTCOME_PLAYER_TELEPORTED"):
            self.assertIn(result + ", EryonTrilhaGlacial_EventScript_BergmiteEscaped", entry)
        self.assertNotIn("setflag FLAG_ERYON_GLACIAL_BERGMITE_RESOLVED", entry)
        species = (ROOT / "src/data/pokemon/species_info/gen_6_families.h").read_text()
        bergmite = species.split("[SPECIES_BERGMITE] =", 1)[1].split(
            "[SPECIES_AVALUGG] =", 1)[0]
        self.assertIn("EVO_LEVEL, 37, SPECIES_AVALUGG", bergmite)

    def test_reward_preserves_item_when_bag_is_full(self):
        source = self.scripts.split("EryonTrilhaGlacial_EventScript_RiftSupplies::", 1)[1].split(
            "EryonTrilhaGlacial_EventScript_RiftSuppliesLocked::", 1)[0]
        self.assertIn("giveitem ITEM_REVIVE", source)
        self.assertIn("goto_if_unset FLAG_ERYON_GLACIAL_BERGMITE_RESOLVED", source)
        self.assertLess(source.index("goto_if_eq VAR_RESULT, FALSE"),
                        source.index("setflag FLAG_ERYON_GLACIAL_RIFT_SUPPLIES_TAKEN"))

    def test_new_flags_do_not_overlap_and_original_eclipse_battle_remains(self):
        flags = (ROOT / "include/constants/flags.h").read_text(encoding="utf-8")
        for suffix, hex_id in (("RIFT_LOG_READ", "4B3"),
                               ("BERGMITE_RESOLVED", "4B4"),
                               ("RIFT_SUPPLIES_TAKEN", "4B5")):
            self.assertIn("FLAG_ERYON_GLACIAL_" + suffix, flags)
            self.assertNotIn("FLAG_UNUSED_0x" + hex_id, flags)
        self.assertIn("trainerbattle_single TRAINER_ERYON_GLACIAL_ECLIPSE_RESEARCHER",
                      self.scripts)
        self.assertIn("giveitem ITEM_NEVER_MELT_ICE", self.scripts)
        self.assertIn("giveitem ITEM_SUPER_POTION", self.scripts)

    def test_frostheim_and_mist_village_react_without_gym_gating(self):
        frost = (ROOT / "data/maps/Eryon_Frostheim/scripts.inc").read_text()
        mist = (ROOT / "data/maps/Eryon_VilaDaNeblina/scripts.inc").read_text()
        self.assertIn("FLAG_ERYON_GLACIAL_BERGMITE_RESOLVED, "
                      "EryonFrostheim_EventScript_ResearcherBergmiteSafe", frost)
        self.assertIn("FLAG_ERYON_GLACIAL_RIFT_LOG_READ, "
                      "EryonVilaNeblina_EventScript_ElderRiftFound", mist)
        self.assertIn("FLAG_ERYON_GLACIAL_BERGMITE_RESOLVED, "
                      "EryonVilaNeblina_EventScript_ElderBergmiteSafe", mist)
        self.assertIn("trainerbattle_single TRAINER_ERYON_GYM_FROSTHEIM", frost)
        self.assertIn("setflag FLAG_BADGE03_GET", frost)


if __name__ == "__main__":
    unittest.main()
