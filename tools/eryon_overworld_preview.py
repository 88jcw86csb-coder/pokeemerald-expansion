#!/usr/bin/env python3
"""Pixel-exact source-art 2x snapshots of Eryon's *repaired* GBA map data.

Not an emulator screenshot: renders primary GENERAL metatiles, combined
layers, index flips and the actual map.bin; does not simulate NPCs, camera
scroll, weather or secondary tileset animations.
"""
from pathlib import Path
import json
import struct
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from eryon_tileset_visuals import unpack_png
from eryon_preview_contact_sheet import write_rgb

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"build/eryon-overworld-previews"
PAL=ROOT/"data/tilesets/primary/general/palettes"

def load_palettes():
    palettes=[]
    for i in range(16):
        lines=(PAL/f"{i:02d}.pal").read_text(encoding="utf-8").splitlines()
        if lines[:3]!=["JASC-PAL","0100","16"]:
            raise ValueError(f"Palette {i:02d} incorrectly formatted")
        palettes.append([tuple(map(int,line.split())) for line in lines[3:19]])
    return palettes

def render_map(name,center_x=None,center_y=None):
    infos=ROOT/"data/maps"/name/"map.json"
    info=json.loads(infos.read_text(encoding="utf-8"))
    layouts={x["id"]:x for x in json.loads((ROOT/"data/layouts/layouts.json").read_text())["layouts"]}
    layout=layouts[info["layout"]]
    map_w,map_h=layout["width"],layout["height"]
    data=(ROOT/layout["blockdata_filepath"]).read_bytes()
    ids=struct.unpack(f"<{map_w*map_h}H",data)
    src=ROOT/"data/tilesets/primary/general"
    index,pal_data=unpack_png((src/"tiles.png").read_bytes())
    desc=(src/"metatiles.bin").read_bytes()
    palettes=load_palettes()
    cols=len(index[0])//8; tile_count=cols*(len(index)//8)
    cell_w,cell_h=24,18
    if center_x is None:
        npcs=info["object_events"]
        center_x=npcs[0]["x"] if npcs else map_w//2
        center_y=npcs[0]["y"] if npcs else map_h//2
    start_x=max(0,min(map_w-cell_w,center_x-cell_w//2))
    start_y=max(0,min(map_h-cell_h,center_y-cell_h//2))
    scale=2;w=cell_w*16*scale;h=cell_h*16*scale
    rgb=bytearray((20,26,40)*(w*h))
    for my in range(cell_h):
        for mx in range(cell_w):
            x,y=mx+start_x,my+start_y
            if not (0<=x<map_w and 0<=y<map_h):
                continue
            metatile=ids[y*map_w+x]&0x3FF
            if metatile>=len(desc)//16:
                continue   # secondary metatile; reported distinctly below
            words=struct.unpack_from("<8H",desc,metatile*16)
            for layer in range(2):
                for q in range(4):
                    word=words[layer*4+q]
                    idx=word&0x3FF;pi=word>>12
                    if idx>=tile_count:
                        continue  # secondary tiles need separate graphical bank
                    px0=(idx%cols)*8;py0=(idx//cols)*8
                    for yy in range(8):
                        for xx in range(8):
                            sx=7-xx if word&0x0400 else xx
                            sy=7-yy if word&0x0800 else yy
                            pixel=index[py0+sy][px0+sx]
                            if layer==1 and pixel==0:continue
                            color=palettes[pi][pixel]
                            vx=(mx*16+(q%2)*8+xx)*scale
                            vy=(my*16+(q//2)*8+yy)*scale
                            for dy in range(scale):
                                at=((vy+dy)*w+vx)*3
                                rgb[at:at+3*scale]=bytes(color)*scale
    return w,h,rgb,{"map":name,"center":[center_x,center_y],"window":[start_x,start_y,cell_w,cell_h],
                     "total_metatiles":len(ids),"unique_ids":len(set(x&0x3ff for x in ids)),
                     "old_bad_sign_tiles":sum(x&0x3ff==3 for x in ids)}

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    names=("Eryon_VilaAurora","Eryon_Rota01","Eryon_Neonara",
           "Eryon_BosqueDeLumina","Eryon_CidadeDaLiga")
    reports=[]
    for name in names:
        w,h,rgb,r=render_map(name)
        if r["old_bad_sign_tiles"]!=0:
            raise AssertionError(f"Metatile 0x003 remains in {name}")
        write_rgb(OUT/(name+".png"),w,h,rgb)
        reports.append(r)
        print("ERYON MAP SOURCE RENDER:",name,r["unique_ids"],"visual metatiles")
    (OUT/"manifest.json").write_text(json.dumps({
        "method":"source metatile render, not Delta gameplay",
        "art_quality":"unapproved_pending_emulator_test",
        "maps":reports},indent=2)+"\n")

if __name__=="__main__":main()
