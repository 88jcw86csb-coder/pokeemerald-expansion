#!/usr/bin/env python3
"""Generate distinct Eryon route terrain plans for map artists.

Produces ASCII tile plans and verifies that a connected walking corridor
joins the west and east borders. This is NOT a GBA map.bin generator:
collision/metatile properties must be authored and tested in Porymap.
"""
from collections import deque
from pathlib import Path

WIDTH, HEIGHT = 48, 44
OUTPUT = Path(__file__).resolve().parents[1] / "docs" / "eryon"

def route(kind):
    tiles = [["#" for _ in range(WIDTH)] for _ in range(HEIGHT)]
    for x in range(WIDTH):
        center = 22 + (2 if (x // 8) % 2 else 0)
        for y in range(center - 3, center + 4):
            tiles[y][x] = "."
    # Keep investigation markers connected to the primary trail.
    for x in ([23] if kind == "valley" else [8]):
        for y in range(18, 25):
            tiles[y][x] = "."
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
    else:
        # Distinctive stony pull-off around the roadside healer.
        for y in range(23, 31):
            for x in range(28, 39):
                tiles[y][x] = ":"
    # The road/valley transitions must align with the fixed warp coordinates.
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
    for name, kind in (("passagem_rochosa", "passage"), ("estrada_oriental", "road"), ("vale_dos_ventos", "valley")):
        tiles = route(kind)
        accessible = reachable(tiles)
        assert (47, 22) in accessible, f"{name}: east exit is unreachable"
        landmarks = (
            [(0, 22), (47, 22), (8, 18), (16, 21), (33, 26)] if kind == "road"
            else [(0, 22), (47, 22), (14, 21), (32, 25), (39, 16), (23, 18), (37, 10)] if kind == "valley"
            else [(0, 22), (47, 22), (11, 22), (30, 24), (19, 32), (37, 14), (34, 34), (24, 18), (25, 18), (41, 18), (15, 18)]
        )
        for x, y in landmarks:
            assert (x, y) in accessible, f"{name}: landmark ({x},{y}) unreachable"
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
