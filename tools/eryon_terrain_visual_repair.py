#!/usr/bin/env python3
"""Repair Eryon's placeholder overworld metatiles without changing walkability.

Source audit: primary GENERAL metatile 0x003 is a piece of a Pokemart sign,
not stone. 0x001 was used for BOTH walls and roads, displaying the same grass.
Use actual primary GENERAL artwork and preserve all 16-bit block collision and
elevation bits. Stamped 3x3 building rooftops occupy only *already blocked*
cells in authoritative village/city plans: never close roads or relocate NPCs.
"""
from __future__ import annotations
from collections import Counter
from pathlib import Path
import json
import re
import struct

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT/"build/eryon-visual-terrain-report.json"
# Primary gTileset_General IDs reviewed in rendered atlas:
# 0x16: foliage, 0x69: actual earth trail (NOT blue water),
# 0x1C: clean grass and 0x6C: neutral rocky soil.
# No 0x003! That was a storefront SIGN, producing giant visual glitches.
VISUAL_METATILES = {0x001: 0x069, 0x002: 0x01C, 0x003: 0x06C}
WALL_METATILE = 0x016
# Building metatiles are the native three-column red-roof / front walls.
# Every existing 3x3 footprint is blocked already; collision cannot change.
HOUSE = ((0x008,0x009,0x00A),
         (0x010,0x011,0x012),
         (0x018,0x019,0x01A))

def retile_word(word):
    tile=word&0x03FF
    if tile not in VISUAL_METATILES:
        return word
    visual=WALL_METATILE if word&0x0C00 else VISUAL_METATILES[tile]
    return (word&0xFC00)|visual

def rows_for_map(name):
    sources=[
        ROOT/"docs/eryon/cidades"/(re.sub(r"(?<!^)(?=[A-Z])","_",name.removeprefix("Eryon_")).lower()+"_city_plan.txt"),
        ROOT/"docs/eryon/vilas"/(re.sub(r"(?<!^)(?=[A-Z])","_",name.removeprefix("Eryon_")).lower()+"_village_plan.txt"),
    ]
    for f in sources:
        if f.is_file():
            return f.read_text(encoding="utf-8").splitlines()[4:]
    return None

def stamp_visible_houses(blocks, width, height, plan):
    if not plan or len(plan)!=height or any(len(r)!=width for r in plan):
        return 0
    # Landmarks are *not* doors or warps; decorative roofing goes on already
    # inaccessible # cells, leaving the original marker and roads traversable.
    centers=[(x,y,s) for y,row in enumerate(plan) for x,s in enumerate(row)
             if s in "CGMHI"]
    used=set()
    placed=0
    for mx,my,s in centers:
        candidates=[]
        for y in range(max(1,my-7),min(height-3,my+4)):
            for x in range(max(1,mx-6),min(width-3,mx+5)):
                coords={(x+dx,y+dy) for dy in range(3) for dx in range(3)}
                if coords&used:
                    continue
                if all(plan[yy][xx]=="#" and (blocks[yy*width+xx]&0x0C00)
                       for xx,yy in coords):
                    distance=abs(x+1-mx)+abs(y+2-my)
                    # Prefer buildings above the landmark near its approach.
                    candidates.append((distance+max(0,y-my)*3,y,x,coords))
        if not candidates:
            continue
        _,y,x,coords=min(candidates,key=lambda c:(c[0],c[1],c[2]))
        for dy in range(3):
            for dx in range(3):
                i=(y+dy)*width+x+dx
                # ALWAYS preserve previous collision and elevation.
                blocks[i]=(blocks[i]&0xFC00)|HOUSE[dy][dx]
        used.update(coords)
        placed+=1
    return placed

def repair(layouts=None,write=True):
    data=layouts or json.loads((ROOT/"data/layouts/layouts.json").read_text(encoding="utf-8"))["layouts"]
    by_id={x["id"]:x for x in data}
    group=json.loads((ROOT/"data/maps/map_groups.json").read_text(encoding="utf-8"))["gMapGroup_Eryon"]
    stats=[]
    for name in group:
        info=json.loads((ROOT/"data/maps"/name/"map.json").read_text(encoding="utf-8"))
        layout=by_id[info["layout"]]
        w,h=layout["width"],layout["height"]
        file=ROOT/layout["blockdata_filepath"]
        original=file.read_bytes()
        if len(original)!=w*h*2:
            raise ValueError(f"{name}: corrupt map data length")
        words=list(struct.unpack(f"<{w*h}H",original))
        before=[word&0xFC00 for word in words]
        swaps=Counter()
        for i,word in enumerate(words):
            fixed=retile_word(word)
            if fixed!=word:
                swaps[f"{word&0x03ff:03x}->{fixed&0x03ff:03x}"]+=1
                words[i]=fixed
        plan=rows_for_map(name)
        placed=stamp_visible_houses(words,w,h,plan)
        # Large towns were solid walls of a single repeated tree motif.
        # Preserve a readable hedgerow along paths, but turn deep blocked
        # interior plots back into meadow until buildings are authored.
        settlements = ("Vila", "Cidade", "Neonara", "Frostheim",
                       "Arkhara", "Umbra", "Ignivar", "Drakonia",
                       "Lunaris", "Verdelume", "Posto", "Refugio", "Aldeia")
        if name.removeprefix("Eryon_").startswith(settlements):
            old=list(words)
            for y in range(1,h-1):
                for x in range(1,w-1):
                    i=y*w+x
                    if old[i]!=0x3C16:
                        continue
                    # Keep dense, clearly impassable leaf boundaries only
                    # immediately beside a genuine walkable avenue.
                    near_walk=any((old[(y+dy)*w+(x+dx)]&0x0C00)==0
                                  for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)))
                    if not near_walk and (x*13+y*7)%17 != 0:
                        words[i]=0x3C1C
        if before!=[word&0xFC00 for word in words]:
            raise AssertionError(f"{name}: collision/elevation changed")
        if write:
            file.write_bytes(struct.pack(f"<{len(words)}H",*words))
        stats.append({"map":name,"changed":sum(swaps.values()),
                      "buildings_on_preblocked_tiles":placed,
                      "substitutions":dict(swaps)})
    result={"region_maps":len(stats),"changed_tiles":sum(x["changed"] for x in stats),
            "new_building_landmarks":sum(x["buildings_on_preblocked_tiles"] for x in stats),
            "collision_elevation":"identical", "maps":stats}
    if write:
        REPORT.parent.mkdir(parents=True,exist_ok=True)
        REPORT.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print("ERYON RENDER REPAIR:",result["region_maps"],"maps",
          result["changed_tiles"],"bad placeholder tiles replaced;",
          result["new_building_landmarks"],"roof facades on blocked ground")
    return result

if __name__=="__main__":
    repair()
