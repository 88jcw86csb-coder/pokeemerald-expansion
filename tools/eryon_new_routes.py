#!/usr/bin/env python3
"""Design three NEW Eryon routes (not yet registered as playable maps).

Run: python3 tools/eryon_new_routes.py
Symbols: # blocked, . trail, , grass, : rocky floor.
"""
from collections import deque
from pathlib import Path

W, H = 48, 44
ROOT = Path(__file__).resolve().parents[1]
ROUTES = {
    "rota_das_cachoeiras": "waterfalls",
    "deserto_de_solaris": "desert",
    "floresta_dos_ecos": "echoes",
}


def carve(tiles, x0, y0, x1, y1, symbol="."):
    """Draw an orthogonal connected corridor."""
    for x in range(min(x0, x1), max(x0, x1) + 1):
        tiles[y0][x] = symbol
    for y in range(min(y0, y1), max(y0, y1) + 1):
        tiles[y][x1] = symbol


def build(kind):
    if kind not in ROUTES.values():
        raise ValueError(f"unknown route: {kind}")
    t = [["#" for _ in range(W)] for _ in range(H)]
    if kind == "waterfalls":
        # A vertical river gorge with a long switchback and two scenic ledges.
        carve(t, 23, 43, 23, 3)
        carve(t, 23, 35, 8, 35, ":")
        carve(t, 8, 35, 8, 21, ":")
        carve(t, 8, 21, 23, 21, ":")
        carve(t, 23, 30, 40, 30, ",")
        carve(t, 40, 30, 40, 12, ",")
        carve(t, 40, 12, 23, 12, ",")
        for cy, cx in ((35, 8), (21, 8), (30, 40), (12, 40)):
            for y in range(max(1, cy-3), min(H-1, cy+4)):
                for x in range(max(1, cx-3), min(W-1, cx+4)):
                    if (x-cx)**2+(y-cy)**2 <= 9:
                        t[y][x] = ","
        t[43][23] = "."
        t[0][23] = "."  # northward exit
        carve(t, 23, 3, 23, 0)
    elif kind == "desert":
        carve(t, 0, 22, 47, 22)
        carve(t, 9, 22, 9, 8, ":")
        carve(t, 9, 8, 30, 8, ":")
        carve(t, 30, 8, 30, 22, ":")
        carve(t, 16, 22, 16, 36, ",")
        carve(t, 16, 36, 40, 36, ",")
        carve(t, 40, 36, 40, 22, ",")
        for cx, cy in ((9, 8), (30, 8), (16, 36), (40, 36)):
            for y in range(max(1, cy-4), min(H-1, cy+5)):
                for x in range(max(1, cx-4), min(W-1, cx+5)):
                    if (x-cx)**2+(y-cy)**2 <= 16:
                        t[y][x] = ":"
        t[22][0] = t[22][47] = "."
    else:
        carve(t, 0, 22, 47, 22)
        carve(t, 12, 22, 12, 7, ",")
        carve(t, 12, 7, 36, 7, ",")
        carve(t, 36, 7, 36, 22, ",")
        carve(t, 19, 22, 19, 38, ",")
        carve(t, 19, 38, 42, 38, ",")
        carve(t, 42, 38, 42, 22, ",")
        for cx, cy in ((12, 7), (36, 7), (19, 38), (42, 38)):
            for y in range(max(1, cy-4), min(H-1, cy+5)):
                for x in range(max(1, cx-4), min(W-1, cx+5)):
                    if (x-cx)**2+(y-cy)**2 <= 14:
                        t[y][x] = ","
        t[22][0] = t[22][47] = "."
    return t


def connected(tiles, start):
    if tiles[start[1]][start[0]] == "#":
        return set()
    found, queue = {start}, deque([start])
    while queue:
        x, y = queue.popleft()
        for nx, ny in ((x+1,y),(x-1,y),(x,y+1),(x,y-1)):
            if 0 <= nx < W and 0 <= ny < H and tiles[ny][nx] != "#" and (nx,ny) not in found:
                found.add((nx,ny))
                queue.append((nx,ny))
    return found


def render(name, tiles):
    return (f"{name} — terrain concept (48x44)\n"
            "# = barrier; . = main trail; , = meadow; : = stone\n"
            "Design only: not a registered GBA map; requires tilesets, events, warps and ROM tests.\n\n"
            + "\n".join("".join(row) for row in tiles) + "\n")


def main():
    out = ROOT / "docs/eryon"
    out.mkdir(parents=True, exist_ok=True)
    for name, kind in ROUTES.items():
        tiles = build(kind)
        start = (23,43) if kind == "waterfalls" else (0,22)
        goal = (23,0) if kind == "waterfalls" else (47,22)
        accessible = connected(tiles, start)
        assert goal in accessible, f"{name}: disconnected exits"
        assert all((x,y) in accessible for y,row in enumerate(tiles)
                   for x,cell in enumerate(row) if cell != "#"), f"{name}: isolated floor"
        (out / f"{name}_terrain_plan.txt").write_text(render(name, tiles), encoding="utf-8")
        print(f"{name}: {len(accessible)} connected tiles")


if __name__ == "__main__":
    main()
