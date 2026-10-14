#!/usr/bin/env python3
"""Honest, non-blocking inventory of unfinished Eryon game systems.

CI reports missing work, while dedicated tests keep structural regressions fatal.
Passing this inventory is NOT evidence of a finished or emulator-tested ROM.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GYM_CITIES = (
    "Verdelume", "Neonara", "Frostheim", "Arkhara",
    "Umbra", "Ignivar", "Lunaris", "Drakonia",
)


def main():
    names = json.loads((ROOT / "data/maps/map_groups.json").read_text(
        encoding="utf-8"))["gMapGroup_Eryon"]
    maps = {
        name: json.loads((ROOT / "data/maps" / name / "map.json").read_text(
            encoding="utf-8"))
        for name in names
    }
    print(f"ERYON MAPS REGISTERED: {len(names)}")
    missing_stories = [
        name for name, info in maps.items()
        if not info["object_events"] and not info["bg_events"]
    ]
    print(f"MAPS WITHOUT INTERACTIVE STORY CONTENT: {len(missing_stories)}")
    for name in missing_stories:
        print(f"  TODO: {name}")

    implemented = []
    for suffix in GYM_CITIES:
        name = "Eryon_" + suffix
        script = (ROOT / "data/maps" / name / "scripts.inc").read_text(
            encoding="utf-8")
        battles = re.findall(
            r"\btrainerbattle_\w+\s+(TRAINER_ERYON_\w+)", script
        )
        badges = re.findall(r"\bsetflag\s+FLAG_BADGE\d+_GET\b", script)
        has_gym_battle = bool(battles and badges)
        if has_gym_battle:
            implemented.append(suffix)
        state = "BATTLE_AND_BADGE_SCRIPT" if has_gym_battle else "GYM_PENDING"
        print(f"GYM {suffix}: {state}")
    print(f"GYM BATTLES WITH BADGE SCRIPT: {len(implemented)}/{len(GYM_CITIES)}")

    wild = json.loads((ROOT / "src/data/wild_encounters.json").read_text(
        encoding="utf-8"))
    group = next((x for x in wild["wild_encounter_groups"]
                  if x["label"] == "gWildMonHeaders"), None)
    wild_by_map = {
        entry.get("map"): entry for entry in group["encounters"]
    } if group else {}
    outdoor = [name for name, info in maps.items()
               if info["map_type"] in ("MAP_TYPE_ROUTE", "MAP_TYPE_UNDERGROUND")]
    missing_land = [
        name for name in outdoor
        if not wild_by_map.get(maps[name]["id"], {}).get("land_mons")
    ]
    print(f"ROUTES/CAVES AUDITED FOR LAND ENCOUNTERS: {len(outdoor)}")
    print(f"WITH LAND ENCOUNTERS: {len(outdoor) - len(missing_land)}/{len(outdoor)}")
    print(f"WITHOUT LAND ENCOUNTERS: {len(missing_land)}")
    for name in missing_land:
        print(f"  ENCOUNTER TODO: {name}")
    print("NOTE: encounter headers do not confirm metatile-based wild battles.")
    print("STILL REQUIRED: Delta traversal, captures, saves, gym fights, League and ending.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
