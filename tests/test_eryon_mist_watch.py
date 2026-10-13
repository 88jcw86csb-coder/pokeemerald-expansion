"""Northern Eryon fog watch: physical map access and multi-city story contract.

Run from repository root:
    python3 -m unittest discover -s tests -p 'test_eryon_mist_watch.py' -v

These static tests do not replace in-game navigation or GBA compilation.
"""
import json
import unittest
from collections import deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAPS = ROOT / "data/maps"
LAYOUTS = ROOT / "data/layouts"
FLAG = "FLAG_ERYON_MIST_SIGNAL_REPAIRED"
SUPPLY_FLAG = "FLAG_ERYON_GLACIAL_SUPPLY_RETRIEVED"
LOCATIONS = ("Eryon_ColinasDaNeblina", "Eryon_TrilhaGlacial")
POINTS = {
    "Eryon_ColinasDaNeblina": ("EryonNeblinaColinas_EventScript_MistKeeper",
                               "EryonNeblinaColinas_EventScript_MistBeacon"),
    "Eryon_TrilhaGlacial": (None, "EryonTrilhaGlacial_EventScript_ResearchSupplies"),
}


def adjacent(point):
    x, y = point
    return ((x-1, y), (x+1, y), (x, y-1), (x, y+1))


class EryonMistWatch(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.maps = {}
        for name in LOCATIONS:
            world = json.loads((MAPS/name/"map.json").read_text(encoding="utf-8"))
            raw = (LAYOUTS/name/"map.bin").read_bytes()
            width, height = 48, 44
            assert len(raw) == width*height*2, name
            walkable = set()
            for y in range(height):
                for x in range(width):
                    pos = 2*(y*width+x)
                    value = int.from_bytes(raw[pos:pos+2], "little")
                    if ((value >> 10) & 3) == 0:
                        walkable.add((x, y))
            cls.maps[name] = (world, walkable)

    def test_both_routes_stay_traversable_and_events_accessible(self):
        for name in LOCATIONS:
            with self.subTest(route=name):
                map_data, floor = self.maps[name]
                npc_positions = {(o["x"], o["y"]) for o in map_data["object_events"]}
                start = (map_data["warp_events"][0]["x"],
                         map_data["warp_events"][0]["y"])
                visited = {start}
                pending = deque([start])
                while pending:
                    for target in adjacent(pending.popleft()):
                        if target in floor and target not in npc_positions and target not in visited:
                            visited.add(target)
                            pending.append(target)
                for warp in map_data["warp_events"]:
                    self.assertIn((warp["x"], warp["y"]), visited)
                for item in map_data["object_events"] + map_data["bg_events"]:
                    self.assertTrue(
                        any(point in visited for point in adjacent(
                            (item["x"], item["y"]))),
                        f"Inaccessible event: {name}/{item['script']}",
                    )
                npc, sign = POINTS[name]
                source = (MAPS/name/"scripts.inc").read_text(encoding="utf-8")
                if npc:
                    self.assertIn(npc, {x["script"] for x in map_data["object_events"]})
                    self.assertIn(npc + "::", source)
                self.assertIn(sign, {x["script"] for x in map_data["bg_events"]})
                self.assertIn(sign + "::", source)

    def test_signal_needs_neonara_badge_and_persists(self):
        script = (MAPS/LOCATIONS[0]/"scripts.inc").read_text(encoding="utf-8")
        flags = (ROOT/"include/constants/flags.h").read_text(encoding="utf-8")
        self.assertIn(f"#define {FLAG} 0x20", flags)
        self.assertIn(f"#define {SUPPLY_FLAG} 0x21", flags)
        self.assertIn(
            "goto_if_unset FLAG_BADGE02_GET, "
            "EryonNeblinaColinas_EventScript_BeaconNeedsBadge", script)
        self.assertIn(f"setflag {FLAG}", script)
        self.assertIn(f"goto_if_set {FLAG}, "
                      "EryonNeblinaColinas_EventScript_BeaconActive", script)
        self.assertIn("special HealPlayerParty", script)

    def test_glacial_reward_can_be_retried_with_full_bag(self):
        s = (MAPS/LOCATIONS[1]/"scripts.inc").read_text(encoding="utf-8")
        self.assertIn(
            f"goto_if_unset {FLAG}, EryonTrilhaGlacial_EventScript_SuppliesSealed",
            s)
        self.assertIn("giveitem ITEM_SUPER_POTION", s)
        self.assertIn(
            "goto_if_eq VAR_RESULT, FALSE, EryonTrilhaGlacial_EventScript_SuppliesFull",
            s)
        self.assertIn(f"setflag {SUPPLY_FLAG}", s)
        self.assertLess(
            s.index("goto_if_eq VAR_RESULT, FALSE, EryonTrilhaGlacial_EventScript_SuppliesFull"),
            s.index(f"setflag {SUPPLY_FLAG}"),
        )

    def test_story_follows_player_across_cities(self):
        scenarios = (
            ("Eryon_Neonara", "EryonNeonara_EventScript_TechnicianRestored"),
            ("Eryon_VilaDaNeblina", "EryonVilaNeblina_EventScript_ElderSignal"),
            ("Eryon_Frostheim", "EryonFrostheim_EventScript_ResearcherSignal"),
        )
        for city, label in scenarios:
            with self.subTest(city=city):
                src = (MAPS/city/"scripts.inc").read_text(encoding="utf-8")
                self.assertIn(
                    f"goto_if_set {FLAG}, {label}", src)
                self.assertIn(label+"::", src)


if __name__ == "__main__":
    unittest.main()
