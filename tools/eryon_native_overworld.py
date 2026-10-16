#!/usr/bin/env python3
"""Make the protagonist overworld frames visually safe on actual GBA hardware.

Our former rectangle-generated 16x32 avatars were demonstrably unfit for
release. Until bespoke Eryon frames are individually pixel-painted, use the
complete, correctly arranged native 4bpp Brendan/May animation sheets from
the decompilation under distinct palettes. The source sprites remain intact.

This is an honest temporary art-quality fallback: native sprites recolored
for Eryon, not new artwork. Retain all animation frames and the registered
event IDs; never rescale or resample pixel data.
"""
from pathlib import Path
import shutil
import struct

ROOT=Path(__file__).resolve().parents[1]
SPRITES=ROOT/"graphics/object_events/pics/people"
PAL=ROOT/"graphics/object_events/palettes"
ACTIONS={
    "walking":(144,32),
    "running":(144,32),
    "field_move":(160,32),
    "surfing":(192,32),
    "mach_bike":(288,32),
    "acro_bike":(864,32),
    "fishing":(384,32),
    "underwater":(128,32),
    "watering":(192,32),
    "decorating":(16,32),
}
# Preserve face/hair shading and the transparent slot. Recolor only
# a few costume and hat indices with restrained Eryon mineral/teal hues.
ACCENTS={
    "brendan":{5:(51,107,126),6:(34,83,105),7:(22,57,85),
               8:(16,42,65),10:(212,184,112),11:(169,128,65),
               12:(233,180,103),13:(185,129,66)},
    "may":{5:(66,99,123),6:(36,69,89),
           10:(86,182,164),11:(45,130,125),
           12:(224,176,114),13:(169,118,63)}
}

def png_info(path):
    raw=path.read_bytes()
    if raw[:8]!=b"\x89PNG\r\n\x1a\n":
        raise ValueError(f"Invalid PNG signature: {path}")
    w,h,bit,kind,compr,fil,interlace=struct.unpack(">IIBBBBB",raw[16:29])
    if (bit,kind,compr,fil,interlace)!=(4,3,0,0,0):
        raise ValueError(f"{path}: expected indexed 4bpp PNG, never resample")
    return w,h

def source_palette(name):
    lines=(PAL/(name+".pal")).read_text(encoding="ascii").splitlines()
    if lines[:3]!=["JASC-PAL","0100","16"] or len(lines)!=19:
        raise ValueError(f"{name}: malformed native GBA palette")
    rgb=[tuple(map(int,line.split())) for line in lines[3:]]
    if any(len(v)!=3 for v in rgb):
        raise ValueError("Invalid native JASC RGB entry")
    return rgb

def write_palette(path,colors):
    rows=["JASC-PAL","0100","16"]+[" ".join(str(c) for c in item) for item in colors]
    path.write_text("\n".join(rows)+"\n",encoding="ascii")

def install():
    for name,eryon in (("brendan","eryon_hero"),("may","eryon_hero_f")):
        original=SPRITES/name
        destination=SPRITES/eryon
        destination.mkdir(parents=True,exist_ok=True)
        for action,(w,h) in ACTIONS.items():
            src=original/(action+".png")
            if png_info(src)!=(w,h):
                raise ValueError(f"{name}/{action} has incorrect native sheet dimensions")
            shutil.copyfile(src,destination/src.name)
            if png_info(destination/src.name)!=(w,h):
                raise ValueError("Frame sheet damaged by copying")
        rgb=source_palette(name)
        for index,color in ACCENTS[name].items():
            rgb[index]=color
        write_palette(PAL/(eryon+".pal"),rgb)
        dark=[tuple(max(0,int(c*0.75)) for c in item) for item in rgb]
        write_palette(PAL/(eryon+"_reflection.pal"),dark)
        print("ERYON GBA NATIVE OVERWORLD:",name,"=>",eryon,
              "10 unscaled 4bpp native action sheets")
    print("NOTICE: Protagonists use native recolored source art; bespoke Eryon sprite sheets still pending.")

if __name__=="__main__":
    install()
