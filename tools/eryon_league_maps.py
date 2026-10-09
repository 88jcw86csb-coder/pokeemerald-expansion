#!/usr/bin/env python3
"""Generate the final Eryon League approach and summit hub (design only)."""
from collections import deque
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]


def route():
    w,h=48,44
    t=[["#" for _ in range(w)] for _ in range(h)]
    for x in range(w):
        y=22+(x//8)%3-1
        for yy in range(y-2,y+3):
            t[yy][x]=":"
    # Three optional mountain detours and lookout platforms.
    for cx,cy in ((10,8),(25,36),(38,8)):
        for y in range(min(cy,22),max(cy,22)+1):
            t[y][cx]=":"
        for y in range(max(1,cy-4),min(h-1,cy+5)):
            for x in range(max(1,cx-4),min(w-1,cx+5)):
                if (x-cx)**2+(y-cy)**2<=16:
                    t[y][x]="."
    for x in range(w):
        t[22][x]=":"
    return t


def league():
    w,h=64,56
    t=[["#" for _ in range(w)] for _ in range(h)]
    for y in range(h):
        for x in range(30,35):
            t[y][x]="."
    for y in (14,28,42):
        for yy in range(y-2,y+3):
            for x in range(6,58):
                t[yy][x]="."
    for cx,cy in ((12,14),(52,14),(12,42),(52,42)):
        for y in range(cy-5,cy+6):
            for x in range(cx-5,cx+6):
                if (x-cx)**2+(y-cy)**2<=25:
                    t[y][x]="P"
    # Facilities are reserved slots, not functional buildings.
    for symbol,x,y in (("C",12,14),("M",52,14),("L",32,28),("H",12,42),("H",52,42)):
        t[y][x]=symbol
    return t


def connected(t,start):
    w,h=len(t[0]),len(t)
    q=deque([start]);seen={start}
    while q:
        x,y=q.popleft()
        for nx,ny in ((x+1,y),(x-1,y),(x,y+1),(x,y-1)):
            if 0<=nx<w and 0<=ny<h and t[ny][nx]!="#" and (nx,ny) not in seen:
                seen.add((nx,ny));q.append((nx,ny))
    return seen


def render(name,t):
    return (f"{name} | Eryon final approach design {len(t[0])}x{len(t)}\n"
            "# blocked; . floor; : mountain path; P plaza; C center; M mart; L league; H hall\n"
            "Concept only: no map registration, tileset, interior, warp or league battles.\n\n"
            +"\n".join("".join(row) for row in t)+"\n")


def main():
    for name,fn,start,exit in (
        ("caminho_da_liga",route,(0,22),(47,22)),
        ("liga_eryon",league,(32,55),(32,0)),
    ):
        t=fn();seen=connected(t,start)
        walk={(x,y) for y,row in enumerate(t) for x,v in enumerate(row) if v!="#"}
        assert seen==walk and exit in seen, f"{name}: disconnected"
        p=ROOT/"docs/eryon"/f"{name}_terrain_plan.txt"
        p.write_text(render(name,t),encoding="utf-8")
        print(name,len(seen))


if __name__=="__main__":
    main()
