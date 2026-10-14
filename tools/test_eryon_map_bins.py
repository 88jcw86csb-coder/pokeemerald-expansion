#!/usr/bin/env python3
"""Unit tests for the Eryon GBA terrain encoder."""
import struct
import tempfile
import unittest
from pathlib import Path
from build_eryon_map_bins import WIDTH, HEIGHT, compile_plan

class TerrainCompilerTests(unittest.TestCase):
    def test_output_size_and_order(self):
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / "map.txt"
            rows = ["." * WIDTH for _ in range(HEIGHT)]
            rows[0] = "#,:." + "." * (WIDTH - 4)
            source.write_text("name\nlegend\nstatus\n\n" + "\n".join(rows) + "\n", encoding="utf-8")
            payload = compile_plan(source, {"#": 0x3C01, ".": 0x3001, ",": 0x3002, ":": 0x3003})
            self.assertEqual(len(payload), WIDTH * HEIGHT * 2)
            self.assertEqual(struct.unpack_from("<4H", payload), (0x3C01, 0x3002, 0x3003, 0x3001))

    def test_registered_league_city_dimensions(self):
        source = Path(__file__).resolve().parents[1] / "docs/eryon/liga_eryon_terrain_plan.txt"
        tiles = {"#": 0x3C01, ".": 0x3001, ",": 0x3002,
                 "L": 0x3001}
        payload = compile_plan(source, tiles, width=96, height=72)
        self.assertEqual(len(payload), 96 * 72 * 2)

    def test_village_and_city_concepts_encode_to_expected_sizes(self):
        root = Path(__file__).resolve().parents[1]
        village_tiles = {"#": 0x3C01, ".": 0x3001, ",": 0x3002,
                         ":": 0x3003, **dict.fromkeys("PCMHI", 0x3001)}
        city_tiles = {"#": 0x3C01, "=": 0x3001, ",": 0x3002, ":": 0x3003,
                      **dict.fromkeys("GCMHP", 0x3001)}
        for name in ("vila_dos_pomares", "vila_do_pico"):
            with self.subTest(village=name):
                path = root / "docs/eryon/vilas" / f"{name}_village_plan.txt"
                self.assertEqual(len(compile_plan(path, village_tiles, 36, 30)), 2160)
        for name in ("neonara", "drakonia"):
            with self.subTest(city=name):
                path = root / "docs/eryon/cidades" / f"{name}_city_plan.txt"
                self.assertEqual(len(compile_plan(path, city_tiles, 64, 56)), 7168)

    def test_league_road_eastern_summit_alcove_is_connected(self):
        root = Path(__file__).resolve().parents[1]
        source = root / "docs/eryon/caminho_da_liga_terrain_plan.txt"
        tiles = {"#": 0x3C01, ".": 0x3001, ":": 0x3003,
                 **dict.fromkeys("PCMLH", 0x3001)}
        binary = compile_plan(source, tiles)
        self.assertEqual(len(binary), 48 * 44 * 2)
        for y in (12, 13, 14):
            for x in range(35, 40):
                word = struct.unpack_from("<H", binary, 2 * (y * 48 + x))[0]
                self.assertEqual(word, 0x3003, (x, y))
        self.assertEqual(struct.unpack_from("<H", binary, 2 * (15 * 48 + 38))[0],
                         0x3003)

    def test_rejects_incomplete_plan(self):
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / "bad.txt"
            source.write_text("name\nlegend\nstatus\n\n" + "." * WIDTH + "\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                compile_plan(source, {"#": 0, ".": 1, ",": 2, ":": 3})

if __name__ == "__main__":
    unittest.main()
