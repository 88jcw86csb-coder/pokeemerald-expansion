#!/usr/bin/env python3
"""Create a distinct Eryon title banner with the existing 128x32 GBA OAM contract.

The original Emerald graphic is untouched. The Eryon banner is generated
deterministically before gbagfx/make and fits two 64x32 8bpp sprite halves.
"""
from pathlib import Path
import struct
import zlib

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "graphics/title_screen/eryon_version.png"
W, H = 128, 32
FONT = {
    "E": ("11111","10000","11110","10000","10000","10000","11111"),
    "R": ("11110","10001","10001","11110","10100","10010","10001"),
    "Y": ("10001","10001","01010","00100","00100","00100","00100"),
    "O": ("01110","10001","10001","10001","10001","10001","01110"),
    "N": ("10001","11001","10101","10101","10011","10001","10001"),
}
PALETTE = (
    (10,16,27),(14,45,57),(36,90,112),(68,150,156),
    (124,217,208),(242,227,178),(235,171,86),(69,51,107),
    (145,108,190),(255,255,243),(26,27,44),(60,61,113),
    (111,103,161),(207,210,237),(19,19,41),(255,255,255),
)

def chunk(kind, payload):
    return (struct.pack(">I", len(payload)) + kind + payload
            + struct.pack(">I", zlib.crc32(kind+payload)&0xFFFFFFFF))

def generate():
    px = [[0]*W for _ in range(H)]
    def point(x,y,c):
        if 0 <= x < W and 0 <= y < H:
            px[y][x]=c
    def block(x,y,c):
        for dy in range(3):
            for dx in range(3):
                point(x+dx,y+dy,c)
    # Angular crystal flourishes at either side of the Eryon wordmark.
    for x,y in ((8,15),(120,15)):
        for i in range(-6,7):
            if -3 <= i <= 3:
                point(x+i,y,5);point(x,y+i,4)
        point(x,y,9)
    for x,y in ((13,5),(115,25),(11,26),(118,5)):
        point(x,y,6)
        point(x+1,y+1,9)
    for i,ch in enumerate("ERYON"):
        for yy,row in enumerate(FONT[ch]):
            for xx,ink in enumerate(row):
                if ink == "1":
                    x=19+i*19+xx*3
                    y=4+yy*3
                    block(x+1,y+1,1)
                    block(x,y,6 if yy >= 5 else 4)
                    point(x,y,9)
    encoded=bytearray()
    for row in px:
        encoded.append(0)
        encoded.extend(row)
    payload=(b"\x89PNG\r\n\x1a\n"
             +chunk(b"IHDR",struct.pack(">IIBBBBB",W,H,8,3,0,0,0))
             +chunk(b"PLTE",bytes(v for rgb in PALETTE for v in rgb))
             +chunk(b"IDAT",zlib.compress(bytes(encoded),9))
             +chunk(b"IEND",b""))
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_bytes(payload)
    print(f"ERYON title: {OUT}, {W}x{H} indexed PNG")
    return OUT

if __name__ == "__main__":
    generate()
