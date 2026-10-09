#!/usr/bin/env python3
"""Four additional 48x44 routes to bridge Eryon's approved gym cities.

ASCII concepts only; engine map.json, warps and encounters are NOT installed.
"""
from collections import deque
from pathlib import Path

W,H=48,44
ROOT=Path(__file__).resolve().parents[1]
ROUTES={
    "estrada_dos_pomares": "orchard",
    "colinas_da_neblina": "mist",
    "trilha_glacial": "ice",
    "trilha_dos_dragoes": "dragon",
    "trilha_lunar": "lunar",
}


def route(kind):
    if kind not in ROUTES.values():
        raise ValueError(kind)
    t=[["#" for _ in range(W)] for _ in range(H)]
    for x in range(W):
        y=22 + ((x//9)%3)-1
        for yy in range(y-2,y+3):
            t[yy][x]="."
    if kind=="orchard":
        branches=[(9,10,":"),(27,33,",")]
    elif kind=="mist":
        branches=[(11,34,","),(34,9,":")]
    elif kind=="ice":
        branches=[(8,8,":"),(37,35,":")]
    elif kind=="lunar":
        branches=[(9,35,","),(38,9,":")]
    else:
        branches=[(13,9,":"),(37,34,":")]
    for cx,cy,ground in branches:
        for x in range(min(cx,24),max(cx,24)+1):
            t[22][x]="."
        for y in range(min(cy,22),max(cy,22)+1):
            t[y][cx]=":"
        for y in range(max(1,cy-5),min(H-1,cy+6)):
            for x in range(max(1,cx-5),min(W-1,cx+6)):
                if (x-cx)**2+(y-cy)**2<=25:
                    t[y][x]=ground
    # Restore a continuous east-west corridor after optional side areas.
    for x in range(W):
        t[22][x]="."
    return t


def reachable(t,start=(0,22)):
    q=deque([start]);seen={start}
    while q:
        x,y=q.popleft()
        for nx,ny in ((x+1,y),(x-1,y),(x,y+1),(x,y-1)):
            if 0<=nx<W and 0<=ny<H and t[ny][nx]!="#" and (nx,ny) not in seen:
                seen.add((nx,ny));q.append((nx,ny))
    return seen


def render(name,t):
    return (f"{name} — Eryon terrain concept 48x44\n"
            "# blocked; . path; , vegetation; : rocky/special ground\n"
            "Design only: metatiles, collisions, wild encounters and warps not installed.\n\n"
            +"\n".join("".join(row) for row in t)+"\n")


def main():
    out=ROOT/"docs/eryon"
    out.mkdir(parents=True,exist_ok=True)
    for name,kind in ROUTES.items():
        t=route(kind);seen=reachable(t)
        walkable={(x,y) for y,row in enumerate(t) for x,c in enumerate(row) if c!="#"}
        assert (47,22) in seen and walkable==seen, f"{name}: disconnected"
        (out/f"{name}_terrain_plan.txt").write_text(render(name,t),encoding="utf-8")
        print(name,len(seen))


if __name__=="__main__":
    main()
