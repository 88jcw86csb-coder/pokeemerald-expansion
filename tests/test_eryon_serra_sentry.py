"""Crystal Serra optional Eclipse sentry and four-exit map progression regression.

Run from repository root:
    python3 -m unittest discover -s tests -p 'test_eryon_serra_sentry.py' -v

Structural tests; a successful ROM build and emulator play remain necessary.
"""
import json
import re
import unittest
from collections import deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SERRA = ROOT / "data/maps/Eryon_SerraDosCristais"
PASSAGE = ROOT / "data/maps/Eryon_PassagemRochosa"
ARKHARA = ROOT / "data/maps/Eryon_Arkhara"
W, H = 48, 44
TRAINER = "TRAINER_ERYON_SERRA_CORE_GUARD"
GUARD_FLAG = "FLAG_ERYON_SERRA_CORE_GUARD_DEFEATED"
CORE_FLAG = "FLAG_ERYON_SERRA_ECLIPSE_SIGNAL_DISABLED"
NORTH_FLAG = "FLAG_ERYON_SERRA_NORTH_CRYSTAL_CALIBRATED"
SOUTH_FLAG = "FLAG_ERYON_SERRA_SOUTH_CRYSTAL_CALIBRATED"


def neighbors(x, y):
    return ((x+1, y), (x-1, y), (x, y+1), (x, y-1))


class SerraSentry(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.world = json.loads((SERRA / "map.json").read_text(encoding="utf-8"))
        cls.script = (SERRA / "scripts.inc").read_text(encoding="utf-8")
        data = (ROOT / "data/layouts/Eryon_SerraDosCristais/map.bin").read_bytes()
        assert len(data) == W * H * 2, "Unexpected map size"
        cls.walkable = set()
        for y in range(H):
            for x in range(W):
                at = 2*(y*W+x)
                metatile = int.from_bytes(data[at:at+2], "little")
                if ((metatile >> 10) & 3) == 0:
                    cls.walkable.add((x, y))

    def test_cliff_alcove_and_every_route_exit_are_reachable(self):
        world = self.world
        guards = [o for o in world["object_events"]
                  if o["script"] == "EryonSerra_EventScript_CoreGuardian"]
        self.assertEqual(len(guards), 1)
        self.assertEqual((guards[0]["x"], guards[0]["y"]), (36, 16))
        occupied = {(o["x"], o["y"]) for o in world["object_events"]}
        entry = world["warp_events"][0]
        origin = entry["x"], entry["y"]
        reachable = {origin}
        queue = deque([origin])
        while queue:
            x, y = queue.popleft()
            for tile in neighbors(x, y):
                if tile in self.walkable and tile not in occupied and tile not in reachable:
                    reachable.add(tile)
                    queue.append(tile)
        self.assertEqual(len(world["warp_events"]), 4)
        for warp in world["warp_events"]:
            self.assertIn((warp["x"], warp["y"]), reachable)
        for npc in world["object_events"]:
            pt = npc["x"], npc["y"]
            self.assertIn(pt, self.walkable, npc["script"])
            self.assertTrue(any(p in reachable for p in neighbors(*pt)),
                            f"NPC not reachable: {npc['script']}")
        for sign in world["bg_events"]:
            pt = sign["x"], sign["y"]
            self.assertTrue(any(p in reachable for p in neighbors(*pt)),
                            f"Sign not reachable: {sign['script']}")
        self.assertGreaterEqual(len(self.walkable), 1583)

    def test_guard_has_unique_save_flag_and_level_appropriate_team(self):
        flags = (ROOT / "include/constants/flags.h").read_text(encoding="utf-8")
        opponents = (ROOT / "include/constants/opponents.h").read_text(encoding="utf-8")
        setup = (ROOT / "src/battle_setup.c").read_text(encoding="utf-8")
        party = (ROOT / "src/data/trainers.party").read_text(encoding="utf-8")
        self.assertIn(f"#define {GUARD_FLAG} 0x28", flags)
        self.assertIn(f"#define {TRAINER} 888", opponents)
        self.assertRegex(opponents, r"(?m)^#define TRAINERS_COUNT_EMERALD\s+890$")
        self.assertIn(f"if (trainerId == {TRAINER})", setup)
        self.assertIn(f"return {GUARD_FLAG};", setup)
        self.assertEqual(len(re.findall(rf"(?m)^=== {TRAINER} ===$", party)), 1)
        team = party.split(f"=== {TRAINER} ===", 1)[1]
        for species, level in (("Nosepass", 32), ("Golbat", 33), ("Klang", 34)):
            self.assertRegex(team, rf"(?m)^{species}\nLevel: {level}$")

    def test_seals_unlock_battle_and_battle_unlocks_core(self):
        script = self.script
        self.assertIn(f"goto_if_unset {NORTH_FLAG}, "
                      "EryonSerra_EventScript_GuardianWaiting", script)
        self.assertIn(f"goto_if_unset {SOUTH_FLAG}, "
                      "EryonSerra_EventScript_GuardianWaiting", script)
        self.assertIn(
            f"trainerbattle_single {TRAINER},", script,
        )
        self.assertIn("MSGBOX_YESNO", script)
        self.assertIn(
            f"goto_if_unset {GUARD_FLAG}, EryonSerra_EventScript_CoreStillGuarded",
            script,
        )
        self.assertIn(
            f"goto_if_unset {NORTH_FLAG}, EryonSerra_EventScript_CoreNeedsSeals",
            script,
        )
        self.assertIn(
            f"goto_if_unset {SOUTH_FLAG}, EryonSerra_EventScript_CoreNeedsSeals",
            script,
        )
        self.assertIn(f"setflag {CORE_FLAG}", script)

    def test_road_and_city_acknowledge_battle_and_shutdown(self):
        passage = (PASSAGE / "scripts.inc").read_text(encoding="utf-8")
        city = (ARKHARA / "scripts.inc").read_text(encoding="utf-8")
        self.assertIn(
            f"goto_if_set {GUARD_FLAG}, "
            "EryonPassagem_EventScript_GuardSerraSentryDefeated", passage)
        self.assertIn(
            f"goto_if_set {GUARD_FLAG}, "
            "EryonArkhara_EventScript_GeologistGuardDefeated", city)
        for src in (passage, city):
            self.assertIn(CORE_FLAG, src)
        self.assertIn("giveitem ITEM_PP_UP", city)
        self.assertIn("FLAG_ERYON_SERRA_SURVEY_REWARD_CLAIMED", city)


if __name__ == "__main__":
    unittest.main()
