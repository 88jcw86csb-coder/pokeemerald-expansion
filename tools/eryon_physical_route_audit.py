#!/usr/bin/env python3
"""Report collision-bit reachability and reciprocal transit across ALL Eryon maps.

Usage: python3 tools/eryon_physical_route_audit.py
       python3 tools/eryon_physical_route_audit.py --json-output build/eryon-physical-routes.json

WARNINGS are intentionally nonfatal because elevation, scripts, one-way doors,
tileset behavior, NPCs and runtime warps require Porymap/Delta confirmation.
Hard failures: missing/corrupt terrain, invalid warp map/index, nonreciprocal links.
"""
import argparse
import json
import struct
from collections import deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def connected(words, width, height, origin):
    x0, y0 = origin
    def walk(x, y):
        return 0 <= x < width and 0 <= y < height and (words[y*width+x] & 0xC00) == 0
    if not walk(x0, y0):
        return set()
    seen={(x0,y0)}
    queue=deque([(x0,y0)])
    while queue:
        x,y=queue.popleft()
        for nx,ny in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
            if (nx,ny) not in seen and walk(nx,ny):
                seen.add((nx,ny))
                queue.append((nx,ny))
    return seen


def audit():
    group=json.loads((ROOT/"data/maps/map_groups.json").read_text())["gMapGroup_Eryon"]
    layouts={l["id"]:l for l in json.loads((ROOT/"data/layouts/layouts.json").read_text())["layouts"]}
    maps={n:json.loads((ROOT/"data/maps"/n/"map.json").read_text()) for n in group}
    by_id={m["id"]:n for n,m in maps.items()}
    reports=[]
    errors=[]
    for name in group:
        m=maps[name]
        l=layouts.get(m["layout"])
        if l is None:
            errors.append(f"{name}: unknown layout {m['layout']}")
            continue
        width,height=l["width"],l["height"]
        file=ROOT/l["blockdata_filepath"]
        if not file.is_file():
            errors.append(f"{name}: missing map.bin")
            continue
        raw=file.read_bytes()
        if len(raw)!=2*width*height:
            errors.append(f"{name}: map.bin length {len(raw)} != {2*width*height}")
            continue
        words=struct.unpack("<"+"H"*(width*height),raw)
        warps=m.get("warp_events",[])
        warnings=[]
        positions=[]
        for index,w in enumerate(warps):
            pos=(w["x"],w["y"])
            positions.append(pos)
            if not (0<=pos[0]<width and 0<=pos[1]<height):
                errors.append(f"{name}: warp {index} outside terrain")
                continue
            other=by_id.get(w["dest_map"])
            if other is None:
                errors.append(f"{name}: warp {index} target missing")
                continue
            other_warps=maps[other]["warp_events"]
            dest=int(w["dest_warp_id"])
            if not (0<=dest<len(other_warps)):
                errors.append(f"{name}: warp {index} destination index invalid")
                continue
            reverse=other_warps[dest]
            if reverse["dest_map"]!=m["id"] or int(reverse["dest_warp_id"])!=index:
                errors.append(f"{name}: warp {index} not reciprocal")
            if (words[pos[1]*width+pos[0]]&0xC00)!=0:
                warnings.append(f"warp {index} collision bits are blocked")
        if positions:
            seen=connected(words,width,height,positions[0])
            for i,pos in enumerate(positions[1:],1):
                if pos not in seen:
                    warnings.append(f"warp 0 cannot reach warp {i} by clear blocks")
            for index,npc in enumerate(m.get("object_events",[])):
                p=(npc["x"],npc["y"])
                if not any((nx,ny) in seen for nx,ny in
                           ((p[0]-1,p[1]),(p[0]+1,p[1]),(p[0],p[1]-1),(p[0],p[1]+1))):
                    warnings.append(f"NPC {index} not adjacent to arrival component")
        reports.append({"map":name,"width":width,"height":height,"warps":len(warps),
                        "reachable_from_first_warp":len(connected(words,width,height,positions[0])) if positions else None,
                        "warnings":warnings})
    return {"maps_registered":len(group),"maps_inspected":len(reports),
            "errors":errors,"warnings":sum(len(r["warnings"]) for r in reports),
            "map_details":reports}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--json-output",type=Path)
    args=parser.parse_args()
    result=audit()
    print(f"Maps inspected: {result['maps_inspected']}/{result['maps_registered']}")
    print(f"Definite errors: {len(result['errors'])}; provisional warnings: {result['warnings']}")
    for err in result["errors"]:
        print("ERROR:",err)
    for item in result["map_details"]:
        for warning in item["warnings"]:
            print("REVIEW:",item["map"],warning)
    if args.json_output:
        args.json_output.parent.mkdir(parents=True,exist_ok=True)
        args.json_output.write_text(json.dumps(result,indent=2)+"\n")
    return 1 if result["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
