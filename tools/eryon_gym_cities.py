#!/usr/bin/env python3
"""Generate eight distinct LARGE gym-city concept maps for Pokemon Eryon.

These are 64x56 ASCII planning layouts, NOT registered engine maps.
City plans reserve G (gym), C (Pokemon Center), M (mart), H (houses),
P (plaza), = (streets), # (blocks), and park vegetation (comma).
"""
from collections import deque
from pathlib import Path

W, H = 64, 56
ROOT = Path(__file__).resolve().parents[1]
CITIES = {
    "verdelume": ("Verdelume", "Grass", 1),
    "neonara": ("Neonara", "Electric", 2),
    "frostheim": ("Frostheim", "Ice", 3),
    "arkhara": ("Arkhara", "Rock", 4),
    "umbra": ("Umbra", "Dark/Poison", 5),
    "ignivar": ("Ignivar", "Fire", 6),
    "lunaris": ("Lunaris", "Psychic/Fairy", 7),
    "drakonia": ("Drakonia", "Dragon", 8),
}
BUILDINGS = {
    "G": (32, 11), "C": (14, 20), "M": (48, 20),
    "H": (13, 39), "P": (32, 28),
}


def city(name):
    if name not in CITIES:
        raise ValueError(name)
    idx = CITIES[name][2]
    t = [["#" for _ in range(W)] for _ in range(H)]
    # A walkable street grid: four neighborhoods, large civic center,
    # outer avenues, a central spine, and north/south/east/west exits.
    for y in (12, 28, 43):
        for x in range(W):
            for dy in (-1, 0, 1):
                t[y+dy][x] = "="
    for x in (14, 32, 49):
        for y in range(H):
            for dx in (-1, 0, 1):
                t[y][x+dx] = "="
    for y in range(23, 34):
        for x in range(26, 39):
            t[y][x] = "P"
    # Park zones change from city to city, without obstructing avenues.
    for cy, cx in ((5, 6 + idx), (49, 56 - idx), (35, 23)):
        for y in range(max(1, cy-3), min(H-1, cy+4)):
            for x in range(max(1, cx-3), min(W-1, cx+4)):
                if (x-cx)**2+(y-cy)**2 <= 9 and t[y][x] == "#":
                    t[y][x] = ","
    # Buildings have accessible entrances on the adjacent avenue.
    for symbol, (x, y) in BUILDINGS.items():
        t[y][x] = symbol
    # Distinct district landmarks: docks, tower, canyon, gardens etc.
    lx = 40 + (idx % 3) * 3
    ly = 35 + (idx % 4)
    for y in range(ly-2, ly+3):
        for x in range(lx-2, lx+3):
            if t[y][x] == "#":
                t[y][x] = ","
    for y in range(min(ly, 43), max(ly, 43)+1):
        t[y][49] = "="
    # Explicit street exits; avoid implying routes are wired yet.
    t[28][0] = t[28][W-1] = "="
    t[0][32] = t[H-1][32] = "="
    return t


def accessible(t, start=(0, 28)):
    passable = set("=,GCMHP")
    q = deque([start])
    seen = {start}
    while q:
        x,y = q.popleft()
        for nx,ny in ((x+1,y),(x-1,y),(x,y+1),(x,y-1)):
            if 0 <= nx < W and 0 <= ny < H and t[ny][nx] in passable and (nx,ny) not in seen:
                seen.add((nx,ny))
                q.append((nx,ny))
    return seen


def render(name, t):
    city_name, typ, badge = CITIES[name]
    return (f"{city_name} | Gym {badge} ({typ}) | Eryon concept 64x56\n"
            "# block; = avenue; , park; G gym; C Pokemon Center; M mart; H housing; P civic plaza\n"
            "Design only: not a registered map.bin. Gym, interiors, scripts and warps not implemented.\n\n"
            + "\n".join("".join(row) for row in t) + "\n")


def main():
    out = ROOT / "docs/eryon/cidades"
    out.mkdir(parents=True, exist_ok=True)
    for name in CITIES:
        t = city(name)
        reached = accessible(t)
        required = {(0,28), (W-1,28), (32,0), (32,H-1)}
        required.update(BUILDINGS.values())
        assert required <= reached, f"{name}: inaccessible city facility/exit"
        (out / f"{name}_city_plan.txt").write_text(render(name,t),encoding="utf-8")
        print(name, len(reached), "connected tiles")


if __name__ == "__main__":
    main()
