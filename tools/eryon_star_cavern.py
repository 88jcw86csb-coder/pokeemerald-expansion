#!/usr/bin/env python3
"""Optional cave labyrinth before Eryon's Victory Road; design, not a ROM map."""
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
            "Design only: cave graphics, encounters, warps and collision not installed.\n\n"
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
