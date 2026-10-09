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

    def test_rejects_incomplete_plan(self):
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / "bad.txt"
            source.write_text("name\nlegend\nstatus\n\n" + "." * WIDTH + "\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                compile_plan(source, {"#": 0, ".": 1, ",": 2, ":": 3})

if __name__ == "__main__":
    unittest.main()
