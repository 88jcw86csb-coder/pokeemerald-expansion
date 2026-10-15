"""Eryon whiteout checkpoints: native heal-location IDs and safe map positions.

Checks repo data, not emulator save/whiteout behavior or successful ARM compilation.
"""
import json
import struct
import unittest
from collections import deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKPOINTS = {
    "VilaAurora": ("VILA_AURORA", 10, 10),
    "Verdelume": ("VERDELUME", 4, 30),
    "Neonara": ("NEONARA", 4, 28),
    "Frostheim": ("FROSTHEIM", 4, 12),
    "Arkhara": ("ARKHARA", 15, 20),
    "Umbra": ("UMBRA", 4, 12),
    "Ignivar": ("IGNIVAR", 4, 28),
    "Lunaris": ("LUNARIS", 19, 29),
    "Drakonia": ("DRAKONIA", 14, 21),
    "CidadeDaLiga": ("CIDADE_DA_LIGA", 30, 36),
    "LigaRecepcao": ("LIGA_RECEPCAO", 12, 12),
    "VilaDosPomares": ("VILA_DOS_POMARES", 4, 14),
    "VilaDaNeblina": ("VILA_DA_NEBLINA", 4, 14),
    "VilaDasAguas": ("VILA_DAS_AGUAS", 4, 13),
    "AldeiaDosEcos": ("ALDEIA_DOS_ECOS", 4, 14),
    "VilaDoPico": ("VILA_DO_PICO", 4, 14),
}


class EryonWhiteoutCheckpoints(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        heal = json.loads((ROOT / "src/data/heal_locations.json").read_text(
            encoding="utf-8"))["heal_locations"]
        cls.heal = {entry["id"]: entry for entry in heal}
        cls.all_heal = heal
        cls.layouts = {
            item["id"]: item
            for item in json.loads((ROOT / "data/layouts/layouts.json").read_text(
                encoding="utf-8"))["layouts"]
        }

    def test_sixteen_locations_are_unique_and_use_eryon_maps(self):
        self.assertEqual(len(CHECKPOINTS), 16)
        keys = [entry["id"] for entry in self.all_heal]
        self.assertEqual(len(keys), len(set(keys)))
        eryon = [entry for entry in self.all_heal
                 if entry["id"].startswith("HEAL_LOCATION_ERYON_")]
        self.assertEqual(len(eryon), len(CHECKPOINTS))
        for name, (map_part, x, y) in CHECKPOINTS.items():
            with self.subTest(map=name):
                entry = self.heal["HEAL_LOCATION_ERYON_" + map_part]
                self.assertEqual(entry["map"], "MAP_ERYON_" + map_part)
                self.assertEqual((entry["x"], entry["y"]), (x, y))
                self.assertEqual(entry["respawn_map"], entry["map"])
                self.assertEqual((entry["respawn_x"], entry["respawn_y"]), (x, y))
                self.assertEqual(entry["respawn_npc"], "LOCALID_NONE")

    def test_every_checkpoint_uses_existing_transition_script(self):
        for name, (map_part, _, _) in CHECKPOINTS.items():
            with self.subTest(map=name):
                script = (ROOT / "data/maps" / ("Eryon_" + name)
                          / "scripts.inc").read_text(encoding="utf-8")
                label = "Eryon_" + name + "_RespawnCheckpoint"
                self.assertIn("map_script MAP_SCRIPT_ON_TRANSITION, " + label,
                              script)
                self.assertEqual(script.count(label + ":"), 1)
                self.assertIn("setrespawn HEAL_LOCATION_ERYON_" + map_part, script)
                self.assertIn(label + ":\n\tsetrespawn "
                              "HEAL_LOCATION_ERYON_" + map_part + "\n\tend",
                              script)

    def test_all_respawn_tiles_are_walkable_and_reachable(self):
        for name, (_, x, y) in CHECKPOINTS.items():
            with self.subTest(map=name):
                world = json.loads((ROOT / "data/maps" / ("Eryon_" + name)
                                    / "map.json").read_text(encoding="utf-8"))
                layout = self.layouts[world["layout"]]
                width, height = layout["width"], layout["height"]
                binary = (ROOT / layout["blockdata_filepath"]).read_bytes()
                self.assertEqual(len(binary), 2 * width * height)
                blocks = struct.unpack("<" + str(width * height) + "H", binary)
                floor = {(cx, cy) for cy in range(height) for cx in range(width)
                         if not ((blocks[cy * width + cx] >> 10) & 3)}
                forbidden = {(obj["x"], obj["y"])
                             for kind in ("object_events", "bg_events", "warp_events")
                             for obj in world[kind]}
                self.assertIn((x, y), floor)
                self.assertNotIn((x, y), forbidden)
                npcs = {(obj["x"], obj["y"]) for obj in world["object_events"]}
                if world["warp_events"]:
                    entry = world["warp_events"][0]
                    start = (entry["x"], entry["y"])
                else:
                    # Starting town: Riolu's new-game spawn.
                    self.assertEqual(name, "VilaAurora")
                    start = (10, 10)
                visited, queue = {start}, deque([start])
                while queue:
                    px, py = queue.popleft()
                    for pos in ((px-1, py), (px+1, py), (px, py-1), (px, py+1)):
                        if pos in floor and pos not in npcs and pos not in visited:
                            visited.add(pos)
                            queue.append(pos)
                self.assertIn((x, y), visited)

    def test_engine_uses_native_setrespawn_and_no_hoenn_healer(self):
        macros = (ROOT / "asm/macros/event.inc").read_text(encoding="utf-8")
        overworld = (ROOT / "src/overworld.c").read_text(encoding="utf-8")
        engine = (ROOT / "src/heal_location.c").read_text(encoding="utf-8")
        generated = (ROOT / "src/data/heal_locations.json.txt").read_text(
            encoding="utf-8")
        self.assertIn(".macro setrespawn heallocation:req", macros)
        self.assertIn("SetLastHealLocationWarp(u8 healLocationId)", overworld)
        self.assertIn("sWarpDestination = gSaveBlock1Ptr->lastHealLocation", overworld)
        self.assertIn("*(warp) = gSaveBlock1Ptr->lastHealLocation", engine)
        self.assertIn("{{ heal_location.id }}", generated)

    def test_qualification_whiteout_keeps_league_lobby_checkpoint(self):
        lobby = (ROOT / "data/maps/Eryon_LigaRecepcao/scripts.inc").read_text()
        qual = (ROOT / "data/maps/Eryon_LigaClassificatoria/scripts.inc").read_text()
        self.assertIn("setrespawn HEAL_LOCATION_ERYON_LIGA_RECEPCAO", lobby)
        self.assertIn("warp MAP_ERYON_LIGA_CLASSIFICATORIA, 22, 30", lobby)
        self.assertIn("goto_if_set FLAG_ERYON_QUALIFIED", qual)
        for index in range(1, 9):
            self.assertIn("clearflag FLAG_ERYON_QUALIFIER_ROUND_" + str(index),
                          qual)
            self.assertIn("cleartrainerflag TRAINER_ERYON_QUALIFIER_" + str(index),
                          qual)


if __name__ == "__main__":
    unittest.main()
