#!/usr/bin/env python3
"""Generate distinct Eryon route terrain plans for map artists.

Produces ASCII tile plans and verifies that a connected walking corridor
joins the west and east borders. This is NOT a GBA map.bin generator:
collision/metatile properties must be authored and tested in Porymap.
"""
from collections import deque
import json
from pathlib import Path

WIDTH, HEIGHT = 48, 44
ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs" / "eryon"
MAP_NAMES = {
    "bosque_de_lumina": "Eryon_BosqueDeLumina",
    "serra_dos_cristais": "Eryon_SerraDosCristais",
    "passagem_rochosa": "Eryon_PassagemRochosa",
    "estrada_oriental": "Eryon_EstradaOriental",
    "vale_dos_ventos": "Eryon_ValeDosVentos",
}

def route(kind):
    tiles = [["#" for _ in range(WIDTH)] for _ in range(HEIGHT)]
    for x in range(WIDTH) if kind != "forest" else ():
        center = 22 + (2 if (x // 8) % 2 else 0)
        for y in range(center - 3, center + 4):
            tiles[y][x] = "."
    # Keep investigation markers connected to the primary trail.
    if kind in ("valley", "road"):
        for y in range(18, 25):
            tiles[y][23 if kind == "valley" else 8] = "."
    if kind == "forest":
        # A north/south woodland route with an eastern glade and westward loop.
        # Keep a narrow main path rather than the generic east/west road.
        for y in range(5, 39):
            center = 16 + (2 if 12 <= y < 22 else 0)
            for x in range(center - 2, center + 3):
                tiles[y][x] = "."
        # Winding loop through the clearing, linking all existing events.
        for y in range(13, 27):
            for x in range(12, 26):
                if (x - 19) ** 2 / 49 + (y - 20) ** 2 / 49 < 1:
                    tiles[y][x] = ","
        for x in range(15, 24):
            tiles[18][x] = "."
            tiles[25][x] = "."
        for y in range(18, 26):
            tiles[y][23] = "."
        for y in range(14, 39):
            tiles[y][16] = "."
        # Both forest warps are placed on explicit clear path tiles.
        tiles[5][14] = "."
        tiles[38][16] = "."
    if kind == "mountain":
        # Stepped ascent with accessible observation terraces.
        for x in range(WIDTH):
            for y in range(19, 27):
                tiles[y][x] = ":"
        for x in (12, 24, 30, 35, 38, 39):
            for y in range(13, 36):
                tiles[y][x] = ":"
        for y in (14, 16, 20, 24, 29, 31, 35):
            for x in range(12, 40):
                tiles[y][x] = ":"
    if kind == "passage":
        # Mountain switchbacks and a sheltered central crossing.
        for x in range(7, 42):
            for y in range(17, 29):
                if abs(y - (22 + ((x // 7) % 3) - 1)) <= 2:
                    tiles[y][x] = ":"
        for x in range(0, WIDTH):
            tiles[22][x] = "."
        # Branching mountain trails connect the hiker, Eclipse guard and medic.
        for x in (19, 34):
            for y in range(22, 35):
                tiles[y][x] = ":"
        for x in range(19, 35):
            tiles[32][x] = ":"
        for y in range(14, 23):
            tiles[y][37] = ":"
        # Northern survey signs and crystal clues.
        for x in range(15, 42):
            tiles[18][x] = ":"
        for y in range(18, 23):
            tiles[y][15] = ":"
    if kind == "valley":
        # Southern meadow and northern lookout are connected to the main path.
        for y in range(24, 36):
            for x in range(11, 39):
                if (x - 25) ** 2 / 196 + (y - 29) ** 2 / 36 < 1:
                    tiles[y][x] = ","
        for y in range(10, 25):
            for x in range(35, 42):
                tiles[y][x] = "."
        # Join the lookout at (37,10) to the investigation marker at (23,18).
        for x in range(23, 38):
            tiles[18][x] = "."
    elif kind == "road":
        # Distinctive stony pull-off around the roadside healer.
        for y in range(23, 31):
            for x in range(28, 39):
                tiles[y][x] = ":"
    # The road/valley transitions must align with the fixed warp coordinates.
    if kind != "forest":
        for x in (0, WIDTH - 1):
            tiles[22][x] = "."
    return tiles

def reachable(tiles, start=(0, 22)):
    """Return all walkable coordinates connected to a starting point."""
    queue = deque([start])
    seen = {start}
    while queue:
        x, y = queue.popleft()
        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if 0 <= nx < WIDTH and 0 <= ny < HEIGHT and tiles[ny][nx] != "#" and (nx, ny) not in seen:
                seen.add((nx, ny))
                queue.append((nx, ny))
    return seen

def main():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    for name, kind in (
        ("bosque_de_lumina", "forest"),
        ("serra_dos_cristais", "mountain"),
        ("passagem_rochosa", "passage"),
        ("estrada_oriental", "road"),
        ("vale_dos_ventos", "valley"),
    ):
        tiles = route(kind)
        accessible = reachable(tiles, (16, 38) if kind == "forest" else (0, 22))
        assert ((14, 5) if kind == "forest" else (47, 22)) in accessible, f"{name}: exit is unreachable"
        map_path = ROOT / "data" / "maps" / MAP_NAMES[name] / "map.json"
        map_data = json.loads(map_path.read_text(encoding="utf-8"))
        landmarks = [(0, 22), (47, 22)] if kind != "forest" else [(16, 38), (14, 5)]
        for event in map_data.get("warp_events", []):
            landmarks.append((event["x"], event["y"]))
        for event in map_data.get("object_events", []):
            landmarks.append((event["x"], event["y"]))
        for event in map_data.get("bg_events", []):
            landmarks.append((event["x"], event["y"]))
        for x, y in landmarks:
            assert 0 <= x < WIDTH and 0 <= y < HEIGHT, (
                f"{name}: event ({x},{y}) outside terrain")
            assert (x, y) in accessible, (
                f"{name}: event ({x},{y}) unreachable from west entrance")
        path = OUTPUT / f"{name}_terrain_plan.txt"
        path.write_text(
            f"{name} — terrain concept (48x44)\n"
            "# = cliff/forest barrier; . = main trail; , = meadow; : = stony rest area\n"
            "Not compiled map data. Convert into Porymap metatiles and verify collision.\n\n"
            + "\n".join("".join(row) for row in tiles) + "\n",
            encoding="utf-8",
        )
        print(f"OK: {path.relative_to(OUTPUT.parents[1])} — traversable west/east corridor")

if __name__ == "__main__":
    main()
