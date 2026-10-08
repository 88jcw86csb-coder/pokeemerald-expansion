#!/usr/bin/env python3
"""Unit tests for Eryon's post-build ROM header check."""
import tempfile
import unittest
from pathlib import Path

from eryon_rom_smoke import validate_rom


def header_rom():
    rom = bytearray(1024 * 1024)
    rom[:4] = bytes((0x00, 0x00, 0x00, 0xEA))
    rom[0xA0:0xA5] = b"ERYON"
    rom[0xAC:0xB0] = b"BPEE"
    rom[0xB2] = 0x96
    rom[0xC0:0xC4] = bytes((0x01, 0x02, 0x03, 0x04))
    rom[0xBD] = (-sum(rom[0xA0:0xBD]) - 0x19) & 0xFF
    return rom


class EryonRomSmokeTests(unittest.TestCase):
    def test_valid_header(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "test.gba"
            path.write_bytes(header_rom())
            size, digest = validate_rom(path)
            self.assertEqual(size, 1024 * 1024)
            self.assertEqual(len(digest), 64)

    def test_rom_identity_matches_makefile(self):
        makefile = (Path(__file__).resolve().parents[1] / "Makefile").read_text(encoding="utf-8")
        self.assertRegex(makefile, r"(?m)^TITLE\\s*\\?=\\s*ERYON\\s*$")
        self.assertRegex(makefile, r"(?m)^GAME_CODE\\s*\\?=\\s*BPEE\\s*$")
        self.assertRegex(makefile, r"(?m)^BUILD_NAME\\s*\\?=\\s*eryon\\s*$")

    def test_null_padded_eryon_title_is_accepted(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "eryon.gba"
            rom = header_rom()
            self.assertEqual(rom[0xA0:0xAC], b"ERYON" + b"\\x00" * 7)
            path.write_bytes(rom)
            size, _ = validate_rom(path)
            self.assertEqual(size, 1024 * 1024)

    def test_invalid_header_checksum(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.gba"
            rom = header_rom()
            rom[0xBD] ^= 1
            path.write_bytes(rom)
            with self.assertRaisesRegex(ValueError, "checksum"):
                validate_rom(path)

    def test_other_game_title_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "other.gba"
            rom = header_rom()
            rom[0xA0:0xA5] = b"OTHER"
            rom[0xBD] = (-sum(rom[0xA0:0xBD]) - 0x19) & 0xFF
            path.write_bytes(rom)
            with self.assertRaisesRegex(ValueError, "ROM title"):
                validate_rom(path)

    def test_other_game_code_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "wrong-code.gba"
            rom = header_rom()
            rom[0xAC:0xB0] = b"ABCD"
            rom[0xBD] = (-sum(rom[0xA0:0xBD]) - 0x19) & 0xFF
            path.write_bytes(rom)
            with self.assertRaisesRegex(ValueError, "game code"):
                validate_rom(path)

    def test_blank_zero_payload_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "empty-zero.gba"
            rom = header_rom()
            rom[0xC0:] = bytes(len(rom) - 0xC0)
            path.write_bytes(rom)
            with self.assertRaisesRegex(ValueError, "payload"):
                validate_rom(path)

    def test_blank_ff_payload_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "empty-ff.gba"
            rom = header_rom()
            rom[0xC0:] = bytes((0xFF,)) * (len(rom) - 0xC0)
            path.write_bytes(rom)
            with self.assertRaisesRegex(ValueError, "payload"):
                validate_rom(path)

    def test_header_only_file_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "truncated.gba"
            path.write_bytes(header_rom()[:192])
            with self.assertRaisesRegex(ValueError, "size"):
                validate_rom(path)

    def test_blank_entry_point_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "blank.gba"
            rom = header_rom()
            rom[:4] = b"\x00" * 4
            path.write_bytes(rom)
            with self.assertRaisesRegex(ValueError, "entry-point"):
                validate_rom(path)

    def test_missing_rom(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(ValueError, "not found"):
                validate_rom(Path(directory) / "missing.gba")


if __name__ == "__main__":
    unittest.main()
