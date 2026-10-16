#!/usr/bin/env python3
"""Deterministic, original 4bpp-compatible Eryon trainer portraits.

All sprites are authored from geometric pixel shapes, not recolors of Hoenn
trainers. Source is Python stdlib only (no runtime Pillow dependency).
PNG: 64x64, indexed 4-bit, 16 palette slots, transparent index 0.
This is the first *integrated* art pass, not the final full-detail art pass.
"""
from __future__ import annotations

import argparse
from pathlib import Path
import struct
import zlib

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "graphics/trainers/front_pics"

# Code, hair, coat, accent, skin, hair length, signature accessory.
# All leaders keep their existing trainer identities, teams, levels and flags.
CAST = (
    ("eryon_kael",       "#486b39", "#416c49", "#74b16b", "#e4a879", "short", "leaves"),
    ("eryon_volt",       "#d8ab45", "#25446c", "#fac85a", "#dfaa80", "spike", "coil"),
    ("eryon_bjorn",      "#aec6e3", "#344c75", "#c1e7ff", "#dbad98", "side",  "snow"),
    ("eryon_tessa",      "#9b5536", "#927051", "#d8a46a", "#c48963", "long",  "relic"),
    ("eryon_nyx",        "#42355e", "#282a57", "#9b8cca", "#d9a28b", "long",  "moon"),
    ("eryon_kaio",       "#b64632", "#682f30", "#ef813c", "#d2926e", "spike", "forge"),
    ("eryon_lyra",       "#947dbb", "#37365f", "#f0cf8a", "#daa3a0", "long",  "star"),
    ("eryon_ryu",        "#287a8c", "#29465f", "#c7dde3", "#cca48b", "long",  "dragon"),
    ("eryon_eclipse",    "#483956", "#26283d", "#9b74bc", "#d5a28c", "short", "eclipse"),
    ("eryon_eclipse_f",  "#9272b4", "#303049", "#b78fd2", "#d7ad99", "long",  "eclipse"),
    ("eryon_commander",  "#b9adc9", "#292943", "#d6b46b", "#d7a999", "long",  "eclipse"),
    # Liga de Eryon: four Elite Four specialists and Champion Aurelio.
    ("eryon_aria",       "#b8ddf0", "#29465e", "#deeffb", "#d8a994", "long",  "snow"),
    ("eryon_bastian",    "#49352c", "#686044", "#d6a263", "#bb947f", "short", "relic"),
    ("eryon_selene",     "#27243a", "#55476d", "#c8a2ec", "#d2a99b", "long",  "wisp"),
    ("eryon_darius",     "#2c343e", "#2d555c", "#6dab9e", "#c29a7f", "side",  "dragon"),
    ("eryon_aurelio",    "#ded1a9", "#264757", "#f8d77e", "#d5a486", "spike", "crown"),
    ("eryon_elya",       "#d4b58d", "#237d86", "#f0d394", "#dcae97", "long", "star"),
)

def rgb(value):
    return tuple(int(value[i:i+2], 16) for i in (1, 3, 5))

def shade(color, factor):
    return tuple(max(0, min(255, int(c*factor))) for c in color)

def palette(hair, coat, accent, skin):
    h, c, a, s = (rgb(x) for x in (hair, coat, accent, skin))
    colors = [
        (255, 0, 255), (23, 28, 43), (40, 43, 62),
        shade(c, .64), c, a, shade(a, 1.27),
        shade(h, .56), h, shade(h, 1.25),
        shade(s, .76), s, shade(s, 1.17),
        (211, 190, 135), (211, 218, 228), (253, 248, 229),
    ]
    return [tuple(min(255, ch) for ch in color) for color in colors]

