#!/usr/bin/env python3
"""Generate eight new original Eryon gym arenas, no edits to existing map.bin.

Each arena is 24x18, 16-bit metatile words. Collision/elevation bits preserved:
floor 0x3001 (elevation 3, passable), walls 0x3C0D (elevation 3, blocked).
The gym signs/leader are accessible without any HMs. Entrance/exit use
scripted warps instead of repurposing legacy route connections.
"""
from collections import deque
from pathlib import Path
import struct

ROOT=Path(__file__).resolve().parents[1]
CITIES=("Verdelume","Neonara","Frostheim","Arkhara",
        "Umbra","Ignivar","Lunaris","Drakonia")
WIDTH,HEIGHT=24,18
FLOOR=0x3001
WALL=0x3C0D
DETAIL=0x3005

def layout(index):
    cells=[[FLOOR]*WIDTH for _ in range(HEIGHT)]
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if x in (0,WIDTH-1) or y in (0,HEIGHT-1):
                cells[y][x]=WALL
    # Eight distinct obstacle combinations, kept outside main corridors.
    for y in range(3,14):
        if y not in (8,10,12):
            cells[y][4+index%3]=WALL
            cells[y][19-index%3]=WALL
    for x in range(7,17):
        if x not in (8,11,12,13,16):
            cells[3+index%3][x]=WALL
    for x,y in ((7,14),(16,14),(6,7),(17,7)):
        cells[y][x]=DETAIL
    return cells

def validate(cells):
    checkpoints={(12,15),(12,6),(12,8),(8,10),(16,10),(12,16)}
    for x,y in checkpoints:
        if cells[y][x] & 0x0C00:
            raise ValueError(f"event blocked at {(x,y)}")
    q=deque([(12,15)])
    seen={(12,15)}
    while q:
        x,y=q.popleft()
        for nx,ny in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
            if (0<=nx<WIDTH and 0<=ny<HEIGHT and
                not cells[ny][nx]&0x0C00 and (nx,ny) not in seen):
                seen.add((nx,ny));q.append((nx,ny))
    floor={(x,y) for y in range(HEIGHT) for x in range(WIDTH)
           if not cells[y][x]&0x0C00}
    if floor != seen or not checkpoints <= seen:
        raise ValueError("gym floor disconnected or event unreachable")
    return len(seen)

def generate():
    result=[]
    for i,city in enumerate(CITIES):
        cells=layout(i)
        walk=validate(cells)
        payload=struct.pack(f"<{WIDTH*HEIGHT}H",
                            *(v for row in cells for v in row))
        path=ROOT/"data/layouts"/("GymEryon_"+city)/"map.bin"
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_bytes(payload)
        print("ERYON_GYM_ARENA",city,WIDTH,HEIGHT,"floor",walk)
        result.append(path)
    return result

if __name__=="__main__":
    generate()
