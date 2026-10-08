#!/usr/bin/env python3
"""Check that an Eryon build produced a structurally plausible GBA ROM.

This does not replace emulator testing or verify map collision.
"""
import argparse
import hashlib
from pathlib import Path


def validate_rom(path):
    if not path.is_file():
        raise ValueError(f"ROM not found: {path}")
    size = path.stat().st_size
    if not 1024 * 1024 <= size <= 32 * 1024 * 1024:
        raise ValueError(f"Invalid GBA ROM size: {size} bytes")
    with path.open("rb") as rom:
        header = rom.read(0xC0)
    # A 192-byte header alone is not a playable cartridge image.
    # Reject blank/truncated outputs even if their header checksum is forged.
    if header[:4] == b"\x00" * 4 or header[:4] == b"\xff" * 4:
        raise ValueError("Missing GBA entry-point instructions")
    if not all(0x20 <= byte <= 0x7E for byte in header[0xAC:0xB0]):
        raise ValueError("Invalid GBA game code in header")
    if header[0xB2] != 0x96:
        raise ValueError("Invalid GBA fixed header value at 0xB2")
    expected = (-sum(header[0xA0:0xBD]) - 0x19) & 0xFF
    if header[0xBD] != expected:
        raise ValueError(
            f"Invalid GBA header checksum: found {header[0xBD]:02X}, expected {expected:02X}"
        )
    digest = hashlib.sha256()
    with path.open("rb") as rom:
        for chunk in iter(lambda: rom.read(1024 * 1024), b""):
            digest.update(chunk)
    return size, digest.hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("rom", type=Path, nargs="?", default=Path("pokeeryon.gba"))
    args = parser.parse_args()
    try:
        size, sha256 = validate_rom(args.rom)
    except ValueError as error:
        parser.exit(1, f"FAIL: {error}\n")
    print(f"PASS: GBA header and size: {args.rom} ({size} bytes)")
    print(f"SHA256: {sha256}")


if __name__ == "__main__":
    main()
