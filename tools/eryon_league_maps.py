#!/usr/bin/env python3
"""Generate the registered HM-free League approach and planned summit hub."""
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
    # The east gate now links to the City of the League.
    for y in range(h):
        t[y][w - 1]="#"
    t[22][w-1] = ":"
    return t


def league():
    # 96x72 capital city; central square houses the League building.
    w,h = 96,72
    t=[["," if (x*y+17*x+13*y)%19<4 else "#" for x in range(w)]
       for y in range(h)]
    def rect(x0,y0,x1,y1,letter="."):
        for y in range(y0,y1+1):
            for x in range(x0,x1+1):
                t[y][x]=letter
    rect(0,34,95,38)
    rect(45,0,51,71)
    rect(13,0,17,71)
    rect(77,0,81,71)
    rect(0,15,95,19)
    rect(0,53,95,57)
    rect(35,25,61,47)
    rect(25,31,71,41)
    rect(33,12,63,20)
    rect(33,53,63,59)
    for x,y in ((18,25),(73,27),(20,46),(74,48)):
        rect(x-4,y-3,x+4,y+3,",")
    for x,y in ((0,36),(48,36),(29,36),(43,33),(64,35),(48,42),(60,40)):
        t[y][x]="."
    t[36][48]="L"
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
    if name == "liga_eryon":
        header = "liga_eryon | Eryon League City 96x72\n"
        palette = "# block; . streets; , gardens; L central league headquarters\n"
        state = ("Registered city plan: League main building in the exact civic "
                 "center; arena and Elite Four state separate.\n\n")
    else:
        header = f"{name} | Eryon final approach design {len(t[0])}x{len(t)}\n"
        palette = ("# blocked; . floor; : mountain path; P plaza; C center; "
                   "M mart; L league; H hall\n")
        state = ("Registered HM-free route between Star Cave and the full-size "
                 "League City; battles inside central building.\n\n")
    return header + palette + state + "\n".join("".join(row) for row in t) + "\n"

def main():
    for name,fn,start,exit in (
        ("caminho_da_liga",route,(0,22),(47,22)),
        ("liga_eryon",league,(0,36),(48,36)),
    ):
        t=fn();seen=connected(t,start)
        walk={(x,y) for y,row in enumerate(t) for x,v in enumerate(row) if v!="#"}
        assert exit in seen, f"{name}: exit unreachable"
        p=ROOT/"docs/eryon"/f"{name}_terrain_plan.txt"
        p.write_text(render(name,t),encoding="utf-8")
        print(name,len(seen))


if __name__=="__main__":
    main()
