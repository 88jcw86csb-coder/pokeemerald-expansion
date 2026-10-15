"""Connectivity contract of the 42 registered Eryon overworld/interior maps.

All map warp indexes and connections must be valid. The start village connects
through a border, and the League's three interior halls use script-based warps.
This is NOT an emulator test and does not validate NPC collision in real time.
"""
import json
import re
import unittest
from collections import deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAP_ROOT = ROOT / "data/maps"
LAYOUT_ROOT = ROOT / "data/layouts"
SCRIPT_WARP = re.compile(
    r"(?m)^\s*warp\s+(MAP_ERYON_[A-Z0-9_]+)"
    r"\s*,\s*(\d+)\s*,\s*(\d+)\b"
)
OPPOSITE = {"up": "down", "down": "up", "left": "right", "right": "left"}


class EryonWorldMapNetwork(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        groups = json.loads((MAP_ROOT / "map_groups.json").read_text(encoding="utf-8"))
        cls.names = groups["gMapGroup_Eryon"]
        cls.maps = {
            name: json.loads((MAP_ROOT / name / "map.json").read_text(encoding="utf-8"))
            for name in cls.names
        }
        cls.scripts = {
            name: (MAP_ROOT / name / "scripts.inc").read_text(encoding="utf-8")
            for name in cls.names
        }
        cls.by_id = {data["id"]: name for name, data in cls.maps.items()}
        cls.dims = {
            record["id"]: (record["width"], record["height"])
            for record in json.loads((LAYOUT_ROOT / "layouts.json").read_text(
                encoding="utf-8"))["layouts"]
        }

    def test_unique_registered_maps_and_all_layouts_exist(self):
        self.assertEqual(len(self.maps), 42)
        self.assertEqual(len(self.by_id), len(self.maps))
        for name, info in self.maps.items():
            with self.subTest(map=name):
                self.assertIn(info["layout"], self.dims)

    def test_all_overworld_warps_have_exact_reverse_pair(self):
        found = 0
        for name, area in self.maps.items():
            for index, warp in enumerate(area["warp_events"]):
                with self.subTest(map=name, warp=index):
                    self.assertIn(warp["dest_map"], self.by_id)
                    dest = self.maps[self.by_id[warp["dest_map"]]]
                    dest_index = int(warp["dest_warp_id"])
                    self.assertGreaterEqual(dest_index, 0)
                    self.assertLess(dest_index, len(dest["warp_events"]))
                    reverse = dest["warp_events"][dest_index]
                    self.assertEqual(reverse["dest_map"], area["id"])
                    self.assertEqual(int(reverse["dest_warp_id"]), index)
                    w, h = self.dims[area["layout"]]
                    self.assertGreaterEqual(warp["x"], 0)
                    self.assertGreaterEqual(warp["y"], 0)
                    self.assertLess(warp["x"], w)
                    self.assertLess(warp["y"], h)
                found += 1
        self.assertGreaterEqual(found, 65)

    def test_border_connections_are_reciprocal(self):
        all_connections = 0
        for name, area in self.maps.items():
            for link in (area["connections"] or []):
                with self.subTest(map=name, neighbor=link["map"]):
                    self.assertIn(link["map"], self.by_id)
                    partner = self.maps[self.by_id[link["map"]]]
                    reciprocal = [
                        other for other in (partner["connections"] or [])
                        if other["map"] == area["id"]
                        and other["direction"] == OPPOSITE[link["direction"]]
                    ]
                    self.assertTrue(reciprocal)
                all_connections += 1
        self.assertGreaterEqual(all_connections, 2)

    def test_scripted_transitions_target_existing_map_and_in_bounds(self):
        found = 0
        for name, source in self.scripts.items():
            for target, x, y in SCRIPT_WARP.findall(source):
                with self.subTest(map=name, dest=target, x=x, y=y):
                    self.assertIn(target, self.by_id)
                    destination = self.maps[self.by_id[target]]
                    width, height = self.dims[destination["layout"]]
                    self.assertLess(int(x), width)
                    self.assertLess(int(y), height)
                found += 1
        self.assertGreaterEqual(found, 5)

    def test_every_registered_map_is_reachable_from_start(self):
        edges = {info["id"]: set() for info in self.maps.values()}
        for name, area in self.maps.items():
            start = area["id"]
            for warp in area["warp_events"]:
                edges[start].add(warp["dest_map"])
            for link in (area["connections"] or []):
                edges[start].add(link["map"])
            for target, _, _ in SCRIPT_WARP.findall(self.scripts[name]):
                edges[start].add(target)
        start = "MAP_ERYON_VILA_AURORA"
        seen, remaining = {start}, deque([start])
        while remaining:
            for neighbor in edges[remaining.popleft()]:
                if neighbor not in seen:
                    seen.add(neighbor)
                    remaining.append(neighbor)
        self.assertEqual(seen, set(self.by_id))
        for internal in ("MAP_ERYON_LIGA_RECEPCAO",
                         "MAP_ERYON_LIGA_CLASSIFICATORIA",
                         "MAP_ERYON_LIGA_RECUPERACAO",
                         "MAP_ERYON_LIGA_ELITE_FOUR"):
            self.assertIn(internal, seen)


if __name__ == "__main__":
    unittest.main()
