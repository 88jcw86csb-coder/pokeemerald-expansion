#!/usr/bin/env python3
"""Unit tests for Eryon's post-build ROM header check."""
import tempfile
import unittest
from pathlib import Path

from eryon_rom_smoke import validate_rom


def header_rom():
    rom = bytearray(192)
    rom[0xB2] = 0x96
    rom[0xBD] = (-sum(rom[0xA0:0xBD]) - 0x19) & 0xFF
    return rom


class EryonRomSmokeTests(unittest.TestCase):
    def test_valid_header(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "test.gba"
            path.write_bytes(header_rom())
            size, digest = validate_rom(path)
            self.assertEqual(size, 192)
            self.assertEqual(len(digest), 64)

    def test_invalid_header_checksum(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.gba"
            rom = header_rom()
            rom[0xBD] ^= 1
            path.write_bytes(rom)
            with self.assertRaisesRegex(ValueError, "checksum"):
                validate_rom(path)

    def test_missing_rom(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(ValueError, "not found"):
                validate_rom(Path(directory) / "missing.gba")


if __name__ == "__main__":
    unittest.main()
