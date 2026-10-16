#!/usr/bin/env python3
"""Generate palette-indexed Eryon-specific secondary tileset *first pass*.

Six distinct biome-themed graphical banks, preserving source metatile layout
and its engine-side behavior/attributes. This is NOT full custom architecture
or finished hand-drawn biomes; advanced tileset painting is still required.
The output is deterministic and generated before make, not manually copied.
Only Python stdlib used to keep GitHub Actions reproducible.
"""
from __future__ import annotations
import colorsys
from pathlib import Path
import struct
import zlib

ROOT=Path(__file__).resolve().parents[1]
TILE_ROOT=ROOT/"data/tilesets/secondary"
THEMES={
    "aurora":   ("petalburg",(211,170,128),0),
    "urban":    ("rustboro",(83,137,155),1),
    "forest":   ("rustboro",(77,149,112),2),
    "crystal":  ("rustboro",(118,166,201),3),
    "desert":   ("rustboro",(202,135,86),4),
    "lunar":    ("rustboro",(125,109,180),5),
}

def chunk(tag,value):
    return (struct.pack(">I",len(value))+tag+value+
            struct.pack(">I",zlib.crc32(tag+value)&0xffffffff))

def unpack_png(raw):
    if raw[:8]!=b"\x89PNG\r\n\x1a\n":
        raise ValueError("expected a PNG")
    at=8
    palette=None
    parts=[]
    while at<len(raw):
        n=struct.unpack(">I",raw[at:at+4])[0];tag=raw[at+4:at+8]
        buf=raw[at+8:at+8+n];at+=12+n
        if tag==b"IHDR":
            w,h,bit,mode,_,_,_=struct.unpack(">IIBBBBB",buf)
        elif tag==b"PLTE":palette=buf
        elif tag==b"IDAT":parts.append(buf)
        elif tag==b"IEND":break
    if bit!=4 or mode!=3 or w%2:
        raise ValueError("only 4-bit indexed GBA tile PNGs supported")
    step=w//2
    data=zlib.decompress(b"".join(parts))
    previous=bytearray(step)
    offset=0
    rows=[]
    for y in range(h):
        filter_type=data[offset];offset+=1
        scan=bytearray(data[offset:offset+step]);offset+=step
        for i in range(step):
            a=scan[i-1] if i else 0
            b=previous[i]
            c=previous[i-1] if i else 0
            if filter_type==1:delta=a
            elif filter_type==2:delta=b
            elif filter_type==3:delta=(a+b)//2
            elif filter_type==4:
                p=a+b-c
                scores=(abs(p-a),abs(p-b),abs(p-c))
                delta=(a,b,c)[scores.index(min(scores))]
            elif filter_type==0:delta=0
            else:raise ValueError("unknown indexed PNG filter")
            scan[i]=(scan[i]+delta)&255
        previous=scan
        rows.append([(value>>4) for value in scan for _ in (0,)] +
                    []) if False else None
        rows.append([p for value in scan for p in (value>>4,value&15)])
    return rows,palette

def pack_png(rows,palette):
    width=len(rows[0]);height=len(rows)
    raw=bytearray()
    for row in rows:
        assert len(row)==width and width%2==0
        raw.append(0)
        raw.extend((row[i]<<4)|row[i+1] for i in range(0,width,2))
    return (b"\x89PNG\r\n\x1a\n"+
            chunk(b"IHDR",struct.pack(">IIBBBBB",width,height,4,3,0,0,0))+
            chunk(b"PLTE",palette)+
            chunk(b"IDAT",zlib.compress(bytes(raw),9))+chunk(b"IEND",b""))

def draw_eryon_details(rows,theme_index):
    """Retouch selected opaque tiles without changing 8x8 atlas positions."""
    height=len(rows);width=len(rows[0]);total=(width//8)*(height//8)
    cols=width//8
    for index in range(total):
        tx=(index%cols)*8;ty=(index//cols)*8
        area=[rows[ty+y][tx+x] for y in range(8) for x in range(8)]
        filled=sum(p!=0 for p in area)
        # Avoid partially transparent building / door / foliage silhouettes.
        # Distribute small decorative accents on dense surfaces only.
        if filled<54 or index%13 not in (3,7):
            continue
        cx=tx+3;cy=ty+3
        if theme_index in (0,1):
            coords=((0,0),(1,0),(0,1),(1,1))  # inlaid civic paving
        elif theme_index==2:
            coords=((0,0),(1,-1),(-1,1))       # leaf / fern flecks
        elif theme_index==3:
            coords=((0,-2),(-1,-1),(0,0),(1,-1),(0,1)) # crystal facets
        elif theme_index==4:
            coords=((-1,0),(0,0),(1,1))        # adobe / mineral flecks
        else:
            coords=((0,-2),(-1,0),(1,0),(0,2)) # star / orbit
        for dx,dy in coords:
            x=cx+dx;y=cy+dy
            if 0<=x<width and 0<=y<height and rows[y][x]!=0:
                rows[y][x]=13 if (dx+dy)%2 else 14
    return rows

def adjust_palette(rgb,target,theme_index):
    r,g,b=rgb
    if max(rgb)<28 or min(rgb)>242 or max(rgb)-min(rgb)<9:
        return rgb
    h,s,v=colorsys.rgb_to_hsv(r/255,g/255,b/255)
    th,ts,tv=colorsys.rgb_to_hsv(*(x/255 for x in target))
    # Tint midtones to create distinct regional material identities while
    # retaining luminance and sufficient edges for legibility on a small LCD.
    wt=(.16,.24,.24,.28,.28,.30)[theme_index]
    new_h=(h*(1-wt)+th*wt)
    ns=min(.86,max(.17,s*(.90 if theme_index==5 else 1.10)))
    if theme_index==3:ns=min(.78,ns+.08)
    rr,gg,bb=colorsys.hsv_to_rgb(new_h,ns,v)
    return tuple(max(0,min(255,round(x*255/8)*8)) for x in (rr,gg,bb))

def generate():
    items=[]
    for theme,(base,tint,idx) in THEMES.items():
        source=TILE_ROOT/base
        out=TILE_ROOT/("eryon_"+theme)
        (out/"palettes").mkdir(parents=True,exist_ok=True)
        pixels,palette=unpack_png((source/"tiles.png").read_bytes())
        expected_size=(128,80 if base=="petalburg" else 256)
        if (len(pixels[0]),len(pixels))!=expected_size:
            raise ValueError(f"{base} dimensions unexpectedly changed")
        (out/"tiles.png").write_bytes(pack_png(draw_eryon_details(pixels,idx),palette))
        for no in range(16):
            src=source/"palettes"/f"{no:02d}.pal"
            lines=src.read_text().splitlines()
            if lines[:3]!=["JASC-PAL","0100","16"] or len(lines)<19:
                raise ValueError(f"unexpected palette {src}")
            out_lines=lines[:3]
            for i,entry in enumerate(lines[3:19]):
                color=tuple(map(int,entry.split()))
                if len(color)!=3:raise ValueError("bad RGB")
                result=adjust_palette(color,tint,idx) if i not in (0,15) else color
                out_lines.append(" ".join(str(c) for c in result))
            (out/"palettes"/f"{no:02d}.pal").write_text(
                "\n".join(out_lines)+"\n",encoding="ascii")
        items.append(out)
        print("ERYON_TILESET",out.relative_to(ROOT))
    return items

if __name__=="__main__":
    generate()
