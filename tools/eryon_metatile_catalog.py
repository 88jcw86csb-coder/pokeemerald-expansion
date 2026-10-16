#!/usr/bin/env python3
"""Render a catalog of *actual compiled primary metatiles* for visual selection.

The source engine stores per-metatile four ground and four overlay descriptors,
with 10-bit 8x8 index, two flip bits, and a 4-bit palette slot. Rendering
these allows checking candidate map block IDs before changing GBA terrain.
"""
from pathlib import Path
import sys
import struct
sys.path.insert(0,str(Path(__file__).resolve().parent))
from eryon_tileset_visuals import unpack_png
from eryon_preview_contact_sheet import write_rgb

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"build/eryon-metatiles"
P=ROOT/"data/tilesets/primary/general"

def pal(path):
    lines=path.read_text().splitlines()
    assert lines[:3]==["JASC-PAL","0100","16"],path
    return [tuple(int(x) for x in line.split()) for line in lines[3:19]]

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    tiles,pal_raw=unpack_png((P/"tiles.png").read_bytes())
    w=len(tiles[0]);h=len(tiles)
    cols=w//8
    total=cols*(h//8)
    print("Primary tile index count:",total)
    palette=[pal(P/"palettes"/f"{i:02d}.pal") for i in range(16)]
    b=(P/"metatiles.bin").read_bytes()
    ids=range(len(b)//16)
    scale=2; cell=16*scale+4; ncol=16; nrows=(len(ids)+ncol-1)//ncol
    ww=ncol*cell;hh=nrows*cell
    canvas=bytearray((31,43,52)*(ww*hh))
    report=[]
    for m in ids:
        words=struct.unpack_from("<8H",b,m*16)
        x0=(m%ncol)*cell+2;y0=(m//ncol)*cell+2
        report.append((m,[w&0x3ff for w in words],[w>>12 for w in words]))
        for layer in range(2):
            for n in range(4):
                word=words[layer*4+n]
                tile=word&0x3ff
                pl=word>>12
                if tile>=total or pl>=16:
                    continue
                tx=(tile%cols)*8;ty=(tile//cols)*8
                xoff=(n%2)*8;yoff=(n//2)*8
                for yy in range(8):
                    for xx in range(8):
                        px=7-xx if word&0x400 else xx
                        py=7-yy if word&0x800 else yy
                        ind=tiles[ty+py][tx+px]
                        if layer==1 and ind==0: continue
                        color=palette[pl][ind]
                        for sy in range(scale):
                            dest=((y0+(yoff+yy)*scale+sy)*ww+x0+(xoff+xx)*scale)*3
                            canvas[dest:dest+scale*3]=bytes(color)*scale
    img=OUT/"primary_general_512.png"
    write_rgb(img,ww,hh,canvas)
    (OUT/"index.txt").write_text(
      "\n".join(f"{m:03d}: tiles={t} palettes={p}" for m,t,p in report)+"\n",encoding="utf-8")
    print("catalog:",img,ww,hh)

if __name__=="__main__":main()
