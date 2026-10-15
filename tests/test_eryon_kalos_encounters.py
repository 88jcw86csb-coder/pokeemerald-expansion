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

    def test_oasis_caravan_alcove_connects_to_original_road(self):
        area = json.loads((MAPS / "Eryon_TrilhaDoOasis/map.json").read_text())
        lines = (ROOT / "docs/eryon/trilha_do_oasis_terrain_plan.txt").read_text().splitlines()[4:]
        self.assertEqual(len(lines), 44)
        self.assertTrue(all(len(row) == 48 for row in lines))
        for y in range(16, 21):
            for x in range(19, 25):
                self.assertNotEqual(lines[y][x], "#")
        self.assertEqual(lines[17][21], ".")
        reached = {(0, 22)}
        queue = deque([(0, 22)])
        while queue:
            x, y = queue.popleft()
            for nx, ny in neighbors(x, y):
                tile = (nx, ny)
                if (0 <= nx < 48 and 0 <= ny < 44 and
                        lines[ny][nx] != "#" and tile not in reached):
                    reached.add(tile)
                    queue.append(tile)
        for point in ((21, 17), (21, 20), (25, 22), (47, 22)):
            self.assertIn(point, reached)
        events = [event for event in area["bg_events"]
                  if event["script"] == "EryonOasis_EventScript_CaravanAlcove"]
        self.assertEqual([(e["x"], e["y"]) for e in events], [(21, 17)])
        source = (MAPS / "Eryon_TrilhaDoOasis/scripts.inc").read_text()
        entry = source.split("EryonOasis_EventScript_CaravanAlcove::", 1)[1].split(
            "EryonOasis_EventScript_AlcoveRiverEvidence::", 1)[0]
        self.assertIn("FLAG_ERYON_OASIS_HELIOPTILE_RESOLVED", entry)
        self.assertIn("FLAG_ERYON_RIVER_SAMPLE_RECORDED", entry)
        self.assertNotIn("setflag ", entry)

    def test_oasis_refuge_reward_is_accessible_and_bag_safe(self):
        area = json.loads((MAPS / "Eryon_TrilhaDoOasis/map.json").read_text())
        events = [e for e in area["bg_events"] if
                  e["script"] == "EryonOasis_EventScript_AlcoveSupplies"]
        self.assertEqual([(e["x"], e["y"]) for e in events], [(23, 17)])
        terrain = (ROOT / "docs/eryon/trilha_do_oasis_terrain_plan.txt").read_text().splitlines()[4:]
        self.assertNotEqual(terrain[17][23], "#")
        self.assertIn("#define FLAG_ERYON_OASIS_ALCOVE_SUPPLIES_TAKEN ", FLAGS)
        source = (MAPS / "Eryon_TrilhaDoOasis/scripts.inc").read_text()
        body = source.split("EryonOasis_EventScript_AlcoveSupplies::", 1)[1].split(
            "EryonOasis_EventScript_AlcoveSuppliesBagFull::", 1)[0]
        self.assertIn("giveitem ITEM_HYPER_POTION", body)
        self.assertLess(body.index("goto_if_eq VAR_RESULT, FALSE"),
                        body.index("setflag FLAG_ERYON_OASIS_ALCOVE_SUPPLIES_TAKEN"))
        self.assertEqual(source.count("EryonOasis_EventScript_AlcoveSupplies::"), 1)

    def test_rom_build_regenerates_route_binary_before_map_audit(self):
        build = (ROOT / "tools/build_eryon.sh").read_text()
        rebuild = "python3 tools/build_eryon_map_bins.py --wall 0x3c01"
        self.assertIn(rebuild, build)
        self.assertLess(build.index(rebuild),
                        build.index("python3 tools/eryon_layout_audit.py"))
        self.assertLess(build.index(rebuild),
                        build.index('make -j"$jobs" -O all'))
        self.assertIn("test_eryon_kalos_encounters.py", build)

    def test_oasis_guide_recognizes_helioptile_without_new_npc(self):
        area = json.loads((MAPS / "Eryon_TrilhaDoOasis/map.json").read_text())
        guides = [e for e in area["object_events"]
                  if e["script"] == "EryonOasis_EventScript_Guide"]
        self.assertEqual(len(guides), 1)
        source = (MAPS / "Eryon_TrilhaDoOasis/scripts.inc").read_text()
        guide = source.split("EryonOasis_EventScript_Guide::", 1)[1].split(
            "EryonOasis_EventScript_GuideClue::", 1)[0]
        self.assertIn("FLAG_ERYON_OASIS_HELIOPTILE_RESOLVED", guide)
        self.assertIn("EryonOasis_EventScript_GuideHelioptile::", source)
        self.assertIn("nivel 36", source)

    def test_wind_valley_new_garden_connects_to_existing_route(self):
        map_data = json.loads((MAPS / "Eryon_ValeDosVentos/map.json").read_text())
        terrain = (ROOT / "docs/eryon/vale_dos_ventos_terrain_plan.txt").read_text().splitlines()[4:48]
        self.assertEqual(len(terrain), 44)
        self.assertTrue(all(len(row) == 48 for row in terrain))
        events = [e for e in map_data["bg_events"] if
                  e["script"] == "EryonVale_EventScript_WindGarden"]
        self.assertEqual([(e["x"], e["y"]) for e in events], [(28, 15)])
        found = {(0, 21)}
        queue = deque([(0, 21)])
        while queue:
            x, y = queue.popleft()
            for nx, ny in neighbors(x, y):
                coord = nx, ny
                if 0 <= nx < 48 and 0 <= ny < 44 and terrain[ny][nx] != "#" and coord not in found:
                    found.add(coord)
                    queue.append(coord)
        for coord in ((28, 15), (28, 18), (47, 21)):
            self.assertIn(coord, found)
        source = (MAPS / "Eryon_ValeDosVentos/scripts.inc").read_text()
        entry = source.split("EryonVale_EventScript_WindGarden::", 1)[1].split(
            "EryonVale_EventScript_WindGardenClue::", 1)[0]
        self.assertIn("VAR_ERYON_SERRA_CLUE_FOUND", entry)
        self.assertNotIn("setflag ", entry)

    def test_wind_garden_supplies_are_unique_and_bag_safe(self):
        area = json.loads((MAPS / "Eryon_ValeDosVentos/map.json").read_text())
        events = [e for e in area["bg_events"] if
                  e["script"] == "EryonVale_EventScript_WindGardenSupplies"]
        self.assertEqual([(e["x"], e["y"]) for e in events], [(30, 15)])
        terrain = (ROOT / "docs/eryon/vale_dos_ventos_terrain_plan.txt").read_text().splitlines()[4:48]
        self.assertNotEqual(terrain[15][30], "#")
        self.assertIn("#define FLAG_ERYON_WIND_GARDEN_REWARD_CLAIMED ", FLAGS)
        source = (MAPS / "Eryon_ValeDosVentos/scripts.inc").read_text()
        body = source.split("EryonVale_EventScript_WindGardenSupplies::", 1)[1].split(
            "EryonVale_EventScript_WindGardenBagFull::", 1)[0]
        self.assertIn("giveitem ITEM_SUPER_POTION", body)
        self.assertLess(body.index("goto_if_eq VAR_RESULT, FALSE"),
                        body.index("setflag FLAG_ERYON_WIND_GARDEN_REWARD_CLAIMED"))

    def test_solar_canyon_branch_and_river_story(self):
        area = json.loads((MAPS / "Eryon_DesertoDeSolaris/map.json").read_text())
        terrain = (ROOT / "docs/eryon/deserto_de_solaris_terrain_plan.txt").read_text().splitlines()[4:48]
        self.assertEqual(len(terrain), 44)
        self.assertTrue(all(len(row) == 48 for row in terrain))
        for y in range(15, 21):
            for x in range(20, 26):
                self.assertNotEqual(terrain[y][x], "#")
        events = [event for event in area["bg_events"]
                  if event["script"] == "EryonSolaris_EventScript_SolarCanyon"]
        self.assertEqual([(e["x"], e["y"]) for e in events], [(22, 18)])
        seen = {(0, 22)}
        queue = deque([(0, 22)])
        while queue:
            x, y = queue.popleft()
            for nx, ny in neighbors(x, y):
                point = (nx, ny)
                if 0 <= nx < 48 and 0 <= ny < 44 and terrain[ny][nx] != "#" and point not in seen:
                    seen.add(point)
                    queue.append(point)
        self.assertIn((22, 18), seen)
        self.assertIn((47, 22), seen)
        script = (MAPS / "Eryon_DesertoDeSolaris/scripts.inc").read_text()
        entry = script.split("EryonSolaris_EventScript_SolarCanyon::", 1)[1].split(
            "EryonSolaris_EventScript_SolarCanyonRiver::", 1)[0]
        self.assertIn("FLAG_ERYON_RIVER_SAMPLE_RECORDED", entry)
        self.assertNotIn("setflag ", entry)

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
