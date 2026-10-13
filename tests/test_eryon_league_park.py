"""League city garden collision and optional Kalos Espurr event contract.

Run from the repository root:
    python3 -m unittest discover -s tests -p 'test_eryon_league_park.py'

These are structural checks, not a GBA ROM build or emulator playthrough.
"""
import json
import unittest
from collections import deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CITY = ROOT / "data/maps/Eryon_CidadeDaLiga"
ROAD = ROOT / "data/maps/Eryon_CaminhoDaLiga"
WIDTH, HEIGHT = 96, 72
ESPURR_FLAG = "FLAG_ERYON_LEAGUE_PARK_ESPURR_RESOLVED"
REWARD_FLAG = "FLAG_ERYON_LEAGUE_PARK_REWARD_CLAIMED"


def neighbors(point):
    x, y = point
    return ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1))


class LeagueParkTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.map = json.loads((CITY / "map.json").read_text(encoding="utf-8"))
        cls.script = (CITY / "scripts.inc").read_text(encoding="utf-8")
        raw = (ROOT / "data/layouts/Eryon_CidadeDaLiga/map.bin").read_bytes()
        assert len(raw) == WIDTH * HEIGHT * 2, "Unexpected League City map dimensions"
        cls.walkable = set()
        for y in range(HEIGHT):
            for x in range(WIDTH):
                at = 2 * (y * WIDTH + x)
                word = int.from_bytes(raw[at:at + 2], "little")
                if ((word >> 10) & 3) == 0:
                    cls.walkable.add((x, y))

    def test_new_garden_reachable_without_crossing_npcs(self):
        botanists = [o for o in self.map["object_events"]
                     if o["script"] == "EryonCidadeLiga_EventScript_ParkBotanist"]
        nests = [o for o in self.map["bg_events"]
                 if o["script"] == "EryonCidadeLiga_EventScript_ParkEspurr"]
        self.assertEqual(len(botanists), 1)
        self.assertEqual(len(nests), 1)
        self.assertEqual((botanists[0]["x"], botanists[0]["y"]), (71, 46))
        self.assertEqual((nests[0]["x"], nests[0]["y"]), (67, 49))
        first_warp = self.map["warp_events"][0]
        start = (first_warp["x"], first_warp["y"])
        npcs = {(o["x"], o["y"]) for o in self.map["object_events"]}
        visited = {start}
        queue = deque([start])
        while queue:
            for p in neighbors(queue.popleft()):
                if p in self.walkable and p not in npcs and p not in visited:
                    visited.add(p)
                    queue.append(p)
        self.assertTrue(any(p in visited for p in neighbors((71, 46))))
        self.assertTrue(any(p in visited for p in neighbors((67, 49))))
        for warp in self.map["warp_events"]:
            self.assertIn((warp["x"], warp["y"]), visited)
        for npc in self.map["object_events"]:
            self.assertTrue(any(p in visited for p in neighbors((npc["x"], npc["y"]))))
        for event in self.map["bg_events"]:
            self.assertTrue(any(p in visited for p in neighbors((event["x"], event["y"]))))

    def test_encounter_depends_on_disabled_eclipse_relay(self):
        flags = (ROOT / "include/constants/flags.h").read_text(encoding="utf-8")
        species = (ROOT / "include/constants/species.h").read_text(encoding="utf-8")
        self.assertIn(f"#define {ESPURR_FLAG} 0x4B", flags)
        self.assertIn("SPECIES_ESPURR", species)
        self.assertIn("setwildbattle SPECIES_ESPURR, 47", self.script)
        self.assertIn(
            "goto_if_unset FLAG_ERYON_STAR_GROTTO_RELAY_DISABLED, "
            "EryonCidadeLiga_EventScript_ParkEspurrDisturbed", self.script)
        self.assertIn("goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, "
                      "EryonCidadeLiga_EventScript_ParkEspurrResolved", self.script)
        self.assertIn("goto_if_eq VAR_RESULT, B_OUTCOME_WON, "
                      "EryonCidadeLiga_EventScript_ParkEspurrResolved", self.script)
        self.assertIn("goto_if_eq VAR_RESULT, B_OUTCOME_RAN, "
                      "EryonCidadeLiga_EventScript_ParkEspurrEscaped", self.script)
        self.assertIn(f"setflag {ESPURR_FLAG}", self.script)

    def test_botanist_reward_is_unique_and_full_bag_safe(self):
        flags = (ROOT / "include/constants/flags.h").read_text(encoding="utf-8")
        items = (ROOT / "include/constants/items.h").read_text(encoding="utf-8")
        self.assertIn(f"#define {REWARD_FLAG} 0x4C", flags)
        self.assertIn("ITEM_DAWN_STONE", items)
        self.assertIn(f"goto_if_unset {ESPURR_FLAG}, "
                      "EryonCidadeLiga_EventScript_ParkResearchPending", self.script)
        self.assertIn("giveitem ITEM_DAWN_STONE", self.script)
        self.assertIn("goto_if_eq VAR_RESULT, FALSE, "
                      "EryonCidadeLiga_EventScript_ParkBagFull", self.script)
        self.assertIn(f"setflag {REWARD_FLAG}", self.script)
        self.assertIn(f"goto_if_set {REWARD_FLAG}, "
                      "EryonCidadeLiga_EventScript_ParkRewardDone", self.script)

    def test_league_road_responds_to_city_recovery(self):
        road = (ROAD / "scripts.inc").read_text(encoding="utf-8")
        self.assertIn("goto_if_set FLAG_ERYON_LEAGUE_PARK_ESPURR_RESOLVED, "
                      "EryonLigaCaminho_EventScript_ObserverParkRestored", road)
        self.assertIn("EryonLigaCaminho_EventScript_ObserverParkRestored::", road)


if __name__ == "__main__":
    unittest.main()
