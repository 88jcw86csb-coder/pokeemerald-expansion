#!/usr/bin/env python3
"""Walkable Star Cavern map, connected to Drakonia and League Road."""
from collections import deque
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
W,H=48,44

def cavern():
    t=[["#" for _ in range(W)] for _ in range(H)]
    # A guaranteed navigable central passage and two side chambers.
    for x in range(W):
        for y in range(20,25):
            t[y][x]="."
    for cx,cy in ((12,10),(35,34)):
        for y in range(min(22,cy),max(22,cy)+1):
            for x in range(cx-1,cx+2):
                t[y][x]=":"
        for y in range(max(1,cy-7),min(H-1,cy+8)):
            for x in range(max(1,cx-8),min(W-1,cx+9)):
                if ((x-cx)/8)**2+((y-cy)/7)**2<=1:
                    t[y][x]=":"
    for x in range(W):
        t[22][x]="."
    # Preserve already-compiled walkable pads, scout clearance and southern
    # relay approach that previously existed only in map.bin (123 tiles).
    for y, spans in (
        (19, ((17, 21),)),
        (20, ((17, 21),)),
        (21, ((0, 10), (14, 15), (17, 21), (23, 31), (39, 47))),
        (22, ((0, 47),)),
        (23, ((11, 22), (32, 33), (37, 38), (40, 41))),
        (24, ((40, 41),)),
        (25, ((40, 41),)),
        (26, ((40, 41),)),
        (27, ((40, 41),)),
        (28, ((40, 41),)),
        (29, ((41, 41),)),
    ):
        for x0, x1 in spans:
            for x in range(x0, x1 + 1):
                t[y][x] = ":"
    # New upper winding loop: avoids the central tunnel, rejoins by the
    # eastern passage, and leads to an optional stellar chamber.
    for y, x0, x1 in (
        (12, 18, 24), (15, 24, 29), (11, 29, 35),
        (16, 35, 40), (9, 27, 31), (13, 27, 31),
    ):
        for x in range(x0, x1 + 1):
            t[y][x] = ":"
    for x, y0, y1 in (
        (24, 12, 15), (29, 9, 15), (35, 11, 16),
        (40, 16, 20), (39, 18, 20),
    ):
        for y in range(y0, y1 + 1):
            t[y][x] = ":"
    for y in range(7, 14):
        for x in range(26, 33):
            if (x - 29) ** 2 / 16 + (y - 10) ** 2 / 9 <= 1.03:
                t[y][x] = ":"
    # Keep the already-registered Eclipse relay terminal at (42, 29) reachable.
    # Its previous block collision was nonzero; do not move the saved event.
    t[29][42] = ":"
    return t

def reachable(t):
    q=deque([(0,22)]);seen={(0,22)}
    while q:
        x,y=q.popleft()
        for nx,ny in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
            if 0<=nx<W and 0<=ny<H and t[ny][nx]!="#" and (nx,ny) not in seen:
                seen.add((nx,ny));q.append((nx,ny))
    return seen

def render(t):
    return ("gruta_das_estrelas — Eryon terrain concept 48x44\n"
            "# blocked; . path; : cave chamber\n"
            "Mapa registrado: galeria superior em curva, camara estelar opcional, tunel livre de HMs e Eclipse investigavel.\n\n"
            +"\n".join("".join(row) for row in t)+"\n")

def main():
    t=cavern()
    floor={(x,y) for y,row in enumerate(t) for x,v in enumerate(row) if v!="#"}
    assert floor==reachable(t) and (47,22) in floor
    dest=ROOT/"docs/eryon/gruta_das_estrelas_terrain_plan.txt"
    dest.write_text(render(t),encoding="utf-8")
    print("Star Cavern:",len(floor),"connected cells")

if __name__=="__main__":
    main()
