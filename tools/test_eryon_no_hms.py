#!/usr/bin/env python3
"""Eryon main-story progression must never require a field HM.

This checks registered Eryon scripts, reciprocal warps and zero-collision
on-foot paths in the GBA terrain binaries. The emulator remains authoritative
for tile behaviors and event-driven obstructions.
"""
import json
import re
import struct
import unittest
from collections import deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAIN_CHAIN = (
    "Eryon_Ignivar",
    "Eryon_FlorestaDosEcos",
    "Eryon_ValeDosEcos",
    "Eryon_AldeiaDosEcos",
    "Eryon_TrilhaLunar",
    "Eryon_Lunaris",
    "Eryon_TrilhaDosDragoes",
    "Eryon_VilaDoPico",
    "Eryon_Drakonia",
    "Eryon_GrutaDasEstrelas",
    "Eryon_CaminhoDaLiga",
)
FORBIDDEN_MOVE = re.compile(
    r"\bMOVE_(?:CUT|ROCK_SMASH|STRENGTH|SURF|WATERFALL|DIVE|FLASH)\b"
)
FORBIDDEN_FIELD_SCRIPT = re.compile(
    r"(?im)^\s*(?:special|call|goto)\s+[A-Za-z0-9_]*"
    r"(?:RockSmash|CutTree|UseStrength|UseSurf|Waterfall|Dive|UseFlash)"
    r"[A-Za-z0-9_]*\b"
)


def walkable_region(raw, width, height, start):
    def open_tile(x, y):
        if not (0 <= x < width and 0 <= y < height):
            return False
        word = struct.unpack_from("<H", raw, 2 * (y * width + x))[0]
        return (word & 0x0C00) == 0

    if not open_tile(*start):
        return set()
    discovered = {start}
    queue = deque([start])
    while queue:
        x, y = queue.popleft()
        for point in ((x + 1, y), (x - 1, y),
                      (x, y + 1), (x, y - 1)):
            if point not in discovered and open_tile(*point):
                discovered.add(point)
                queue.append(point)
    return discovered


class NoMandatoryHMsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        groups = json.loads(
            (ROOT / "data/maps/map_groups.json").read_text(encoding="utf-8")
        )["gMapGroup_Eryon"]
        cls.maps = {}
        for name in groups:
            cls.maps[name] = json.loads(
                (ROOT / "data/maps" / name / "map.json").read_text(encoding="utf-8")
            )
        cls.layouts = {
            entry["id"]: entry
            for entry in json.loads(
                (ROOT / "data/layouts/layouts.json").read_text(encoding="utf-8")
            )["layouts"]
        }

    def test_no_required_hm_scripts_anywhere_in_eryon(self):
        for name, data in self.maps.items():
            with self.subTest(map=name):
                self.assertFalse(data["requires_flash"])
                script = (ROOT / "data/maps" / name / "scripts.inc").read_text(
                    encoding="utf-8"
                )
                self.assertNotRegex(script, FORBIDDEN_MOVE)
                self.assertNotRegex(script, FORBIDDEN_FIELD_SCRIPT)
                # Each map entrance is an ordinary reciprocal warp or edge.
                for warp in data.get("warp_events", []):
                    self.assertTrue(warp["dest_map"], f"{name} has empty warp")

    def test_main_story_warps_connect_without_hms(self):
        ids = {self.maps[name]["id"]: name for name in self.maps}
        for source, destination in zip(MAIN_CHAIN, MAIN_CHAIN[1:]):
            with self.subTest(segment=f"{source} -> {destination}"):
                src = self.maps[source]
                dst = self.maps[destination]
                edges = [
                    (i, warp) for i, warp in enumerate(src["warp_events"])
                    if warp["dest_map"] == dst["id"]
                ]
                self.assertEqual(len(edges), 1)
                index, warp = edges[0]
                next_index = int(warp["dest_warp_id"])
                self.assertLess(next_index, len(dst["warp_events"]))
                back = dst["warp_events"][next_index]
                self.assertEqual(ids[back["dest_map"]], source)
                self.assertEqual(int(back["dest_warp_id"]), index)

    def test_main_story_warp_exits_reachable_on_foot(self):
        for position, name in enumerate(MAIN_CHAIN):
            with self.subTest(map=name):
                data = self.maps[name]
                layout = self.layouts[data["layout"]]
                width, height = layout["width"], layout["height"]
                path = ROOT / layout["blockdata_filepath"]
                raw = path.read_bytes()
                self.assertEqual(len(raw), 2 * width * height)
                if position:
                    previous_id = self.maps[MAIN_CHAIN[position - 1]]["id"]
                    entrance = next(
                        warp for warp in data["warp_events"]
                        if warp["dest_map"] == previous_id
                    )
                else:
                    entrance = data["warp_events"][0]
                walkable = walkable_region(
                    raw, width, height, (entrance["x"], entrance["y"])
                )
                self.assertTrue(walkable, f"{name}: inaccessible entrance")
                if position + 1 < len(MAIN_CHAIN):
                    target_id = self.maps[MAIN_CHAIN[position + 1]]["id"]
                    exit_warp = next(
                        warp for warp in data["warp_events"]
                        if warp["dest_map"] == target_id
                    )
                    self.assertIn(
                        (exit_warp["x"], exit_warp["y"]), walkable,
                        f"{name}: HM-free exit blocked"
                    )
                if name == "Eryon_GrutaDasEstrelas":
                    self.assertIn((31, 30), walkable)
                if name == "Eryon_CaminhoDaLiga":
                    self.assertIn((44, 22), walkable)

    def test_arkhara_stone_city_open_on_foot(self):
        import json
        chain = ("Eryon_PassagemRochosa", "Eryon_Arkhara",
                 "Eryon_EstradaOriental")
        for source, destination in zip(chain, chain[1:]):
            with self.subTest(pair=source + " -> " + destination):
                src = self.maps[source]
                dst = self.maps[destination]
                outgoing = [(i, w) for i, w in enumerate(src["warp_events"])
                            if w["dest_map"] == dst["id"]]
                self.assertEqual(len(outgoing), 1)
                i, w = outgoing[0]
                reverse = dst["warp_events"][int(w["dest_warp_id"])]
                self.assertEqual(reverse["dest_map"], src["id"])
                self.assertEqual(int(reverse["dest_warp_id"]), i)
        city = self.maps["Eryon_Arkhara"]
        layout = self.layouts[city["layout"]]
        raw = (ROOT / layout["blockdata_filepath"]).read_bytes()
        self.assertEqual(len(raw), 64 * 56 * 2)
        start = city["warp_events"][0]
        end = city["warp_events"][1]
        reachable = walkable_region(
            raw, layout["width"], layout["height"], (start["x"], start["y"])
        )
        self.assertIn((end["x"], end["y"]), reachable)
        scripts = (ROOT / "data/maps/Eryon_Arkhara/scripts.inc").read_text(
            encoding="utf-8"
        )
        self.assertIn("setflag FLAG_ERYON_ARKHARA_RELAY_READ", scripts)
        self.assertNotRegex(scripts, FORBIDDEN_MOVE)

    def test_optional_star_chart_not_a_gate(self):
        cave_script = (ROOT / "data/maps/Eryon_GrutaDasEstrelas/scripts.inc").read_text(
            encoding="utf-8"
        )
        self.assertIn("setflag FLAG_ERYON_STAR_CHART_READ", cave_script)
        self.assertIn("EryonEstrelas_EventScript_StarChartRead::", cave_script)
        self.assertIn("EryonEstrelas_EventScript_OldBridge::", cave_script)
        self.assertNotRegex(cave_script, r"(?i)\b(?:MOVE_CUT|MOVE_STRENGTH|MOVE_ROCK_SMASH)\b")
        flags = (ROOT / "include/constants/flags.h").read_text(encoding="utf-8")
        self.assertRegex(
            flags, r"(?m)^#define\s+FLAG_ERYON_STAR_CHART_READ\s+0x2A\b"
        )
        road_script = (ROOT / "data/maps/Eryon_CaminhoDaLiga/scripts.inc").read_text(
            encoding="utf-8"
        )
        self.assertIn("special HealPlayerParty", road_script)


if __name__ == "__main__":
    unittest.main()
