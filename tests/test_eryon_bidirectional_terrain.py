"""Bidirectional collision-level regression across all 42 registered Eryon maps.

For each physical warp, the test explores the *actual stored blockdata* and
asserts that every other exit and scripted event tile belongs to its component.
This supplements map-level reachability checks with an every-entry guarantee.
It does not prove that the GBA engine triggers a warp or that Delta works.
"""
from collections import deque
import json
from pathlib import Path
import struct
import unittest

ROOT = Path(__file__).resolve().parents[1]


def walkable_component(words, width, height, start):
    def open_tile(x, y):
        return (0 <= x < width and 0 <= y < height
                and (words[y * width + x] & 0x0C00) == 0)

    if not open_tile(*start):
        return set()
    reached = {start}
    queue = deque([start])
    while queue:
        x, y = queue.popleft()
        for nx, ny in ((x + 1, y), (x - 1, y),
                       (x, y + 1), (x, y - 1)):
            if (nx, ny) not in reached and open_tile(nx, ny):
                reached.add((nx, ny))
                queue.append((nx, ny))
    return reached


class EryonBidirectionalTerrainTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        group = json.loads(
            (ROOT / "data/maps/map_groups.json").read_text()
        )["gMapGroup_Eryon"]
        cls.names = group
        cls.maps = {
            name: json.loads(
                (ROOT / "data/maps" / name / "map.json").read_text()
            )
            for name in group
        }
        cls.by_id = {m["id"]: name for name, m in cls.maps.items()}
        cls.layouts = {
            entry["id"]: entry
            for entry in json.loads(
                (ROOT / "data/layouts/layouts.json").read_text()
            )["layouts"]
        }

    def test_every_warp_arrival_can_reach_all_other_warps_and_events(self):
        self.assertEqual(len(self.names), 42)
        for name in self.names:
            map_data = self.maps[name]
            layout = self.layouts[map_data["layout"]]
            width, height = layout["width"], layout["height"]
            raw = (ROOT / layout["blockdata_filepath"]).read_bytes()
            with self.subTest(map=name, type="binary"):
                self.assertEqual(len(raw), width * height * 2)
            words = struct.unpack(f"<{width * height}H", raw)
            exits = map_data["warp_events"]
            for index, entry in enumerate(exits):
                arrival = (entry["x"], entry["y"])
                reachable = walkable_component(words, width, height, arrival)
                with self.subTest(map=name, warp=index, type="arrival"):
                    self.assertTrue(reachable, f"{name} entry warp {index} blocked")
                for destination_index, dest in enumerate(exits):
                    with self.subTest(map=name, warp=index, to_warp=destination_index):
                        self.assertIn(
                            (dest["x"], dest["y"]), reachable,
                            f"{name}: warp {index} cannot reach exit {destination_index}"
                        )
                for group in ("object_events", "bg_events", "coord_events"):
                    for event_index, event in enumerate(map_data[group]):
                        with self.subTest(map=name, warp=index,
                                          event_group=group, event=event_index):
                            self.assertIn(
                                (event["x"], event["y"]), reachable,
                                f"{name}: warp {index} cannot reach {group}[{event_index}]"
                            )

    def test_every_physical_warp_has_reciprocal_exit(self):
        for name in self.names:
            current = self.maps[name]
            for index, link in enumerate(current["warp_events"]):
                target_name = self.by_id.get(link["dest_map"])
                with self.subTest(map=name, warp=index):
                    self.assertIsNotNone(target_name)
                    target = self.maps[target_name]["warp_events"]
                    destination_index = int(link["dest_warp_id"])
                    self.assertGreaterEqual(destination_index, 0)
                    self.assertLess(destination_index, len(target))
                    reverse = target[destination_index]
                    self.assertEqual(reverse["dest_map"], current["id"])
                    self.assertEqual(int(reverse["dest_warp_id"]), index)

    def test_starting_town_and_route01_reversible_border(self):
        village = self.maps["Eryon_VilaAurora"]
        road = self.maps["Eryon_Rota01"]
        self.assertTrue(any(c["direction"] == "up" and
                            c["map"] == road["id"]
                            for c in village["connections"]))
        self.assertTrue(any(c["direction"] == "down" and
                            c["map"] == village["id"]
                            for c in road["connections"]))
        for name, entrance, exit_tile in (
            ("Eryon_VilaAurora", (10, 10), (10, 0)),
            ("Eryon_Rota01", (10, 19), (19, 10)),
        ):
            m = self.maps[name]
            layout = self.layouts[m["layout"]]
            w, h = layout["width"], layout["height"]
            raw = (ROOT / layout["blockdata_filepath"]).read_bytes()
            words = struct.unpack(f"<{w * h}H", raw)
            with self.subTest(map=name):
                reached = walkable_component(words, w, h, entrance)
                self.assertIn(exit_tile, reached)


if __name__ == "__main__":
    unittest.main()
