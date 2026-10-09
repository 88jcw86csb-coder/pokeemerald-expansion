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
    "bosque_de_lumina": "BosqueDeLumina",
    "serra_dos_cristais": "SerraDosCristais",
    "passagem_rochosa": "PassagemRochosa",
    "estrada_oriental": "EstradaOriental",
    "vale_dos_ventos": "ValeDosVentos",
    "estrada_dos_pomares": "EstradaDosPomares",
}
PREVIEW_SPECS = {
    "rota_das_cachoeiras": "RotaDasCachoeiras",
    "deserto_de_solaris": "DesertoDeSolaris",
    "floresta_dos_ecos": "FlorestaDosEcos",
    "colinas_da_neblina": "ColinasDaNeblina",
    "trilha_glacial": "TrilhaGlacial",
    "trilha_dos_dragoes": "TrilhaDosDragoes",
    "trilha_lunar": "TrilhaLunar",
    "trilha_do_oasis": "TrilhaDoOasis",
    "caminho_da_liga": "CaminhoDaLiga",
    "gruta_das_estrelas": "GrutaDasEstrelas",
}
WIDTH, HEIGHT = 48, 44

def compile_plan(path, tile_ids, width=WIDTH, height=HEIGHT):
    lines = path.read_text(encoding="utf-8").splitlines()
    rows = lines[4:]
    if any(len(line) != width or not set(line) <= set(tile_ids) for line in rows):
        raise ValueError(f"{path}: invalid terrain symbol or row width")
    if len(rows) != height:
        raise ValueError(f"{path}: expected {height} rows of {width} symbols; got {len(rows)}")
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
    parser.add_argument("--preview-unregistered", action="store_true",
                        help="encode unregistered 48x44 concepts under build/eryon-previews")
    args = parser.parse_args()
    tiles = dict(zip("#.,:", (args.wall, args.path, args.meadow, args.stone)))
    for key, value in tiles.items():
        if not 0 <= value <= 0xFFFF:
            parser.error(f"{key} metatile word must be 0..65535")
    # GBA map entries: bits 0..9 metatile, 10..11 collision, 12..15 elevation.
    # Prevent a provisional palette from accidentally turning walls into floors.
    if not (tiles["#"] & 0x0C00):
        parser.error("--wall must have a nonzero collision field (bits 10-11)")
    for symbol in ".,:":
        if tiles[symbol] & 0x0C00:
            parser.error(f"walkable {symbol!r} must have zero collision bits")
    elevations = {value & 0xF000 for value in tiles.values()}
    if elevations != {0x3000}:
        parser.error("all terrain words must use elevation 3 to match Eryon NPCs")
    generated = {}
    for key, folder in SPECS.items():
        src = ROOT / "docs/eryon" / f"{key}_terrain_plan.txt"
        dest = ROOT / "data/layouts" / f"Eryon_{folder}" / "map.bin"
        payload = compile_plan(src, tiles)
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(payload)
        generated[f"LAYOUT_ERYON_{key.upper()}"] = dest.relative_to(ROOT).as_posix()
        print(f"{dest.relative_to(ROOT)}: {len(payload)} bytes")
    if args.preview_unregistered:
        for key, folder in PREVIEW_SPECS.items():
            src = ROOT / "docs/eryon" / f"{key}_terrain_plan.txt"
            dest = ROOT / "build/eryon-previews" / folder / "map.bin"
            payload = compile_plan(src, tiles)
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(payload)
            print(f"PREVIEW ONLY {dest.relative_to(ROOT)}: {len(payload)} bytes")
    if args.preview_unregistered:
        src = ROOT / "docs/eryon/liga_eryon_terrain_plan.txt"
        dest = ROOT / "build/eryon-previews/LigaEryon/map.bin"
        # Reserved facility letters are placeholder floor until proper
        # tilesets, buildings, NPCs and entrance warps are implemented.
        league_tiles = {**tiles, "P": tiles["."], "C": tiles["."],
                        "M": tiles["."], "L": tiles["."], "H": tiles["."]}
        payload = compile_plan(src, league_tiles, width=64, height=56)
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(payload)
        print(f"PREVIEW ONLY {dest.relative_to(ROOT)}: {len(payload)} bytes")
    if args.preview_unregistered:
        # Village/city landmark symbols are only floor placeholders.
        # These previews are not functional buildings or gym interiors.
        from eryon_villages import VILLAGES
        from eryon_gym_cities import CITIES
        village_tiles = {**tiles, **{mark: tiles["."] for mark in "PC MHI".replace(" ", "")}}
        for key in VILLAGES:
            src = ROOT / "docs/eryon/vilas" / f"{key}_village_plan.txt"
            dest = ROOT / "build/eryon-previews/villages" / key / "map.bin"
            payload = compile_plan(src, village_tiles, width=36, height=30)
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(payload)
            print(f"PREVIEW VILLAGE {key}: {len(payload)} bytes")
        city_tiles = {**tiles, "=": tiles["."],
                      **{mark: tiles["."] for mark in "GCMHP"}}
        for key in CITIES:
            src = ROOT / "docs/eryon/cidades" / f"{key}_city_plan.txt"
            dest = ROOT / "build/eryon-previews/cities" / key / "map.bin"
            payload = compile_plan(src, city_tiles, width=64, height=56)
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(payload)
            print(f"PREVIEW CITY {key}: {len(payload)} bytes")
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
