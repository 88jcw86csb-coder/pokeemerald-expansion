#!/usr/bin/env python3
"""Generate nearest-neighbor artwork contact sheets for honest visual review.

These are rendered from the exact 4bpp indexed PNG assets used by gbagfx.
They are not gameplay screenshots or Delta emulator results.
"""
from pathlib import Path
import json
import struct
import zlib

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"build/eryon-preview"
SIG=b"\x89PNG\r\n\x1a\n"

def load_png(path):
    raw=path.read_bytes()
    if not raw.startswith(SIG):
        raise ValueError(f"Bad PNG signature: {path}")
    off=8
    palette=None
    packed=[]
    width=height=bpp=color=None
    while off<len(raw):
        n=struct.unpack_from(">I",raw,off)[0]
        tag=raw[off+4:off+8]
        block=raw[off+8:off+8+n]
        got=struct.unpack_from(">I",raw,off+8+n)[0]
        if zlib.crc32(tag+block)&0xffffffff != got:
            raise ValueError(f"PNG CRC failure: {path} {tag!r}")
        off+=12+n
        if tag==b"IHDR":
            width,height,bpp,color,compress,filt,interlace=struct.unpack(">IIBBBBB",block)
            if (color,compress,filt,interlace)!=(3,0,0,0) or bpp not in (4,8):
                raise ValueError(f"Unsupported palette PNG {path}")
        elif tag==b"PLTE":
            palette=[tuple(block[i:i+3]) for i in range(0,len(block),3)]
        elif tag==b"IDAT":
            packed.append(block)
        elif tag==b"IEND":
            break
    if not palette or not packed:
        raise ValueError(f"Missing PNG palette/data: {path}")
    data=zlib.decompress(b"".join(packed))
    stride=(width*bpp+7)//8
    if len(data)!=(stride+1)*height:
        raise ValueError(f"Bad PNG image size: {path}")
    pixels=[]
    for y in range(height):
        row=data[y*(stride+1):(y+1)*(stride+1)]
        if row[0]!=0:
            raise ValueError(f"Generator must use lossless filter zero: {path}")
        if bpp==4:
            for byte in row[1:]:
                pixels.extend((byte>>4,byte&15))
        else:
            pixels.extend(row[1:])
    if len(pixels)!=width*height or max(pixels)>=len(palette):
        raise ValueError(f"Indexed pixels invalid: {path}")
    return width,height,pixels,palette

def draw(canvas,cw,ch,path,x,y,scale=3,crop=None):
    w,h,pix,pal=load_png(path)
    if crop:
        ox,oy,sw,sh=crop
    else:
        ox=oy=0;sw=w;sh=h
    for yy in range(sh):
        for xx in range(sw):
            k=pix[(oy+yy)*w+ox+xx]
            # Deliberately visualize palette index zero as transparency.
            color=((39,51,68) if ((xx//4+yy//4)%2) else (58,70,85)) if k==0 else pal[k]
            px=x+xx*scale
            py=y+yy*scale
            for dy in range(scale):
                start=((py+dy)*cw+px)*3
                canvas[start:start+3*scale]=bytes(color)*scale

def write_rgb(path,w,h,canvas):
    rows=b"".join(b"\0"+bytes(canvas[y*w*3:(y+1)*w*3]) for y in range(h))
    def chunk(tag,data):
        return (struct.pack(">I",len(data))+tag+data+
                struct.pack(">I",zlib.crc32(tag+data)&0xffffffff))
    raw=(SIG+chunk(b"IHDR",struct.pack(">IIBBBBB",w,h,8,2,0,0,0))+
         chunk(b"IDAT",zlib.compress(rows,9))+chunk(b"IEND",b""))
    path.write_bytes(raw)

def make_sheet():
    OUT.mkdir(parents=True,exist_ok=True)
    portraits=["eryon_hero","eryon_hero_f","eryon_elya"]
    portraits += ["eryon_"+n for n in (
        "kael","volt","bjorn","tessa","nyx","kaio","lyra","ryu",
        "eclipse","eclipse_f","commander","aria","bastian","selene",
        "darius","aurelio")]
    cols,scale,pad=5,3,10
    cell=64*scale+pad
    rows=(len(portraits)+cols-1)//cols
    w,h=cols*cell,rows*cell
    bitmap=bytearray((25,34,45)*(w*h))
    for i,name in enumerate(portraits):
        draw(bitmap,w,h,ROOT/"graphics/trainers/front_pics"/(name+".png"),
             i%cols*cell+pad//2,i//cols*cell+pad//2,scale)
    write_rgb(OUT/"personagens.png",w,h,bitmap)
    # Overworld and animation quality: two native 144x32 strips enlarged
    names=["eryon_hero","eryon_hero_f"]
    sw,sh=144*4+20,len(names)*(32*4+20)
    bitmap=bytearray((25,34,45)*(sw*sh))
    for i,name in enumerate(names):
        draw(bitmap,sw,sh,ROOT/"graphics/object_events/pics/people"/name/"walking.png",
             10,i*(32*4+20)+10,4)
    write_rgb(OUT/"protagonistas_animacao.png",sw,sh,bitmap)
    # The six secondary tilesets reveal the true state of environment art.
    names=["aurora","urban","forest","crystal","desert","lunar"]
    sw,sh=128*6+35,275
    bitmap=bytearray((25,34,45)*(sw*sh))
    for i,name in enumerate(names):
        draw(bitmap,sw,sh,ROOT/"data/tilesets/secondary"/("eryon_"+name)/"tiles.png",
             5+i*(128+5),5,1)
    write_rgb(OUT/"terrenos_tilesets.png",sw,sh,bitmap)
    manifest={
        "source":"generated GBA-indexed source artwork; not Delta screenshots",
        "portrait_order":portraits,
        "hero_order":names,
        "quality_status":"visual approval pending game rendering and pixel-art review"
    }
    (OUT/"manifest.json").write_text(json.dumps(manifest,indent=2)+"\n",encoding="utf-8")
    for name in ("personagens.png","protagonistas_animacao.png","terrenos_tilesets.png"):
        print("ERYON VISUAL PREVIEW:",OUT/name)

if __name__=="__main__":
    make_sheet()
