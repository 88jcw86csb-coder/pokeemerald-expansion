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
    # Keep 24 pre-existing terrain adjustments that were saved only in map.bin.
    for y, spans in (
        (18, ((16, 16), (17, 17), (18, 18), (33, 33), (34, 34), (35, 35))),
        (19, ((16, 16), (17, 17), (18, 18), (33, 33), (34, 34), (35, 35))),
        (20, ((16, 16), (17, 17), (18, 18))),
        (24, ((29, 29), (30, 30), (31, 31))),
        (25, ((29, 29), (30, 30), (31, 31))),
        (26, ((29, 29), (30, 30), (31, 31))),
    ):
        for x0, x1 in spans:
            for x in range(x0, x1 + 1):
                t[y][x] = ":"
    # Upper twin-summit rim, northern stargazer plaza, southern return loop.
    for y, a, b in ((10,10,16),(14,16,25),(7,25,38),(34,25,32),(31,32,40)):
        for x in range(a,b+1):
            t[y][x] = ":"
    for x, a, b in ((16,10,14),(25,7,14),(32,31,34),(40,23,31)):
        for y in range(a,b+1):
            t[y][x] = ":"
    for y in range(6,11):
        for x in range(20,27):
            if (x-23)**2/9+(y-8)**2/4 <= 1:
                t[y][x] = ":"
    for y in range(30,36):
        for x in range(34,40):
            if (x-36.5)**2/6.25+(y-33)**2/5 <= 1:
                t[y][x] = ":"
    # Newly carved eastern summit alcove above the existing lookout path.
    # Keep the generator authoritative so regeneration preserves the new terrain.
    for y in (12, 13, 14):
        for x in range(35, 40):
            t[y][x] = ":"
    # A narrow switchback connects the eastern summit alcove to the upper rim.
    # All existing ridge and road cells remain unchanged.
    for x in range(32, 36):
        t[12][x] = ":"
    for y in range(8, 13):
        t[y][32] = ":"
    # A new northern connector offers a shorter walk from the Star Memorial
    # to the eastern summit switchback without closing the original winding rim.
    for x in range(25, 33):
        t[11][x] = ":"
    for y in range(11, 15):
        t[y][26] = ":"
    for x in range(25, 27):
        t[14][x] = ":"
    # An optional summit birdwatching clearing branches north of the existing
    # shortcut without touching the main path or any object event.
    for y in range(8, 11):
        for x in range(27, 30):
            t[y][x] = "."
    t[11][28] = ":"
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
    # Preserve earlier 33 garden block refinements from the committed city.
    for x,y in ((64,44),(65,44),(67,44),(68,44),(69,44),(70,44),(72,44),(73,44),(74,44),(64,45),(65,45),(67,45),(68,45),(69,45),(64,46),(66,46),(67,46),(68,46),(69,46),(66,47),(67,47),(68,47),(69,47),(66,48),(68,48),(69,48),(66,49),(67,49),(68,49),(69,49),(66,50),(67,50),(69,50)):
        t[y][x]=","
    # Original north-east hill district: winding hill, oval planted court and
    # two accesses, from the central square and the east avenue.
    def terrace_step(x,y):
        for yy in range(y-1,y+2):
            for xx in range(x-1,x+2):
                if 0<xx<95 and 0<yy<71 and t[yy][xx]=="#":
                    t[yy][xx]="."
    stages=((60,34),(62,32),(65,30),(67,28),(70,26),(75,25),(79,25),(80,28))
    for (ax,ay),(bx,by) in zip(stages,stages[1:]):
        x,y=ax,ay
        while x!=bx or y!=by:
            terrace_step(x,y)
            if x!=bx: x+=1 if bx>x else -1
            if y!=by: y+=1 if by>y else -1
        terrace_step(bx,by)
    for y in range(20,32):
        for x in range(63,82):
            if ((x-71.5)/9)**2+((y-25.5)/5)**2<=1 and t[y][x]=="#":
                t[y][x]=","
    for y in range(25,30):
        terrace_step(70,y)
    t[25][70]="."
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