def paint(name, hair, coat, accent, skin, cut, motif):
    w = h = 64
    p = [[0] * w for _ in range(h)]
    def put(x, y, color):
        if 0 <= x < w and 0 <= y < h:
            p[y][x] = color
    def rect(x0, y0, x1, y1, color):
        for y in range(max(0, y0), min(h, y1)):
            for x in range(max(0, x0), min(w, x1)):
                put(x, y, color)
    def oval(cx, cy, rx, ry, color):
        for y in range(max(0, cy-ry), min(h, cy+ry+1)):
            for x in range(max(0, cx-rx), min(w, cx+rx+1)):
                if (x-cx)**2 * ry**2 + (y-cy)**2 * rx**2 <= rx**2 * ry**2:
                    put(x, y, color)
    def line(x0, y0, x1, y1, color, thick=1):
        steps=max(abs(x1-x0),abs(y1-y0),1)
        for i in range(steps+1):
            x=x0+(x1-x0)*i//steps; y=y0+(y1-y0)*i//steps
            rect(x-thick//2,y-thick//2,x+1+thick//2,y+1+thick//2,color)
    # Dark outlined shoulders, dimensional coat and contrasting sleeves.
    oval(31, 60, 30, 21, 1)
    oval(31, 62, 27, 20, 3)
    oval(15, 55, 11, 14, 2)
    oval(49, 55, 11, 14, 2)
    oval(16, 57, 8, 12, 4)
    oval(47, 56, 8, 12, 4)
    rect(22, 43, 42, 64, 2)
    rect(24, 44, 40, 64, 4)
    line(23, 44, 34, 64, 5, 3)
    line(42, 44, 33, 64, 6, 2)
    # Collar and neutral neck, with facial outline and three skin values.
    rect(27, 39, 37, 48, 1)
    rect(28, 39, 36, 46, 11)
    oval(32, 26, 15, 17, 1)
    oval(32, 27, 13, 15, 10)
    oval(33, 26, 11, 14, 11)
    rect(25, 33, 39, 36, 12)
    # Long silhouettes stay readable in the 64px GBA portrait box.
    if cut == "long":
        oval(17, 31, 9, 24, 1)
        oval(47, 30, 8, 23, 1)
        oval(18, 31, 7, 22, 8)
        oval(46, 31, 6, 22, 8)
    if cut == "spike":
        for x,y in ((16,15),(24,8),(33,6),(43,10),(50,18)):
            line(x,23,x+3,y,7,5)
            line(x+1,22,x+3,y+2,8,3)
    if cut == "side":
        oval(44, 35, 9, 22, 7)
        oval(44, 35, 7, 20, 8)
    oval(30, 15, 17, 12, 7)
    oval(30, 14, 15, 10, 8)
    oval(28, 13, 12, 7, 9)
    rect(17, 19, 27, 24, 7)
    line(31, 8, 43, 19, 8, 5)
    # Eyes and mouth: pixels remain intentional when reduced on GBA.
    rect(25, 27, 29, 29, 1)
    rect(36, 27, 40, 29, 1)
    put(27, 27, 15); put(38, 27, 15)
    line(30, 35, 36, 35, 10)
    # Insignia and character signature, not just a palette recolor.
    if motif == "leaves":
        oval(44, 47, 4, 7, 5); oval(48, 43, 6, 3, 6)
        line(48, 42, 40, 55, 13)
    elif motif == "coil":
        oval(45, 49, 6, 6, 6); oval(45, 49, 3, 3, 1)
        line(46, 42, 43, 48, 15, 2)
    elif motif == "snow":
        for dx,dy in ((-5,0),(5,0),(0,-5),(0,5)):
            line(46, 48, 46+dx, 48+dy, 15, 2)
        oval(46, 48, 2, 2, 6)
    elif motif == "relic":
        rect(46, 45, 54, 56, 13); rect(48, 47, 52, 54, 5)
        line(49, 47, 52, 52, 1)
    elif motif == "moon":
        oval(47, 48, 7, 7, 6); oval(50, 46, 6, 7, 3)
    elif motif == "forge":
        oval(45, 48, 6, 8, 5); oval(45, 49, 3, 5, 6)
        line(44, 44, 47, 37, 6, 2)
    elif motif == "star":
        line(45, 41, 45, 57, 6, 2); line(38, 49, 52, 49, 6, 2)
        oval(45, 49, 2, 2, 15)
    elif motif == "dragon":
        line(45, 42, 50, 47, 14, 3); line(50,47,42,55,14,3)
        line(47, 45, 51, 43, 6, 2)
    elif motif == "eclipse":
        oval(46, 48, 7, 7, 13); oval(46, 48, 5, 5, 2)
        oval(49, 46, 4, 5, 3); line(45,39,45,57,6,1)
    elif motif == "wisp":
        # Selene's spectral flame and trailing ethereal ribbons.
        oval(46, 49, 5, 8, 6); oval(45, 48, 3, 6, 3)
        line(47, 43, 50, 38, 5, 2); line(43, 50, 39, 56, 14, 2)
    elif motif == "crown":
        # Aurélio's laurel medallion: not Wallace's costume or portrait.
        line(42, 54, 42, 44, 13, 2); line(50, 54, 50, 44, 13, 2)
        line(42, 45, 46, 40, 14, 2); line(50, 45, 46, 40, 14, 2)
        oval(46, 51, 3, 3, 6)
    # White/cream piping improves silhouettes without transparency tricks.
    line(21, 48, 18, 60, 14)
    line(41, 45, 43, 59, 13)
    if name == "eryon_elya":
        # Field researcher Elya: upright spectacles, crystal cap pin,
        # slim research collar and a distinct shoulder-length hair shape.
        # Keep the face / silhouette different from Lyra's long hair.
        rect(22, 24, 11, 4, 14)
        rect(35, 24, 11, 4, 14)
        rect(31, 25, 5, 2, 13)
        rect(23, 25, 8, 2, 3)
        rect(36, 25, 8, 2, 3)
        line(25, 18, 22, 36, 7, 2)
        line(46, 17, 49, 33, 7, 2)
        rect(27, 41, 10, 8, 9)
        rect(29, 45, 6, 3, 4)
        rect(37, 49, 6, 10, 14)
    if name == "eryon_commander":
        # The commander's ceremonial crescent headpiece and epaulettes must
        # read differently from the female Eclipse operative even in 4bpp
        # grayscale/index space, not merely through palette recoloring.
        line(22, 8, 29, 3, 14, 3)
        line(29, 3, 38, 6, 14, 3)
        rect(28, 3, 35, 6, 15)
        oval(14, 52, 11, 5, 13)
        oval(51, 52, 10, 5, 13)
        line(17, 49, 14, 61, 15, 2)
        line(47, 49, 50, 61, 15, 2)
        rect(28, 46, 36, 50, 6)
    return p, palette(hair, coat, accent, skin)

def png_chunk(tag, payload):
    return struct.pack(">I", len(payload))+tag+payload+struct.pack(
        ">I", zlib.crc32(tag+payload)&0xffffffff)

def indexed_png(pixels, colors):
    width=height=64
    # Two 4-bit palette indices per byte, row filter type 0.
    data=bytearray()
    for row in pixels:
        data.append(0)
        data.extend((row[i] << 4) | row[i+1] for i in range(0,width,2))
    pal=bytes(v for rgb in colors for v in rgb)
    return (b"\x89PNG\r\n\x1a\n"
            +png_chunk(b"IHDR",struct.pack(">IIBBBBB",width,height,4,3,0,0,0))
            +png_chunk(b"PLTE",pal)
            +png_chunk(b"IDAT",zlib.compress(bytes(data),9))
            +png_chunk(b"IEND",b""))

# Field sprite shares the existing 16-color NPC_4 palette, avoiding a
# dangerous global palette remap. 0 is the field sprite's transparent index.
ECLIPSE_FIELD_PALETTE = (
    (115,197,164), (255,213,180), (255,197,148), (222,148,115),
    (123,65,65), (106,139,172), (57,74,98), (8,16,32),
    (213,115,164), (164,65,115), (82,32,65), (213,213,213),
    (139,139,148), (65,65,82), (255,255,255), (0,0,0),
)

def make_eclipse_field_sprite(dest):
    """8 GBA-ready 16x32 frames arranged 2 columns x 4 rows."""
    width, height = 32, 128
    canvas = [[0]*width for _ in range(height)]
    def rect(x, y, w, h, value):
        for yy in range(y, y+h):
            for xx in range(x, x+w):
                if 0 <= xx < width and 0 <= yy < height:
                    canvas[yy][xx] = value
    for frame in range(8):
        ox, oy=(frame % 2)*16, (frame // 2)*32
        # New angular field uniform: violet cap with eclipse emblem,
        # navy split tunic and boots, not a recolored Aqua member.
        step = (-1 if frame % 3 == 1 else 1 if frame % 3 == 2 else 0)
        rect(ox+5,oy+6,7,8,15)    # hair/head outline
        rect(ox+6,oy+7,5,8,2)     # face
        rect(ox+4,oy+4,9,5,7)     # cap band
        rect(ox+5,oy+4,7,2,9)     # violet trim
        rect(ox+9,oy+5,2,2,14)    # emblem
        rect(ox+10,oy+5,1,2,7)
        rect(ox+3,oy+15,11,12,15) # coat shadow silhouette
        rect(ox+4,oy+16,9,10,7)   # dark uniform
        rect(ox+5,oy+17,7,7,10)   # purple panels
        rect(ox+7,oy+17,2,9,9)    # jacket centre
        rect(ox+7,oy+20,2,3,14)   # clasp
        rect(ox+2,oy+17,2,8,6)    # left sleeve
        rect(ox+13,oy+17,2,8,6)   # right sleeve
        rect(ox+5+step,oy+26,3,4,15)
        rect(ox+9-step,oy+26,3,4,15)
        rect(ox+5+step,oy+26,3,3,7)
        rect(ox+9-step,oy+26,3,3,7)
        if frame in (2,3):
            rect(ox+5,oy+10,6,3,7) # back hat / coat
            rect(ox+7,oy+21,3,3,14)
            rect(ox+8,oy+21,2,3,7)
        elif frame in (4,5,6,7):
            rect(ox+5,oy+11,2,2,1)
        else:
            rect(ox+6,oy+11,2,2,15)
            rect(ox+10,oy+11,2,2,15)
    pal=bytes(v for color in ECLIPSE_FIELD_PALETTE for v in color)
    rows=bytearray()
    for row in canvas:
        rows.append(0)
        rows.extend((row[i]<<4)|row[i+1] for i in range(0,width,2))
    payload=(b"\x89PNG\r\n\x1a\n"
        +png_chunk(b"IHDR",struct.pack(">IIBBBBB",width,height,4,3,0,0,0))
        +png_chunk(b"PLTE",pal)
        +png_chunk(b"IDAT",zlib.compress(bytes(rows),9))
        +png_chunk(b"IEND",b""))
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_bytes(payload)
    return dest

# Eryon's protagonist is a teal-clad explorer with a cream cap, dark
# trousers and a circular backpack emblem, NOT Brendan/May's costume.
# For player movement keep the exact original sprite-strip dimensions and
# animation frame counts, including bikes, fishing and underwater.
HERO_FIELD_PALETTE = (
    (115,197,164), (255,222,190), (238,181,139), (205,142,110),
    (112,72,49), (56,136,148), (32,92,111), (23,52,74),
    (20,35,55), (246,233,200), (224,180,96), (69,131,87),
    (184,104,66), (94,62,53), (255,255,248), (0,0,0),
)

def indexed_strip_png(canvas, palette):
    height, width = len(canvas), len(canvas[0])
    assert width % 2 == 0 and all(len(row) == width for row in canvas)
    raw=bytearray()
    for row in canvas:
        raw.append(0)
        raw.extend((row[i]<<4)|row[i+1] for i in range(0,width,2))
    pal=bytes(component for rgb in palette for component in rgb)
    return (b"\x89PNG\r\n\x1a\n"
          + png_chunk(b"IHDR",struct.pack(">IIBBBBB",width,height,4,3,0,0,0))
          + png_chunk(b"PLTE",pal)
          + png_chunk(b"IDAT",zlib.compress(bytes(raw),9))
          + png_chunk(b"IEND",b""))

def hero_frame(size, phase, action, female=False):
    """One player frame, with no original Emerald character art reused."""
    canvas=[[0]*size for _ in range(32)]
    def rect(x,y,w,h,c):
        for yy in range(max(0,y),min(32,y+h)):
            for xx in range(max(0,x),min(size,x+w)):
                canvas[yy][xx]=c
    center=size//2
    shift=(-1,0,1)[phase%3]
    x=center-8
    # Distinctive square teal-and-cream cap with amber star insignia.
    rect(x+4,2,8,8,15); rect(x+5,3,6,5,9)
    rect(x+4,2,8,3,5); rect(x+5,2,5,2,9)
    rect(x+9,3,2,2,10); rect(x+2,8,12,2,6)
    rect(x+5,10,6,5,2)
    rect(x+5,11,2,2,15);rect(x+9,11,2,2,15)
    # Explorer's cream jacket and teal vest.
    rect(x+3,15,11,12,15)
    rect(x+4,16,9,10,9)
    rect(x+5,17,7,9,5)
    rect(x+7,17,3,9,6)
    rect(x+3,16,2,11,13)
    rect(x+13,16,2,11,13)
    # Dark two-tone shorts, stride-specific boots.
    rect(x+5+shift,26,3,4,8); rect(x+10-shift,26,3,4,8)
    rect(x+4+shift,29,4,2,15); rect(x+10-shift,29,4,2,15)
    if action in ("bike","acro"):
        # Bicycle is part of the 32px-wide sprite (wheels/tubes).
        if size == 32:
            rect(2,26,7,4,15);rect(23,26,7,4,15)
            rect(4,27,3,2,6);rect(25,27,3,2,6)
            rect(8,24,14,2,10)
    elif action in ("surf","underwater"):
        if size == 32:
            rect(2,25,28,6,5);rect(4,26,24,3,14)
            rect(7,30,18,2,6)
    elif action == "fishing":
        if size == 32:
            rect(25,3,2,23,4);rect(24,3,3,3,13)
            rect(18,13,9,2,10)
    elif action == "field":
        rect(x+13,15,2,6,10)
    elif action == "running":
        rect(x+3,17+shift,2,10,6)
    if female:
        # Longer side braids and amber circlet, unlike the original May sprite.
        rect(x+2,8,3,16,4)
        rect(x+12,9,3,16,4)
        rect(x+3,6,10,2,10)
    if phase%4 in (2,3):
        # Back-facing backpack clearly visible on some animations.
        rect(x+5,15,7,10,7); rect(x+6,16,5,7,5)
        rect(x+7,18,3,3,10)
    return canvas

def generate_hero_girl_assets():
    base=ROOT/"graphics/object_events/pics/people/eryon_hero_f"
    base.mkdir(parents=True,exist_ok=True)
    formats={
        "walking":(9,16,"walking"),"running":(9,16,"running"),
        "field_move":(5,32,"field"),"surfing":(6,32,"surf"),
        "mach_bike":(9,32,"bike"),"acro_bike":(27,32,"acro"),
        "fishing":(12,32,"fishing"),"underwater":(4,32,"underwater"),
        "watering":(6,32,"field"),"decorating":(1,16,"field"),
    }
    for name,(count,size,action) in formats.items():
        frames=[hero_frame(size,i,action,True) for i in range(count)]
        rows=[[pixel for frame in frames for pixel in frame[y]]
              for y in range(32)]
        (base/(name+".png")).write_bytes(indexed_strip_png(
            rows,HERO_FIELD_PALETTE))
    # All player actions, both genders and reflections share one palette.
    # Their original Emerald graphics stay on disk and are not deleted.
    front, colors=paint("eryon_hero_f", "#674135", "#366c79",
                        "#dbb269", "#d3a083", "long", "star")
    (OUT/"eryon_hero_f.png").write_bytes(indexed_png(front,colors))
    back=[]
    for frame in range(4):
        pixels=[[0]*64 for _ in range(64)]
        def rect(x,y,w,h,c):
            for yy in range(max(0,y),min(64,y+h)):
                for xx in range(max(0,x),min(64,x+w)):
                    pixels[yy][xx]=c
        rect(20,9,26,38,7);rect(23,10,22,37,8)
        rect(22,8,24,8,5);rect(24,10,20,5,6)
        rect(18,30,33,34,1);rect(21,31,26,32,4)
        rect(25,33,20,30,5);rect(27,36,16,22,3)
        rect(28,39,14,12,7);rect(31,42,8,7,13)
        rect(35,43,3,4,6)
        rect(12,43+frame,9,6,2);rect(46,35-frame*2,11,6,2)
        if frame>=2:
            rect(53,25,5,5,14);rect(55,26,2,3,1)
        back.extend(pixels)
    (ROOT/"graphics/trainers/back_pics/eryon_hero_f.png").write_bytes(
        indexed_strip_png(back,colors))
    # The May palette color indices are replaced in the Eryon build,
    # but Hoenn's original sprite files remain untouched.
    print("ERYON_VISUAL female explorer x10 and battle front/back generated")

def generate_hero_assets():
    base=ROOT/"graphics/object_events/pics/people/eryon_hero"
    base.mkdir(parents=True,exist_ok=True)
    formats={
        "walking":(9,16,"walking"),"running":(9,16,"running"),
        "field_move":(5,32,"field"),"surfing":(6,32,"surf"),
        "mach_bike":(9,32,"bike"),"acro_bike":(27,32,"acro"),
        "fishing":(12,32,"fishing"),"underwater":(4,32,"underwater"),
    }
    for name,(count,size,action) in formats.items():
        frames=[hero_frame(size,i,action) for i in range(count)]
        rows=[[pixel for frame in frames for pixel in frame[y]]
              for y in range(32)]
        (base/(name+".png")).write_bytes(indexed_strip_png(
            rows,HERO_FIELD_PALETTE))
    pal=(ROOT/"graphics/object_events/palettes/eryon_hero.pal")
    lines=["JASC-PAL","0100","16"]
    lines.extend(" ".join(str(c) for c in rgb) for rgb in HERO_FIELD_PALETTE)
    pal.write_text("\n".join(lines)+"\n",encoding="utf-8")
    reflection=ROOT/"graphics/object_events/palettes/eryon_hero_reflection.pal"
    reflected=[tuple(min(255,int(c*0.75)) for c in color)
               for color in HERO_FIELD_PALETTE]
    reflection.write_text("\n".join(["JASC-PAL","0100","16"]+[
        " ".join(str(c) for c in rgb) for rgb in reflected])+"\n",
        encoding="utf-8")
    # New trainer portrait and complete throwing animation strip.
    front, colors=paint("eryon_hero", "#63432b", "#366c79",
                        "#dbb269", "#d3a083", "spike", "star")
    (OUT/"eryon_hero.png").write_bytes(indexed_png(front,colors))
    back=[]
    for frame in range(4):
        pixels=[[0]*64 for _ in range(64)]
        def rect(x,y,w,h,c):
            for yy in range(max(0,y),min(64,y+h)):
                for xx in range(max(0,x),min(64,x+w)):
                    pixels[yy][xx]=c
        rect(22,8,22,28,7); rect(25,8,18,24,8)
        rect(21,8,24,7,5);rect(23,9,20,5,6)
        rect(19,31,30,32,1);rect(21,32,26,31,4)
        rect(25,34,20,29,3);rect(27,36,16,24,5)
        rect(29,39,12,12,7);rect(31,41,8,8,13)
        rect(34,43,3,4,6)
        rect(12,41+frame,10,6,2);rect(47,34-frame*2,11,6,2)
        rect(51,30-frame*2,6,6,11)
        if frame>=2:
            rect(53,25,5,5,14);rect(55,26,2,3,1)
        back.extend(pixels)
    # Back animation uses the same indexed palette as the hero front pic.
    backfile=ROOT/"graphics/trainers/back_pics/eryon_hero.png"
    backfile.write_bytes(indexed_strip_png(back,colors))
    print("ERYON_VISUAL hero overworld x8 and battle front/back generated")

# Dedicated GBA overworld portraits for the eight Eryon leaders.
# Each keeps a 16x32 frame, eight 2x4 frames, and NPC_4's reserved palette
# to avoid changing palette assignment or breaking existing NPC sprites.
ERYON_LEADER_FIELD_STYLES = {
    "kael":     (11, 4, 3, 10, "leaf"),
    "volt":     (5, 7, 14, 4, "spark"),
    "bjorn":    (14, 6, 11, 7, "snow"),
    "tessa":    (3, 4, 11, 13, "relic"),
    "nyx":      (10, 7, 8, 13, "moon"),
    "kaio":     (4, 13, 8, 15, "forge"),
    "lyra":     (8, 10, 14, 7, "star"),
    "ryu":      (6, 7, 11, 15, "dragon"),
}

def generate_leader_field_sprites():
    dest=ROOT/"graphics/object_events/pics/people/eryon_leaders"
    dest.mkdir(parents=True,exist_ok=True)
    produced=[]
    for name,(coat,hair,trim,boots,emblem) in ERYON_LEADER_FIELD_STYLES.items():
        canvas=[[0]*32 for _ in range(128)]
        def rect(x,y,w,h,c):
            for yy in range(max(0,y),min(128,y+h)):
                for xx in range(max(0,x),min(32,x+w)):
                    canvas[yy][xx]=c
        for n in range(8):
            x,y=(n%2)*16,(n//2)*32
            step=(0,-1,1)[n%3]
            # Individual haircut and head silhouette.
            rect(x+4,y+4,10,12,15)
            rect(x+5,y+5,8,10,1)
            rect(x+6,y+7,6,8,2)
            rect(x+4,y+4,10,4,hair)
            if name in ("nyx","lyra","tessa"):
                rect(x+3,y+7,3,13,hair)
                rect(x+12,y+7,3,13,hair)
            elif name in ("volt","kaio"):
                rect(x+4,y+2,3,6,hair)
                rect(x+9,y+1,4,6,hair)
            elif name in ("bjorn","ryu"):
                rect(x+3,y+6,11,3,trim)
            elif name=="kael":
                rect(x+5,y+2,7,3,coat)
            rect(x+6,y+12,2,2,15)
            rect(x+10,y+12,2,2,15)
            # Coats/sashes/capes; preserve transparent margins.
            rect(x+3,y+17,11,11,15)
            rect(x+4,y+18,9,9,coat)
            rect(x+3,y+18,2,8,trim)
            rect(x+12,y+18,2,8,trim)
            rect(x+7,y+18,3,9,hair)
            rect(x+7,y+20,3,2,trim)
            if name in ("bjorn","ryu","lyra"):
                rect(x+2,y+19,2,12,coat)
                rect(x+13,y+19,2,12,coat)
            rect(x+5+step,y+27,3,3,boots)
            rect(x+10-step,y+27,3,3,boots)
            # Symbol drawn onto the tunic (botanical / electric / icy /
            # archaeology / moon / forge / stellar / dragon).
            if emblem=="leaf":
                rect(x+8,y+20,2,3,11)
                rect(x+10,y+19,2,2,11)
            elif emblem=="spark":
                rect(x+9,y+18,2,3,14)
                rect(x+7,y+21,3,2,14)
            elif emblem=="snow":
                rect(x+8,y+20,5,1,14)
                rect(x+10,y+18,1,5,14)
            elif emblem=="relic":
                rect(x+8,y+19,4,5,11)
                rect(x+9,y+20,2,3,7)
            elif emblem=="moon":
                rect(x+8,y+19,4,5,14)
                rect(x+10,y+18,3,5,coat)
            elif emblem=="forge":
                rect(x+8,y+20,4,4,8)
                rect(x+9,y+19,2,2,11)
            elif emblem=="star":
                rect(x+10,y+19,1,6,14)
                rect(x+8,y+21,5,1,14)
            else:
                rect(x+8,y+19,4,2,11)
                rect(x+10,y+21,2,3,14)
            if n in (2,3):
                rect(x+6,y+9,7,3,hair)
                rect(x+7,y+20,3,5,trim)
        out=dest/("eryon_"+name+".png")
        out.write_bytes(indexed_strip_png(canvas,ECLIPSE_FIELD_PALETTE))
        produced.append(out)
    print("ERYON_VISUAL eight unique gym leader field sprites:",len(produced))
    return produced

def generate(target=OUT):
    target.mkdir(parents=True, exist_ok=True)
    created=[]
    for name, hair, coat, accent, skin, cut, motif in CAST:
        img, colors=paint(name,hair,coat,accent,skin,cut,motif)
        dest=target/(name+".png")
        dest.write_bytes(indexed_png(img,colors))
        created.append(dest)
        print("ERYON_VISUAL",dest.relative_to(ROOT) if dest.is_relative_to(ROOT) else dest)
    generate_hero_assets()
    generate_hero_girl_assets()
    generate_leader_field_sprites()
    field = make_eclipse_field_sprite(
        ROOT / "graphics/object_events/pics/people/eryon_eclipse.png")
    print("ERYON_VISUAL", field.relative_to(ROOT))
    return created

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--out",type=Path,default=OUT)
    args=parser.parse_args()
    generate(args.out)
