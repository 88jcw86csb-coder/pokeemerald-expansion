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
    "rota_04": "Rota04",
    "colinas_da_neblina": "ColinasDaNeblina",
    "trilha_glacial": "TrilhaGlacial",
    "rota_das_cachoeiras": "RotaDasCachoeiras",
    "trilha_do_oasis": "TrilhaDoOasis",
    "deserto_de_solaris": "DesertoDeSolaris",
    "floresta_dos_ecos": "FlorestaDosEcos",
    "gruta_das_estrelas": "GrutaDasEstrelas",
    "trilha_dos_dragoes": "TrilhaDosDragoes",
    "trilha_lunar": "TrilhaLunar",
}
# Every currently registered 48x44 route belongs in SPECS. Do not create
# previews for maps which are already referenced by data/layouts/layouts.json.
PREVIEW_SPECS = {}
WIDTH, HEIGHT = 48, 44

def compile_plan(path, tile_ids, width=WIDTH, height=HEIGHT):
    lines = path.read_text(encoding="utf-8").splitlines()
    rows = lines[4:]
    if any(len(line) != width or not set(line) <= set(tile_ids) for line in rows):
        raise ValueError(f"{path}: invalid terrain symbol or row width")
    if len(rows) != height:
        raise ValueError(f"{path}: expected {height} rows of {width} symbols; got {len(rows)}")
    # Convert legacy provisional metatile words to verified art *while*
    # preserving the authoritative plan's collision/elevation topology.
    from eryon_terrain_visual_repair import retile_word, stamp_visible_houses
    values = [retile_word(tile_ids[symbol]) for row in rows for symbol in row]
    stamp_visible_houses(values, width, height, rows)
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
    # First village is now engine-registered, not just a preview.
    from eryon_villages import VILLAGES
    village_tiles = {**tiles, **{mark: tiles["."] for mark in "PCMHI"}}
    village_src = ROOT / "docs/eryon/vilas/vila_dos_pomares_village_plan.txt"
    village_dest = ROOT / "data/layouts/Eryon_VilaDosPomares/map.bin"
    village_payload = compile_plan(village_src, village_tiles, width=36, height=30)
    village_dest.parent.mkdir(parents=True, exist_ok=True)
    village_dest.write_bytes(village_payload)
    generated["LAYOUT_ERYON_VILA_DOS_POMARES"] = village_dest.relative_to(ROOT).as_posix()
    print(f"{village_dest.relative_to(ROOT)}: {len(village_payload)} bytes")
    neblina_src = ROOT / "docs/eryon/vilas/vila_da_neblina_village_plan.txt"
    neblina_dest = ROOT / "data/layouts/Eryon_VilaDaNeblina/map.bin"
    neblina_payload = compile_plan(neblina_src, village_tiles, width=36, height=30)
    neblina_dest.parent.mkdir(parents=True, exist_ok=True)
    neblina_dest.write_bytes(neblina_payload)
    generated["LAYOUT_ERYON_VILA_DA_NEBLINA"] = neblina_dest.relative_to(ROOT).as_posix()
    print(f"{neblina_dest.relative_to(ROOT)}: {len(neblina_payload)} bytes")
    refuge_src = ROOT / "docs/eryon/vilas/refugio_cristal_village_plan.txt"
    refuge_dest = ROOT / "data/layouts/Eryon_RefugioCristal/map.bin"
    refuge_payload = compile_plan(refuge_src, village_tiles, width=36, height=30)
    refuge_dest.parent.mkdir(parents=True, exist_ok=True)
    refuge_dest.write_bytes(refuge_payload)
    generated["LAYOUT_ERYON_REFUGIO_CRISTAL"] = refuge_dest.relative_to(ROOT).as_posix()
    print(f"{refuge_dest.relative_to(ROOT)}: {len(refuge_payload)} bytes")
    outpost_src = ROOT / "docs/eryon/vilas/posto_oriental_village_plan.txt"
    outpost_dest = ROOT / "data/layouts/Eryon_PostoOriental/map.bin"
    outpost_payload = compile_plan(outpost_src, village_tiles, width=36, height=30)
    outpost_dest.parent.mkdir(parents=True, exist_ok=True)
    outpost_dest.write_bytes(outpost_payload)
    generated["LAYOUT_ERYON_POSTO_ORIENTAL"] = outpost_dest.relative_to(ROOT).as_posix()
    print(f"{outpost_dest.relative_to(ROOT)}: {len(outpost_payload)} bytes")
    waters_src = ROOT / "docs/eryon/vilas/vila_das_aguas_village_plan.txt"
    waters_dest = ROOT / "data/layouts/Eryon_VilaDasAguas/map.bin"
    waters_payload = compile_plan(waters_src, village_tiles, width=36, height=30)
    waters_dest.parent.mkdir(parents=True, exist_ok=True)
    waters_dest.write_bytes(waters_payload)
    generated["LAYOUT_ERYON_VILA_DAS_AGUAS"] = waters_dest.relative_to(ROOT).as_posix()
    print(f"{waters_dest.relative_to(ROOT)}: {len(waters_payload)} bytes")
    # The mountain settlement is now a registered rest village.
    peak_src = ROOT / "docs/eryon/vilas/vila_do_pico_village_plan.txt"
    peak_dest = ROOT / "data/layouts/Eryon_VilaDoPico/map.bin"
    peak_payload = compile_plan(peak_src, village_tiles, width=36, height=30)
    peak_dest.parent.mkdir(parents=True, exist_ok=True)
    peak_dest.write_bytes(peak_payload)
    generated["LAYOUT_ERYON_VILA_DO_PICO"] = peak_dest.relative_to(ROOT).as_posix()
    print(f"{peak_dest.relative_to(ROOT)}: {len(peak_payload)} bytes")
    # Echo Village is registered; compile its current authoritative village plan.
    aldeia_src = ROOT / "docs/eryon/vilas/aldeia_dos_ecos_village_plan.txt"
    aldeia_dest = ROOT / "data/layouts/Eryon_AldeiaDosEcos/map.bin"
    aldeia_payload = compile_plan(aldeia_src, village_tiles, width=36, height=30)
    aldeia_dest.parent.mkdir(parents=True, exist_ok=True)
    aldeia_dest.write_bytes(aldeia_payload)
    generated["LAYOUT_ERYON_ALDEIA_DOS_ECOS"] = aldeia_dest.relative_to(ROOT).as_posix()
    print(f"{aldeia_dest.relative_to(ROOT)}: {len(aldeia_payload)} bytes")
    # Neonara is the first registered gym city after Verdelume.
    neonara_tiles = {**tiles, "=": tiles["."],
                     **{mark: tiles["."] for mark in "GCMHP"}}
    neonara_src = ROOT / "docs/eryon/cidades/neonara_city_plan.txt"
    neonara_dest = ROOT / "data/layouts/Eryon_Neonara/map.bin"
    neonara_payload = compile_plan(neonara_src, neonara_tiles, width=64, height=56)
    neonara_dest.parent.mkdir(parents=True, exist_ok=True)
    neonara_dest.write_bytes(neonara_payload)
    generated["LAYOUT_ERYON_NEONARA"] = neonara_dest.relative_to(ROOT).as_posix()
    print(f"{neonara_dest.relative_to(ROOT)}: {len(neonara_payload)} bytes")
    frostheim_src = ROOT / "docs/eryon/cidades/frostheim_city_plan.txt"
    frostheim_dest = ROOT / "data/layouts/Eryon_Frostheim/map.bin"
    frostheim_payload = compile_plan(frostheim_src, neonara_tiles, width=64, height=56)
    frostheim_dest.parent.mkdir(parents=True, exist_ok=True)
    frostheim_dest.write_bytes(frostheim_payload)
    generated["LAYOUT_ERYON_FROSTHEIM"] = frostheim_dest.relative_to(ROOT).as_posix()
    print(f"{frostheim_dest.relative_to(ROOT)}: {len(frostheim_payload)} bytes")
    umbra_src = ROOT / "docs/eryon/cidades/umbra_city_plan.txt"
    umbra_dest = ROOT / "data/layouts/Eryon_Umbra/map.bin"
    umbra_payload = compile_plan(umbra_src, neonara_tiles, width=64, height=56)
    umbra_dest.parent.mkdir(parents=True, exist_ok=True)
    umbra_dest.write_bytes(umbra_payload)
    generated["LAYOUT_ERYON_UMBRA"] = umbra_dest.relative_to(ROOT).as_posix()
    print(f"{umbra_dest.relative_to(ROOT)}: {len(umbra_payload)} bytes")
    ignivar_src = ROOT / "docs/eryon/cidades/ignivar_city_plan.txt"
    ignivar_dest = ROOT / "data/layouts/Eryon_Ignivar/map.bin"
    ignivar_payload = compile_plan(ignivar_src, neonara_tiles, width=64, height=56)
    ignivar_dest.parent.mkdir(parents=True, exist_ok=True)
    ignivar_dest.write_bytes(ignivar_payload)
    generated["LAYOUT_ERYON_IGNIVAR"] = ignivar_dest.relative_to(ROOT).as_posix()
    print(f"{ignivar_dest.relative_to(ROOT)}: {len(ignivar_payload)} bytes")
    # Fourth gym city: Arkhara is now a registered route waypoint.
    arkhara_src = ROOT / "docs/eryon/cidades/arkhara_city_plan.txt"
    arkhara_dest = ROOT / "data/layouts/Eryon_Arkhara/map.bin"
    arkhara_payload = compile_plan(arkhara_src, neonara_tiles, width=64, height=56)
    arkhara_dest.parent.mkdir(parents=True, exist_ok=True)
    arkhara_dest.write_bytes(arkhara_payload)
    generated["LAYOUT_ERYON_ARKHARA"] = arkhara_dest.relative_to(ROOT).as_posix()
    print(f"{arkhara_dest.relative_to(ROOT)}: {len(arkhara_payload)} bytes")
    # Eighth gym city now has a registered overworld and reciprocal warp.
    dragon_src = ROOT / "docs/eryon/cidades/drakonia_city_plan.txt"
    dragon_dest = ROOT / "data/layouts/Eryon_Drakonia/map.bin"
    dragon_payload = compile_plan(dragon_src, neonara_tiles, width=64, height=56)
    dragon_dest.parent.mkdir(parents=True, exist_ok=True)
    dragon_dest.write_bytes(dragon_payload)
    generated["LAYOUT_ERYON_DRAKONIA"] = dragon_dest.relative_to(ROOT).as_posix()
    print(f"{dragon_dest.relative_to(ROOT)}: {len(dragon_payload)} bytes")
    # Registered League approach: facility letters are walkable floor markers.
    league_road_tiles = {**tiles, **{mark: tiles["."] for mark in "PCMLH"}}
    league_road_src = ROOT / "docs/eryon/caminho_da_liga_terrain_plan.txt"
    league_road_dest = ROOT / "data/layouts/Eryon_CaminhoDaLiga/map.bin"
    league_road_payload = compile_plan(league_road_src, league_road_tiles)
    league_road_dest.parent.mkdir(parents=True, exist_ok=True)
    league_road_dest.write_bytes(league_road_payload)
    generated["LAYOUT_ERYON_CAMINHO_DA_LIGA"] = league_road_dest.relative_to(ROOT).as_posix()
    print(f"{league_road_dest.relative_to(ROOT)}: {len(league_road_payload)} bytes")
    # The League is now a real 96x72 city, not an unregistered preview.
    league_src = ROOT / "docs/eryon/liga_eryon_terrain_plan.txt"
    league_dest = ROOT / "data/layouts/Eryon_CidadeDaLiga/map.bin"
    league_tiles = {"#": tiles["#"], ".": tiles["."],
                    ",": tiles[","], "L": tiles["."]}
    league_payload = compile_plan(league_src, league_tiles, width=96, height=72)
    league_dest.parent.mkdir(parents=True, exist_ok=True)
    league_dest.write_bytes(league_payload)
    generated["LAYOUT_ERYON_CIDADE_DA_LIGA"] = league_dest.relative_to(ROOT).as_posix()
    print(f"{league_dest.relative_to(ROOT)}: {len(league_payload)} bytes")
    if args.preview_unregistered:
        # Village/city landmark symbols are only floor placeholders.
        # These previews are not functional buildings or gym interiors.
        from eryon_villages import VILLAGES
        from eryon_gym_cities import CITIES
        village_tiles = {**tiles, **{mark: tiles["."] for mark in "PC MHI".replace(" ", "")}}
        for key in VILLAGES:
            if key in ("vila_dos_pomares", "vila_da_neblina", "refugio_cristal", "posto_oriental", "vila_das_aguas", "vila_do_pico", "aldeia_dos_ecos"):
                continue
            src = ROOT / "docs/eryon/vilas" / f"{key}_village_plan.txt"
            dest = ROOT / "build/eryon-previews/villages" / key / "map.bin"
            payload = compile_plan(src, village_tiles, width=36, height=30)
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(payload)
            print(f"PREVIEW VILLAGE {key}: {len(payload)} bytes")
        city_tiles = {**tiles, "=": tiles["."],
                      **{mark: tiles["."] for mark in "GCMHP"}}
        for key in CITIES:
            if key in ("neonara", "frostheim", "umbra", "ignivar", "drakonia"):
                continue
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
