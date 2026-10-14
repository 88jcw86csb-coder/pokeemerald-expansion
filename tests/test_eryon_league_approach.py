"""Static accessibility and optional reward contract for the League approach.

Run from repository root:
    python3 -m unittest discover -s tests -p 'test_eryon_league_approach.py'

Inspects actual layout metatiles/collision flags and map events.
It does not replace a GBA build or emulator playthrough.
"""
import json
import unittest
from collections import deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAP_ROOT = ROOT / "data/maps"
LAYOUT_ROOT = ROOT / "data/layouts"
AREAS = {
    "Eryon_CaminhoDaLiga": (48, 44),
    "Eryon_CidadeDaLiga": (96, 72),
}


def neighbors(p):
    x, y = p
    return ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1))


def reachable_tiles(walkable, start, blockers):
    self_contained = walkable - blockers
    if start not in self_contained:
        return set()
    seen = {start}
    queue = deque([start])
    while queue:
        for point in neighbors(queue.popleft()):
            if point in self_contained and point not in seen:
                seen.add(point)
                queue.append(point)
    return seen


class EryonLeagueApproach(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.areas = {}
        for name, (w, h) in AREAS.items():
            map_data = json.loads((MAP_ROOT / name / "map.json").read_text(encoding="utf-8"))
            raw = (LAYOUT_ROOT / name / "map.bin").read_bytes()
            assert len(raw) == w * h * 2, f"Unexpected dimensions for {name}"
            walkable = set()
            for y in range(h):
                for x in range(w):
                    offset = 2 * (y * w + x)
                    word = int.from_bytes(raw[offset:offset + 2], "little")
                    # Pokeemerald metatile format: bits 10-11 = collision,
                    # bits 12-15 = elevation. Do not assume a single floor ID.
                    if (word >> 10) & 3 == 0:
                        walkable.add((x, y))
            cls.areas[name] = (map_data, walkable)

    def test_all_critical_events_can_be_reached(self):
        for name, (data, walkable) in self.areas.items():
            with self.subTest(map=name):
                warps = data["warp_events"]
                self.assertGreaterEqual(len(warps), 2)
                start = (warps[0]["x"], warps[0]["y"])
                blocked = {(n["x"], n["y"]) for n in data["object_events"]}
                reachable = reachable_tiles(walkable, start, blocked)
                for warp in warps:
                    self.assertIn((warp["x"], warp["y"]), reachable)
                for npc in data["object_events"]:
                    point = (npc["x"], npc["y"])
                    self.assertIn(point, walkable, npc["script"])
                    self.assertTrue(
                        any(adj in reachable for adj in neighbors(point)),
                        f"NPC inaccessible: {name}/{npc['script']}",
                    )
                for event in data["bg_events"]:
                    point = (event["x"], event["y"])
                    self.assertIn(point, walkable, event["script"])
                    self.assertTrue(
                        any(adj in reachable for adj in neighbors(point)),
                        f"Interaction inaccessible: {name}/{event['script']}",
                    )

    def test_league_building_is_in_central_city(self):
        data, walkable = self.areas["Eryon_CidadeDaLiga"]
        destination = [w for w in data["warp_events"]
                       if w["dest_map"] == "MAP_ERYON_LIGA_RECEPCAO"]
        self.assertEqual(len(destination), 1)
        self.assertEqual((destination[0]["x"], destination[0]["y"]), (48, 36))
        self.assertIn((48, 36), walkable)

    def test_optional_victory_reward_does_not_block_evidence_quest(self):
        script = (MAP_ROOT / "Eryon_CidadeDaLiga" / "scripts.inc").read_text(encoding="utf-8")
        flags = (ROOT / "include/constants/flags.h").read_text(encoding="utf-8")
        self.assertIn("#define FLAG_ERYON_GROTTO_SCOUT_REWARD_CLAIMED 0x43", flags)
        self.assertIn("giveitem ITEM_RARE_CANDY", script)
        self.assertIn("setflag FLAG_ERYON_GROTTO_SCOUT_REWARD_CLAIMED", script)
        self.assertIn(
            "goto_if_eq VAR_RESULT, FALSE, EryonCidadeLiga_EventScript_InvestigatorScoutRewardFull",
            script,
        )
        self.assertIn(
            "goto_if_set FLAG_ERYON_GROTTO_ECLIPSE_SCOUT_DEFEATED, "
            "EryonCidadeLiga_EventScript_InvestigatorScoutReward", script,
        )
        self.assertIn(
            "goto EryonCidadeLiga_EventScript_InvestigatorNormal", script,
        )
        self.assertIn(
            "goto_if_set FLAG_ERYON_DRAGON_TRAIL_MANIFEST_READ, "
            "EryonCidadeLiga_EventScript_InvestigatorManifest", script,
        )


    def test_league_road_story_priorities_and_existing_warps(self):
        script = (MAP_ROOT / "Eryon_CaminhoDaLiga" / "scripts.inc").read_text(encoding="utf-8")
        guardian = script.split("EryonLigaCaminho_EventScript_RouteGuardian::", 1)[1].split("EryonLigaCaminho_EventScript_Medic:", 1)[0]
        courier = script.split("EryonLigaCaminho_EventScript_LigaCourier::", 1)[1].split("EryonLigaCaminho_EventScript_LigaCourierAfter::", 1)[0]
        self.assertLess(
            guardian.index("goto_if_set FLAG_ERYON_CHAMPION_CROWNED"),
            guardian.index("goto_if_set FLAG_ERYON_QUALIFIED"),
        )
        self.assertLess(
            courier.index("goto_if_set FLAG_ERYON_CHAMPION_CROWNED"),
            courier.index("goto_if_set FLAG_ERYON_QUALIFIED"),
        )
        self.assertLess(
            courier.index("goto_if_set FLAG_ERYON_QUALIFIED"),
            courier.index("goto_if_set FLAG_ERYON_ECLIPSE_EVIDENCE_REPORTED"),
        )
        for label in (
            "GuardianChampion", "GuardianQualified",
            "LigaCourierChampion", "LigaCourierEvidence",
        ):
            self.assertIn("EryonLigaCaminho_EventScript_" + label + "::", script)
        road = self.areas["Eryon_CaminhoDaLiga"][0]
        self.assertEqual(road["warp_events"][0]["dest_map"], "MAP_ERYON_GRUTA_DAS_ESTRELAS")
        self.assertEqual(road["warp_events"][1]["dest_map"], "MAP_ERYON_CIDADE_DA_LIGA")


if __name__ == "__main__":
    unittest.main()
