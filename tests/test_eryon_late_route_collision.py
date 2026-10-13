"""Physical accessibility regression for the Eryon late-game route chain.

Run from repository root:
    python3 -m unittest discover -s tests -p 'test_eryon_late_route_collision.py'

Reads *actual binary layout collision bits*, not only map JSON or scripts.
Checks two-way walk access and interaction with stationary NPCs. It cannot
prove in-game warp activation, sprite animation or every event state.
"""
import json
import unittest
from collections import deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAPS = ROOT / "data/maps"
LAYOUTS = ROOT / "data/layouts"
CHAIN = (
    "Eryon_Lunaris",
    "Eryon_TrilhaDosDragoes",
    "Eryon_VilaDoPico",
    "Eryon_Drakonia",
    "Eryon_GrutaDasEstrelas",
    "Eryon_CaminhoDaLiga",
    "Eryon_CidadeDaLiga",
)


def neighbors(point):
    x, y = point
    return (x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)


def flood(walkable, start, blocked):
    allowed = walkable - blocked
    if start not in allowed:
        return set()
    seen = {start}
    queue = deque((start,))
    while queue:
        for target in neighbors(queue.popleft()):
            if target in allowed and target not in seen:
                seen.add(target)
                queue.append(target)
    return seen


class EryonLateRouteCollision(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        entries = json.loads((LAYOUTS / "layouts.json").read_text(encoding="utf-8"))
        dims = {item["id"]: (item["width"], item["height"])
                for item in entries["layouts"]}
        cls.areas = {}
        for name in CHAIN:
            map_data = json.loads((MAPS / name / "map.json").read_text(encoding="utf-8"))
            width, height = dims[map_data["layout"]]
            blockdata = (LAYOUTS / name / "map.bin").read_bytes()
            if len(blockdata) != width * height * 2:
                raise AssertionError(f"Unexpected binary map dimensions: {name}")
            walkable = set()
            for y in range(height):
                for x in range(width):
                    start = 2 * (y * width + x)
                    cell = int.from_bytes(blockdata[start:start + 2], "little")
                    if (cell >> 10) & 3 == 0:
                        walkable.add((x, y))
            cls.areas[name] = (map_data, walkable)

    def test_warps_and_npcs_reachable_with_stationary_characters(self):
        for name, (area, walkable) in self.areas.items():
            with self.subTest(area=name):
                warps = area["warp_events"]
                self.assertGreaterEqual(len(warps), 2)
                blocked = {(obj["x"], obj["y"]) for obj in area["object_events"]}
                origin = (warps[0]["x"], warps[0]["y"])
                available = flood(walkable, origin, blocked)
                for warp in warps:
                    self.assertIn((warp["x"], warp["y"]), available,
                                  f"Inaccessible warp in {name}")
                for npc in area["object_events"]:
                    position = npc["x"], npc["y"]
                    self.assertIn(position, walkable,
                                  f"NPC on blocked cell in {name}: {npc['script']}")
                    self.assertTrue(
                        any(tile in available for tile in neighbors(position)),
                        f"Inaccessible NPC in {name}: {npc['script']}")
                for interaction in area["bg_events"]:
                    position = interaction["x"], interaction["y"]
                    # A sign/terminal may be mounted on a *blocked* wall.
                    # Accessibility depends on a walkable adjacent square.
                    self.assertTrue(
                        any(tile in available for tile in neighbors(position)),
                        f"Inaccessible interaction in {name}: {interaction['script']}")

    def test_neighboring_maps_have_return_warps(self):
        for left, right in zip(CHAIN, CHAIN[1:]):
            first = self.areas[left][0]
            second = self.areas[right][0]
            outbound = [(i, w) for i, w in enumerate(first["warp_events"])
                        if w["dest_map"] == second["id"]]
            self.assertTrue(outbound, f"No warp from {left} to {right}")
            for index, warp in outbound:
                back_id = int(warp["dest_warp_id"])
                self.assertLess(back_id, len(second["warp_events"]))
                return_warp = second["warp_events"][back_id]
                self.assertEqual(return_warp["dest_map"], first["id"])
                self.assertEqual(int(return_warp["dest_warp_id"]), index)

    def test_story_interactions_remain_on_accessible_maps(self):
        required = {
            "Eryon_TrilhaDosDragoes": "EryonDragoes_EventScript_SupplyCrate",
            "Eryon_VilaDoPico": "EryonPico_EventScript_RadioOperator",
            "Eryon_Drakonia": "EryonDrakonia_EventScript_SanctuaryHistorian",
            "Eryon_GrutaDasEstrelas": "EryonEstrelas_EventScript_RelayConsole",
            "Eryon_CaminhoDaLiga": "EryonLigaCaminho_EventScript_SupplyCache",
            "Eryon_CidadeDaLiga": "EryonCidadeLiga_EventScript_Investigator",
        }
        for name, label in required.items():
            with self.subTest(map=name, event=label):
                area = self.areas[name][0]
                events = area["object_events"] + area["bg_events"]
                self.assertIn(label, [item["script"] for item in events])
                source = (MAPS / name / "scripts.inc").read_text(encoding="utf-8")
                self.assertIn(label + "::", source)


if __name__ == "__main__":
    unittest.main()
