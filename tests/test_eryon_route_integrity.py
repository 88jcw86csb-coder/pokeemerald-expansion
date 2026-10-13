"""Static integrity checks for the late-game Eryon route chain.

Run: python3 -m unittest discover -s tests -p 'test_eryon_route_integrity.py'
These are structural checks, NOT in-game collision or GBA compilation tests.
"""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAPS = ROOT / "data" / "maps"
CHAIN = [
    "Eryon_Lunaris",
    "Eryon_TrilhaDosDragoes",
    "Eryon_VilaDoPico",
    "Eryon_Drakonia",
    "Eryon_GrutaDasEstrelas",
    "Eryon_CaminhoDaLiga",
    "Eryon_CidadeDaLiga",
]
IDS = {
    "Eryon_Lunaris": "MAP_ERYON_LUNARIS",
    "Eryon_TrilhaDosDragoes": "MAP_ERYON_TRILHA_DOS_DRAGOES",
    "Eryon_VilaDoPico": "MAP_ERYON_VILA_DO_PICO",
    "Eryon_Drakonia": "MAP_ERYON_DRAKONIA",
    "Eryon_GrutaDasEstrelas": "MAP_ERYON_GRUTA_DAS_ESTRELAS",
    "Eryon_CaminhoDaLiga": "MAP_ERYON_CAMINHO_DA_LIGA",
    "Eryon_CidadeDaLiga": "MAP_ERYON_CIDADE_DA_LIGA",
}


class EryonRouteIntegrity(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.maps = {
            name: json.loads((MAPS / name / "map.json").read_text(encoding="utf-8"))
            for name in CHAIN
        }

    def test_each_map_has_unique_npc_positions_and_valid_scripts(self):
        for name, data in self.maps.items():
            with self.subTest(map=name):
                scripts = (MAPS / name / "scripts.inc").read_text(encoding="utf-8")
                events = data.get("object_events", [])
                positions = [(npc["x"], npc["y"]) for npc in events]
                self.assertEqual(len(positions), len(set(positions)))
                for npc in events:
                    self.assertIn(npc["script"] + "::", scripts)
                for sign in data.get("bg_events", []):
                    self.assertIn(sign["script"] + "::", scripts)

    def test_bidirectional_route_chain(self):
        for left, right in zip(CHAIN, CHAIN[1:]):
            with self.subTest(pair=f"{left} -> {right}"):
                left_warps = self.maps[left]["warp_events"]
                right_warps = self.maps[right]["warp_events"]
                forward = [(idx, w) for idx, w in enumerate(left_warps)
                           if w["dest_map"] == IDS[right]]
                backward = [(idx, w) for idx, w in enumerate(right_warps)
                            if w["dest_map"] == IDS[left]]
                self.assertTrue(forward, "Forward warp missing")
                self.assertTrue(backward, "Return warp missing")
                for index, warp in forward:
                    dest = int(warp["dest_warp_id"])
                    self.assertLess(dest, len(right_warps))
                    self.assertEqual(right_warps[dest]["dest_map"], IDS[left])
                    self.assertEqual(int(right_warps[dest]["dest_warp_id"]), index)
                for index, warp in backward:
                    dest = int(warp["dest_warp_id"])
                    self.assertLess(dest, len(left_warps))
                    self.assertEqual(left_warps[dest]["dest_map"], IDS[right])
                    self.assertEqual(int(left_warps[dest]["dest_warp_id"]), index)

    def test_league_road_supply_cache_does_not_consume_on_full_bag(self):
        data = self.maps["Eryon_CaminhoDaLiga"]
        script = (MAPS / "Eryon_CaminhoDaLiga" / "scripts.inc").read_text(encoding="utf-8")
        self.assertIn("EryonLigaCaminho_EventScript_SupplyCache",
                      [e["script"] for e in data["bg_events"]])
        self.assertIn("giveitem ITEM_MAX_POTION", script)
        self.assertIn("goto_if_eq VAR_RESULT, FALSE, EryonLigaCaminho_EventScript_CacheFull", script)
        self.assertIn("setflag FLAG_ERYON_LEAGUE_ROAD_CACHE_TAKEN", script)

    def test_league_city_aid_station_and_safe_lobby_warp(self):
        city = self.maps["Eryon_CidadeDaLiga"]
        scripts = (MAPS / "Eryon_CidadeDaLiga" / "scripts.inc").read_text(encoding="utf-8")
        lobby = (MAPS / "Eryon_LigaRecepcao" / "scripts.inc").read_text(encoding="utf-8")
        self.assertIn("EryonCidadeLiga_EventScript_AidStation",
                      [e["script"] for e in city["bg_events"]])
        self.assertIn("giveitem ITEM_FULL_RESTORE", scripts)
        self.assertIn("goto_if_eq VAR_RESULT, FALSE, EryonCidadeLiga_EventScript_AidFull", scripts)
        self.assertIn("setflag FLAG_ERYON_LEAGUE_CITY_AID_COLLECTED", scripts)
        self.assertIn("EryonLigaLobby_Text_Qualified, MSGBOX_DEFAULT\n\tclosemessage\n\twarp", lobby)


if __name__ == "__main__":
    unittest.main()
