#!/usr/bin/env python3
"""Informational audit of Eryon's provisional map and character visuals.

This does NOT certify artwork originality or playability. It reports legacy
resources and simple terrain signals to guide incremental replacements.
Run: python3 tools/eryon_visual_audit.py [--json] [--strict]
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import struct

ROOT = Path(__file__).resolve().parents[1]
MAPS = ROOT / "data" / "maps"
LAYOUTS = ROOT / "data" / "layouts"


def audit():
    layouts = json.loads((LAYOUTS / "layouts.json").read_text(encoding="utf-8"))
    regional_layouts = {
        item["id"]: item for item in layouts["layouts"]
        if item["id"].startswith("LAYOUT_ERYON_")
    }
    base_digests = set()
    for file in LAYOUTS.glob("*/map.bin"):
        if not file.parent.name.startswith("Eryon_"):
            base_digests.add(hashlib.sha256(file.read_bytes()).hexdigest())

    regions = []
    all_gfx = Counter()
    borrowed_secondary = Counter()
    portrait_pics = {}
    for info_path in sorted(MAPS.glob("Eryon_*/map.json")):
        info = json.loads(info_path.read_text(encoding="utf-8"))
        layout = regional_layouts[info["layout"]]
        filename = ROOT / layout["blockdata_filepath"]
        raw = filename.read_bytes()
        expected_size = 2 * layout["width"] * layout["height"]
        if len(raw) != expected_size:
            raise ValueError(f"{info_path.parent.name}: wrong map.bin length")
        tiles = struct.unpack(f"<{len(raw) // 2}H", raw)
        # Bits 0-9 identify the metatile; collision/elevation are independent.
        freqs = Counter(block & 0x03FF for block in tiles)
        top_id, top_count = freqs.most_common(1)[0]
        gfx = Counter(event["graphics_id"] for event in info["object_events"])
        all_gfx.update(gfx)
        borrowed_secondary[layout["secondary_tileset"]] += 1
        regions.append({
            "name": info_path.parent.name,
            "width": layout["width"],
            "height": layout["height"],
            "secondary_tileset": layout["secondary_tileset"],
            "distinct_metatiles": len(freqs),
            "dominant_metatile": top_id,
            "dominant_tile_fraction": round(top_count / len(tiles), 4),
            "legacy_binary_exact_match": hashlib.sha256(raw).hexdigest() in base_digests,
            "object_events": len(info["object_events"]),
            "legacy_object_graphics": sum(
                count for key, count in gfx.items()
                if not key.startswith("OBJ_EVENT_GFX_ERYON_")
            ),
        })

    trainers = (ROOT / "src/data/trainers.party").read_text(encoding="utf-8")
    chunks = re.split(r"(?m)^=== (TRAINER_ERYON_[A-Z0-9_]+) ===\n", trainers)
    for i in range(1, len(chunks), 2):
        section = chunks[i + 1]
        pic = re.search(r"(?m)^Pic: (.+)$", section)
        if pic:
            portrait_pics[chunks[i]] = pic.group(1)

    return {
        "purpose": "inventory_only_not_originality_certification",
        "regional_maps": len(regions),
        "regional_layouts": len(regional_layouts),
        "legacy_tilesets": dict(borrowed_secondary),
        "overworld_graphics_top": dict(all_gfx.most_common(12)),
        "original_eryon_overworld_uses": sum(
            count for key, count in all_gfx.items() if key.startswith("OBJ_EVENT_GFX_ERYON_")
        ),
        "trainer_portraits": portrait_pics,
        "maps": regions,
        "exact_original_layout_matches": [m["name"] for m in regions if m["legacy_binary_exact_match"]],
        "placeholder_candidates": [
            m["name"] for m in regions if m["distinct_metatiles"] <= 4
            or m["dominant_tile_fraction"] > 0.80
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="Machine-readable full inventory")
    parser.add_argument("--strict", action="store_true",
                        help="Fail while borrowed sprites/tilesets or placeholder layouts remain")
    args = parser.parse_args()
    report = audit()
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(f"Eryon visual inventory: {report['regional_maps']} maps, "
              f"{report['regional_layouts']} dedicated layout entries")
        print("Legacy tilesets:", report["legacy_tilesets"])
        print("Exact Hoenn binary matches:", report["exact_original_layout_matches"])
        print("Placeholder terrain candidates:", report["placeholder_candidates"])
        print("Original Eryon overworld gfx uses:", report["original_eryon_overworld_uses"])
        print("Trainers with legacy portrait references:", len(report["trainer_portraits"]))
        print("Note: these heuristics cannot judge artistic identity or emulator visuals.")
    borrowed = bool(report["legacy_tilesets"]) or bool(report["overworld_graphics_top"])
    unfinished = bool(report["placeholder_candidates"]) or borrowed
    return 1 if args.strict and unfinished else 0


if __name__ == "__main__":
    raise SystemExit(main())
