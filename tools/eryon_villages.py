#!/usr/bin/env python3
"""Generate distinct Eryon rest villages between major gym cities.

These are 36x30 ASCII design plans, NOT compiled GBA maps.
"""
from collections import deque
from pathlib import Path

W,H=36,30
ROOT=Path(__file__).resolve().parents[1]
VILLAGES={
    "vila_dos_pomares": ("Pomares", "orchard"),
    "vila_da_neblina": ("Neblina", "mist"),
    "refugio_cristal": ("Refugio Cristal", "crystal"),
    "posto_oriental": ("Posto Oriental", "outpost"),
    "vila_das_aguas": ("Vila das Aguas", "water"),
    "aldeia_dos_ecos": ("Aldeia dos Ecos", "forest"),
    "vila_do_pico": ("Vila do Pico", "peak"),
}
BUILDINGS={"C":(12,12),"M":(24,12),"H":(12,20),"I":(24,20)}


def village(name):
    if name not in VILLAGES:
        raise ValueError(name)
    kind=VILLAGES[name][1]
    t=[["#" for _ in range(W)] for _ in range(H)]
    for y in range(13,17):
        for x in range(W):
            t[y][x]="."
    for x in range(16,20):
        for y in range(H):
            t[y][x]="."
    for y in (8,23):
        for x in range(6,30):
            t[y][x]="."
    for x in (8,27):
        for y in range(8,24):
            t[y][x]="."
    for y in range(12,19):
        for x in range(14,22):
            t[y][x]="P"
    for marker,(x,y) in BUILDINGS.items():
        t[y][x]=marker
    # Different districts for each village, with connected paths.
    special={
        "orchard": (5,5,","),
        "mist": (30,5,","),
        "crystal": (5,25,":"),
        "outpost": (30,25,":"),
        "water": (5,5,":"),
        "forest": (30,5,","),
        "peak": (30,25,":"),
    }
    cx,cy,ground=special[kind]
    for y in range(max(1,cy-3),min(H-1,cy+4)):
        for x in range(max(1,cx-3),min(W-1,cx+4)):
            if (x-cx)**2+(y-cy)**2<=9 and t[y][x]=="#":
                t[y][x]=ground
    for x in range(min(cx,8 if cx<18 else 27),max(cx,8 if cx<18 else 27)+1):
        t[cy][x]="."
    for y in range(min(cy,8 if cy<15 else 23),max(cy,8 if cy<15 else 23)+1):
        t[y][8 if cx<18 else 27]="."
    t[cy][cx]="P"
    return t


def reachable(t,start=(0,14)):
    q=deque([start]);seen={start}
    while q:
        x,y=q.popleft()
        for nx,ny in ((x+1,y),(x-1,y),(x,y+1),(x,y-1)):
            if 0<=nx<W and 0<=ny<H and t[ny][nx]!="#" and (nx,ny) not in seen:
                seen.add((nx,ny));q.append((nx,ny))
    return seen


def render(name,t):
    return (f"{VILLAGES[name][0]} | Eryon village concept 36x30\n"
            "# barrier; . path; , grove; : stone; P plaza; C center; M mart; H home; I inn\n"
            "Design only: buildings, encounters, warp links and interiors are not implemented.\n\n"
            +"\n".join("".join(row) for row in t)+"\n")


def main():
    out=ROOT/"docs/eryon/vilas"
    out.mkdir(parents=True,exist_ok=True)
    for name in VILLAGES:
        t=village(name)
        seen=reachable(t)
        required={(0,14),(W-1,14),(18,0),(18,H-1)}
        required.update(BUILDINGS.values())
        assert required<=seen, f"{name}: blocked exit or facility"
        (out/f"{name}_village_plan.txt").write_text(render(name,t),encoding="utf-8")
        print(name,len(seen))


if __name__=="__main__":
    main()
