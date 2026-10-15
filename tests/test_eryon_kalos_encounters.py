"""Regression checks for Eryon's optional Kalos wildlife discoveries.

Run from repository root:
    python3 -m unittest discover -s tests -p 'test_eryon_kalos_encounters.py'

Checks event flow and physical accessibility, not live gameplay or ROM compilation.
"""
import json
import unittest
from collections import deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAPS = ROOT / "data/maps"
LAYOUTS = ROOT / "data/layouts"
FLAGS = (ROOT / "include/constants/flags.h").read_text(encoding="utf-8")
SPECIES = (ROOT / "include/constants/species.h").read_text(encoding="utf-8")

AREAS = (
    ("Eryon_TrilhaDosDragoes", 48, 44,
     "EryonDragoes_EventScript_NoibatNest",
     "FLAG_ERYON_DRAGON_TRAIL_NOIBAT_RESOLVED",
     "NOIBAT", 38),
    ("Eryon_TrilhaDoOasis", 48, 44,
     "EryonOasis_EventScript_HelioptileNest",
     "FLAG_ERYON_OASIS_HELIOPTILE_RESOLVED",
     "HELIOPTILE", 32),
    ("Eryon_Drakonia", 64, 56,
     "EryonDrakonia_EventScript_AxewShrine",
     "FLAG_ERYON_DRAKONIA_AXEW_RESOLVED",
     "AXEW", 42),
)


def neighbors(x, y):
    return ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1))


class EryonKalosEncounters(unittest.TestCase):
    def test_nests_exist_and_can_be_reached_without_blocking_route(self):
        for name, w, h, script, flag, species, level in AREAS:
            with self.subTest(area=name):
                area = json.loads((MAPS / name / "map.json").read_text(encoding="utf-8"))
                raw = (LAYOUTS / name / "map.bin").read_bytes()
                self.assertEqual(len(raw), 2 * w * h)
                walkable = set()
                for y in range(h):
                    for x in range(w):
                        at = 2 * (y * w + x)
                        word = int.from_bytes(raw[at:at + 2], "little")
                        if ((word >> 10) & 3) == 0:
                            walkable.add((x, y))
                events = [ev for ev in area["bg_events"] if ev["script"] == script]
                self.assertEqual(len(events), 1)
                position = events[0]["x"], events[0]["y"]
                occupied = {(npc["x"], npc["y"]) for npc in area["object_events"]}
                origin = area["warp_events"][0]
                start = origin["x"], origin["y"]
                self.assertIn(start, walkable)
                reached = {start}
                queue = deque((start,))
                while queue:
                    x, y = queue.popleft()
                    for tile in neighbors(x, y):
                        if tile in walkable and tile not in occupied and tile not in reached:
                            reached.add(tile)
                            queue.append(tile)
                for warp in area["warp_events"]:
                    self.assertIn((warp["x"], warp["y"]), reached)
                self.assertTrue(any(tile in reached for tile in neighbors(*position)))
                source = (MAPS / name / "scripts.inc").read_text(encoding="utf-8")
                self.assertIn(f"{script}::", source)

    def test_encounters_are_catchable_and_retries_survive_escape(self):
        for name, w, h, script, flag, species, level in AREAS:
            with self.subTest(species=species):
                self.assertIn(f"#define {flag} ", FLAGS)
                self.assertIn(f"SPECIES_{species}", SPECIES)
                source = (MAPS / name / "scripts.inc").read_text(encoding="utf-8")
                self.assertIn(f"setwildbattle SPECIES_{species}, {level}", source)
                self.assertIn("dowildbattle", source)
                self.assertIn("specialvar VAR_RESULT, GetBattleOutcome", source)
                self.assertIn("B_OUTCOME_CAUGHT", source)
                self.assertIn("B_OUTCOME_WON", source)
                self.assertIn("B_OUTCOME_RAN", source)
                self.assertIn("B_OUTCOME_PLAYER_TELEPORTED", source)
                self.assertIn(f"setflag {flag}", source)
                # The catch/faint outcome branches must occur before the
                # outcome handler that persists the encounter.
                self.assertLess(source.index("B_OUTCOME_CAUGHT"), source.index(f"setflag {flag}"))
                self.assertLess(source.index("B_OUTCOME_WON"), source.index(f"setflag {flag}"))
                self.assertIn("MSGBOX_YESNO", source)

    def test_dragon_shrine_requires_local_eclipse_victory(self):
        source = (MAPS / "Eryon_Drakonia/scripts.inc").read_text(encoding="utf-8")
        self.assertIn(
            "goto_if_unset FLAG_ERYON_DRAKONIA_ECLIPSE_DEFEATED, "
            "EryonDrakonia_EventScript_AxewShrineDisturbed", source)

    def test_discoveries_affect_village_and_dragon_sanctuary(self):
        village = (MAPS / "Eryon_VilaDoPico/scripts.inc").read_text(encoding="utf-8")
        drakonia = (MAPS / "Eryon_Drakonia/scripts.inc").read_text(encoding="utf-8")
        self.assertIn(
            "goto_if_set FLAG_ERYON_DRAGON_TRAIL_NOIBAT_RESOLVED, "
            "EryonPico_EventScript_GeologistNoibat", village)
        self.assertIn(
            "goto_if_set FLAG_ERYON_DRAGON_TRAIL_NOIBAT_RESOLVED, "
            "EryonDrakonia_EventScript_ResearcherNoibat", drakonia)
        self.assertIn(
            "goto_if_set FLAG_ERYON_DRAKONIA_AXEW_RESOLVED, "
            "EryonPico_EventScript_ElderAxew", village)


if __name__ == "__main__":
    unittest.main()
