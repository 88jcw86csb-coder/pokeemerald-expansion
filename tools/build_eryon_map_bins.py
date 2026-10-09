#!/usr/bin/env python3
"""Convert Eryon ASCII terrain plans into 48x44 GBA map blockdata.

The IDs below are provisional. Inspect metatiles in Porymap before declaring
these maps playable. Each tile is a little-endian 16-bit map entry.
"""
import argparse
import json
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPECS = {
    "passagem_rochosa": "PassagemRochosa",
    "estrada_oriental": "EstradaOriental",
    "vale_dos_ventos": "ValeDosVentos",
}
WIDTH, HEIGHT = 48, 44

def compile_plan(path, tile_ids):
    lines = path.read_text(encoding="utf-8").splitlines()
    rows = lines[4:]
    if any(len(line) != WIDTH or not set(line) <= set("#.,:") for line in rows):
        raise ValueError(f"{path}: invalid terrain symbol or row width")
    if len(rows) != HEIGHT:
        raise ValueError(f"{path}: expected {HEIGHT} rows of {WIDTH} symbols; got {len(rows)}")
    values = [tile_ids[symbol] for row in rows for symbol in row]
    return struct.pack(f"<{len(values)}H", *values)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wall", type=lambda s: int(s, 0), required=True,
                        help="impassable metatile word (including collision/elevation)")
    parser.add_argument("--path", type=lambda s: int(s, 0), required=True,
                        help="walkable path metatile word")
    parser.add_argument("--meadow", type=lambda s: int(s, 0), required=True,
                        help="walkable meadow metatile word")
    parser.add_argument("--stone", type=lambda s: int(s, 0), required=True,
                        help="walkable stone metatile word")
    parser.add_argument("--install-layouts", action="store_true",
                        help="update layouts.json paths after generating all binaries")
    args = parser.parse_args()
    tiles = dict(zip("#.,:", (args.wall, args.path, args.meadow, args.stone)))
    for key, value in tiles.items():
        if not 0 <= value <= 0xFFFF:
            parser.error(f"{key} metatile word must be 0..65535")
    generated = {}
    for key, folder in SPECS.items():
        src = ROOT / "docs/eryon" / f"{key}_terrain_plan.txt"
        dest = ROOT / "data/layouts" / f"Eryon_{folder}" / "map.bin"
        payload = compile_plan(src, tiles)
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(payload)
        generated[f"LAYOUT_ERYON_{key.upper()}"] = dest.relative_to(ROOT).as_posix()
        print(f"{dest.relative_to(ROOT)}: {len(payload)} bytes")
    if args.install_layouts:
        layouts_path = ROOT / "data/layouts/layouts.json"
        data = json.loads(layouts_path.read_text(encoding="utf-8"))
        installed = set()
        for layout in data["layouts"]:
            layout_id = layout["id"]
            if layout_id in generated:
                layout["blockdata_filepath"] = generated[layout_id]
                installed.add(layout_id)
        if installed != set(generated):
            raise ValueError(f"Missing layout registrations: {set(generated) - installed}")
        layouts_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print("Updated data/layouts/layouts.json with generated map paths")

if __name__ == "__main__":
    main()
