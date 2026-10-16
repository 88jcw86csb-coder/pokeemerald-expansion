#!/usr/bin/env python3
"""Authoritative 20x20 GBA terrain for Eryon's opening two maps.

Replaces the random one-cell tree obstacles and 0x003 storefront fragments
shown in Delta screenshots. Uses complete three-by-three native house
metatiles, continuous paths, clustered trees and correct collision/elevation.
This is an original LAYOUT arrangement using the engine's known metatiles;
native art is temporary pending completely original tilesets.
"""
from collections import deque
from pathlib import Path
import json
import struct

ROOT = Path(__file__).resolve().parents[1]
MAPS = {
    "Eryon_VilaAurora": [
        "TTT......===..TT.TTT",
        "TTT......===..TT.TTT",
        "TTT......===..TT.TTT",
        "TTT......===.....TTT",
        "..ABC....===...ABC..",
        "..DEF==..===...DEF..",
        "..GHI==..===...GHI..",
        "TT...==..===.==...TT",
        "TT...==========...TT",
        "TT.===============..",
        "...===============..",
        "...===============..",
        "..ABC==========ABC..",
        "..DEF==..===.==DEF..",
        "..GHI==========GHI..",
        "...==============...",
        "TTT......===.==..TTT",
        "TTT...TT.===.....TTT",
        "TTT...TT.===.....TTT",
        "TTT...TT.===.....TTT"
    ],
    "Eryon_Rota01": [
        "TTT......===....TTTT",
        "TTT......===....TTTT",
        "TTT.TTT..===....TTTT",
        "TTT.TTT...===TTTTTTT",
        "TTT.TTT...===TTTTTTT",
        "TTT.TTT..===.TTTTTTT",
        "TTT......===....TTTT",
        "TTT.....===.........",
        "TT......===.........",
        "TT......===.........",
        "TTTT.....===========",
        "..TT...=.===========",
        "..TT.....=======....",
        ".....===========..TT",
        ".....======.......TT",
        "TTTT....===.....TTTT",
        "TTTT..TT.===.TTTTTTT",
        "TTTT..TT.===.TTTTTTT",
        "TTTT..TT.===.TTTTTTT",
        "TTTT.....===....TTTT"
    ]
}
TILES = {
    ".": 0x301C,  # level 3: meadow, traversable
    "=": 0x3069,  # level 3: earth path, traversable
    "T": 0x3C16,  # native tree canopy, collision 3
    "A": 0x3C08, "B": 0x3C09, "C": 0x3C0A,
    "D": 0x3C10, "E": 0x3C11, "F": 0x3C12,
    "G": 0x3C18, "H": 0x3C19, "I": 0x3C1A,
}
# The professor, roadside trainers, study sign and both map boundaries must
# stay reachable in the REAL binary compiled for the GBA.
REQUIRED = {
    "Eryon_VilaAurora": ((10,0),(10,10),(12,12),(7,9)),
    "Eryon_Rota01": ((10,19),(19,10),(9,8),(5,13),(14,12),(7,11))
}

def layout_bytes(rows):
    if len(rows)!=20 or any(len(row)!=20 for row in rows):
        raise ValueError("Opening map must have exactly 20 rows of 20 cells")
    if any(ch not in TILES for row in rows for ch in row):
        raise ValueError("Unknown GBA metatile in first act")
    words=[TILES[ch] for row in rows for ch in row]
    return struct.pack("<400H", *words)

def component(data, start):
    words=struct.unpack("<400H",data)
    if words[start[1]*20+start[0]] & 0x0C00:
        return set()
    q=deque([start]);seen={start}
    while q:
        x,y=q.popleft()
        for nx,ny in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
            if 0<=nx<20 and 0<=ny<20 and (nx,ny) not in seen:
                if not words[ny*20+nx]&0x0C00:
                    seen.add((nx,ny));q.append((nx,ny))
    return seen

def validate(name, data):
    if len(data)!=800:
        raise ValueError("Expected 800-byte 20x20 map")
    required=REQUIRED[name]
    visited=component(data,required[0])
    if any(pos not in visited for pos in required):
        raise ValueError(f"{name}: blocked opening story event/exit")
    if len(visited)<180:
        raise ValueError(f"{name}: too few connected walkable tiles")

def generate():
    for name,rows in MAPS.items():
        binary=layout_bytes(rows)
        validate(name,binary)
        output=ROOT/"data/layouts"/name/"map.bin"
        output.write_bytes(binary)
        print("ERYON FIRST ACT:",name,
              "20x20, 800 bytes, verified walkable events",len(component(binary,REQUIRED[name][0])))

if __name__=="__main__":
    generate()
