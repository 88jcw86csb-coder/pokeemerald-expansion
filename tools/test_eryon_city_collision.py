"""Regression for checked-in city terrain of Eryon's registered gyms.

This tests map bits and event reachability. It cannot verify Delta gameplay,
tileset art, collision behaviors or the result of an ARM ROM compilation.
"""
import json
import struct
import unittest
from collections import deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CITIES = ("Neonara", "Frostheim", "Arkhara", "Umbra", "Ignivar", "Drakonia")
W, H = 64, 56
WORDS = {
    "#": 0x3C01, ".": 0x3001, "=": 0x3001, ",": 0x3002,
    ":": 0x3003, "G": 0x3001, "C": 0x3001, "M": 0x3001,
    "H": 0x3001, "P": 0x3001,
}


def load_city(city):
    plan = (ROOT / "docs/eryon/cidades" / (city.lower() + "_city_plan.txt"))
    rows = plan.read_text(encoding="utf-8").splitlines()[4:]
    binary = (ROOT / "data/layouts" / ("Eryon_" + city) / "map.bin").read_bytes()
    info = json.loads((ROOT / "data/maps" / ("Eryon_" + city) / "map.json").read_text(
        encoding="utf-8"))
    return rows, binary, info


def traversable_from_west(rows, info):
    walk = {(x, y) for y, row in enumerate(rows) for x, symbol in enumerate(row)
            if symbol != "#"}
    blockers = {(e["x"], e["y"]) for e in info["object_events"]}
    entrance = info["warp_events"][0]
    start = (entrance["x"], entrance["y"])
    if start not in walk or start in blockers:
        return set()
    reached = {start}
    queue = deque([start])
    while queue:
        x, y = queue.popleft()
        for tile in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
            if tile in walk and tile not in blockers and tile not in reached:
                reached.add(tile)
                queue.append(tile)
    return reached


class EryonCityCollisionTests(unittest.TestCase):
    def test_binary_exactly_matches_authoritative_city_plan(self):
        for city in CITIES:
            with self.subTest(city=city):
                rows, data, _ = load_city(city)
                self.assertEqual(len(rows), H)
                self.assertTrue(all(len(row) == W for row in rows))
                self.assertEqual(len(data), W * H * 2)
                blocks = struct.unpack("<" + str(W * H) + "H", data)
                self.assertGreater(sum(bool(v & 0x0C00) for v in blocks), 2000)
                for y, row in enumerate(rows):
                    for x, symbol in enumerate(row):
                        self.assertEqual(blocks[y * W + x], WORDS[symbol],
                                         (city, x, y))

    def test_travel_and_events_remain_accessible_with_stationary_npcs(self):
        for city in CITIES:
            with self.subTest(city=city):
                rows, _, info = load_city(city)
                reached = traversable_from_west(rows, info)
                self.assertTrue(reached)
                for event in info["warp_events"] + info["bg_events"]:
                    self.assertIn((event["x"], event["y"]), reached,
                                  (city, event))
                for npc in info["object_events"]:
                    x, y = npc["x"], npc["y"]
                    self.assertTrue(
                        any((x+dx, y+dy) in reached for dx, dy in
                            ((1, 0), (-1, 0), (0, 1), (0, -1))),
                        (city, "unreachable NPC", npc["script"]),
                    )

    def test_all_event_locations_unique_and_gym_landmark_reachable(self):
        for city in CITIES:
            with self.subTest(city=city):
                rows, _, info = load_city(city)
                events = (info["object_events"] + info["bg_events"] +
                          info["warp_events"])
                points = [(event["x"], event["y"]) for event in events]
                self.assertEqual(len(points), len(set(points)), city)
                self.assertIn((32, 11), traversable_from_west(rows, info),
                              (city, "gym district unreachable"))


if __name__ == "__main__":
    unittest.main()
