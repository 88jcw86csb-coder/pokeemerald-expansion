#!/usr/bin/env python3
"""Regression tests for the Solaris desert to Ignivar sixth-gym-city expansion.

These are static encoding and graph checks, not a GBA emulator playtest.
"""
import json
import unittest
from collections import deque
from pathlib import Path

from build_eryon_map_bins import SPECS, PREVIEW_SPECS, compile_plan

ROOT = Path(__file__).resolve().parents[1]
TILES = {"#": 0x3C01, ".": 0x3001, ",": 0x3002, ":": 0x3003}


def load_map(name):
    return json.loads((ROOT / "data/maps" / name / "map.json").read_text(encoding="utf-8"))


def terrain_rows(path):
    return (ROOT / path).read_text(encoding="utf-8").splitlines()[4:]


def reachable(rows, start, occupied=()):
    """Walkable coordinates reachable while treating stationary NPCs as blocked."""
    height, width = len(rows), len(rows[0])
    occupied = set(occupied)
    found = {start}
    queue = deque([start])
    while queue:
        x, y = queue.popleft()
        for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            nx, ny = x + dx, y + dy
            point = (nx, ny)
            if (0 <= nx < width and 0 <= ny < height
                    and rows[ny][nx] != "#"
                    and point not in occupied and point not in found):
                found.add(point)
                queue.append(point)
    return found


class IgnivarExpansionTests(unittest.TestCase):
    def test_promoted_routes_not_regenerated_as_previews(self):
        self.assertFalse(set(SPECS) & set(PREVIEW_SPECS),
                         "Registered route must not also appear in PREVIEW_SPECS")

    def test_city_and_desert_terrain_sizes(self):
        city_path = ROOT / "docs/eryon/cidades/ignivar_city_plan.txt"
        city_tiles = {**TILES, "=": TILES["."],
                      **{symbol: TILES["."] for symbol in "GCMHP"}}
        self.assertEqual(len(compile_plan(city_path, city_tiles, 64, 56)), 7168)
        desert_path = ROOT / "docs/eryon/deserto_de_solaris_terrain_plan.txt"
        self.assertEqual(len(compile_plan(desert_path, TILES, 48, 44)), 4224)

    def test_reciprocal_warps_and_passable_solaris_crossing(self):
        desert = load_map("Eryon_DesertoDeSolaris")
        city = load_map("Eryon_Ignivar")
        self.assertEqual((desert["warp_events"][1]["dest_map"],
                          desert["warp_events"][1]["dest_warp_id"]),
                         ("MAP_ERYON_IGNIVAR", "0"))
        self.assertEqual((city["warp_events"][0]["dest_map"],
                          city["warp_events"][0]["dest_warp_id"]),
                         ("MAP_ERYON_DESERTO_DE_SOLARIS", "1"))
        desert_rows = terrain_rows("docs/eryon/deserto_de_solaris_terrain_plan.txt")
        occupied = {(npc["x"], npc["y"]) for npc in desert["object_events"]}
        found = reachable(desert_rows, (0, 22), occupied)
        self.assertIn((47, 22), found, "Desert must be crossable despite stationary NPCs")
        city_rows = terrain_rows("docs/eryon/cidades/ignivar_city_plan.txt")
        city_occupied = {(npc["x"], npc["y"]) for npc in city["object_events"]}
        city_reachable = reachable(city_rows, (0, 28), city_occupied)
        self.assertIn((32, 28), city_reachable, "Central plaza must be accessible")

    def test_ignivar_events_exist_and_can_be_approached(self):
        city = load_map("Eryon_Ignivar")
        rows = terrain_rows("docs/eryon/cidades/ignivar_city_plan.txt")
        script = (ROOT / "data/maps/Eryon_Ignivar/scripts.inc").read_text(encoding="utf-8")
        occupied = {(npc["x"], npc["y"]) for npc in city["object_events"]}
        accessible = reachable(rows, (0, 28), occupied)
        for event in city["object_events"] + city["bg_events"]:
            with self.subTest(script=event["script"]):
                point = (event["x"], event["y"])
                self.assertNotEqual(rows[point[1]][point[0]], "#")
                self.assertIn(event["script"] + "::", script)
                neighbors = ((point[0] + 1, point[1]), (point[0] - 1, point[1]),
                             (point[0], point[1] + 1), (point[0], point[1] - 1))
                self.assertTrue(any(p in accessible for p in neighbors),
                                f"Cannot approach {event['script']}")
        self.assertIn("goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND", script)

    def test_registered_ignivar_layout_matches_map(self):
        groups = json.loads((ROOT / "data/maps/map_groups.json").read_text())
        layouts = json.loads((ROOT / "data/layouts/layouts.json").read_text())["layouts"]
        self.assertIn("Eryon_Ignivar", groups["gMapGroup_Eryon"])
        city = load_map("Eryon_Ignivar")
        layout = next(x for x in layouts if x["id"] == city["layout"])
        self.assertEqual((layout["width"], layout["height"]), (64, 56))
        self.assertEqual(layout["blockdata_filepath"], "data/layouts/Eryon_Ignivar/map.bin")


if __name__ == "__main__":
    unittest.main()
