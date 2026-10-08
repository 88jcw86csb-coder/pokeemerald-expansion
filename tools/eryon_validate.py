#!/usr/bin/env python3
"""Static consistency checks for Eryon's opening maps (not an emulator test)."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NAMES = ["Eryon_VilaAurora", "Eryon_Rota01", "Eryon_BosqueDeLumina", "Eryon_Rota02", "Eryon_Verdelume"]


def load(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def main():
    errors = []
    groups = load("data/maps/map_groups.json")
    layouts = {entry["id"]: entry for entry in load("data/layouts/layouts.json")["layouts"]}
    scripts = (ROOT / "data/event_scripts.s").read_text(encoding="utf-8")
    maps = {name: load(f"data/maps/{name}/map.json") for name in NAMES}
    ids = {m["id"]: name for name, m in maps.items()}
    if set(groups.get("gMapGroup_Eryon", [])) != set(NAMES):
        errors.append("Eryon map group does not match opening map files")
    wild = load("src/data/wild_encounters.json")
    wild_group = next((group for group in wild["wild_encounter_groups"] if group["label"] == "gWildMonHeaders"), None)
    wild_by_map = {entry.get("map"): entry for entry in wild_group["encounters"]} if wild_group else {}
    species_constants = (ROOT / "include/constants/species.h").read_text(encoding="utf-8")
    if not re.search(r"(?m)^\s*SPECIES_RIOLU\s*=", species_constants):
        errors.append("Riolu starter species is not defined in the species enum")
    for route in ("Eryon_Rota01", "Eryon_BosqueDeLumina", "Eryon_Rota02"):
        map_id = maps[route]["id"]
        encounter = wild_by_map.get(map_id)
        if not encounter or "land_mons" not in encounter:
            errors.append(f"{route}: no land wild encounters")
            continue
        mons = encounter["land_mons"]["mons"]
        if len(mons) != 12:
            errors.append(f"{route}: expected 12 land encounter slots, found {len(mons)}")
        for mon in mons:
            if not re.search(r"(?m)^\s*" + re.escape(mon["species"]) + r"\s*=", species_constants):
                errors.append(f"{route}: unknown species constant {mon['species']}")
            if mon["min_level"] > mon["max_level"]:
                errors.append(f"{route}: invalid encounter level range for {mon['species']}")
    # Enforce the project's Gen I-VI-only roster in opening encounters.
    species_numbers = {
        name: int(number)
        for name, number in re.findall(
            r"(?m)^\s*(SPECIES_[A-Z0-9_]+)\s*=\s*(\d+)\s*,?",
            species_constants,
        )
    }
    for route in ("Eryon_Rota01", "Eryon_BosqueDeLumina", "Eryon_Rota02"):
        encounter = wild_by_map.get(maps[route]["id"], {})
        for mon in encounter.get("land_mons", {}).get("mons", []):
            number = species_numbers.get(mon["species"])
            if number is None:
                errors.append(f"{route}: cannot resolve National Dex number for {mon['species']}")
            elif not 1 <= number <= 721:
                errors.append(f"{route}: species outside National Dex 001-721: {mon['species']}")
    starter_ui = (ROOT / "src/starter_choose.c").read_text(encoding="utf-8")
    if not re.search(r"#define STARTER_MON_COUNT\s+1\b", starter_ui):
        errors.append("Starter selector must expose exactly one Pokemon")
    if not re.search(r"tStarterSelection\s*=\s*0\s*;", starter_ui):
        errors.append("Starter selector must initialize cursor to slot zero")
    for match in re.finditer(r"sPokeballCoords\[(\d+)\]", starter_ui):
        if int(match.group(1)) >= 1:
            errors.append(f"Starter selector references invalid ball slot {match.group(1)}")
    starter_script = (ROOT / "data/maps/Eryon_VilaAurora/scripts.inc").read_text(encoding="utf-8")
    for required in ("givemon SPECIES_RIOLU, 5", "MON_GIVEN_TO_PARTY", "MON_GIVEN_TO_PC", "VAR_ERYON_STARTER_RECEIVED"):
        if required not in starter_script:
            errors.append(f"Vila Aurora: missing starter gift requirement: {required}")
    if "goto_if_eq VAR_RESULT, FALSE" in starter_script:
        errors.append("Vila Aurora: incorrect boolean check for givemon result")
    clue_var = (ROOT / "include/constants/vars.h").read_text(encoding="utf-8")
    forest_script = (ROOT / "data/maps/Eryon_BosqueDeLumina/scripts.inc").read_text(encoding="utf-8")
    town_script = (ROOT / "data/maps/Eryon_Verdelume/scripts.inc").read_text(encoding="utf-8")
    if not re.search(r"(?m)^#define VAR_ERYON_LUMINA_CLUE_FOUND\s+0x40F8\b", clue_var):
        errors.append("Lumina clue persistent variable missing")
    if "setvar VAR_ERYON_LUMINA_CLUE_FOUND, 1" not in forest_script:
        errors.append("Lumina clue discovery is not persisted")
    if "goto_if_ge VAR_ERYON_LUMINA_CLUE_FOUND, 1" not in forest_script:
        errors.append("Lumina researcher lacks repeat-visit dialogue")
    if "goto_if_ge VAR_ERYON_LUMINA_CLUE_FOUND, 1" not in town_script:
        errors.append("Verdelume does not react to the Lumina clue")
    if "EryonVerdelume_EventScript_Kael::" not in town_script:
        errors.append("Verdelume is missing Kael's first encounter")
    if "EryonVerdelume_EventScript_KaelClue::" not in town_script:
        errors.append("Kael does not react to the Eclipse clue")
    if not any(obj.get("script") == "EryonVerdelume_EventScript_Kael" for obj in maps["Eryon_Verdelume"]["object_events"]):
        errors.append("Kael's NPC is missing from Verdelume")
    for name, m in maps.items():
        layout = layouts.get(m["layout"])
        if layout is None:
            errors.append(f"{name}: missing layout {m['layout']}")
            continue
        width, height = layout["width"], layout["height"]
        block_path = ROOT / layout["blockdata_filepath"]
        if not block_path.exists():
            errors.append(f"{name}: missing layout binary {block_path}")
        elif block_path.stat().st_size != width * height * 2:
            errors.append(f"{name}: layout binary has {block_path.stat().st_size} bytes; expected {width * height * 2}")

        opposites = {"up": "down", "down": "up", "left": "right", "right": "left"}
        for connection in m.get("connections") or []:
            direction = connection.get("direction")
            target_name = ids.get(connection.get("map"))
            if direction not in opposites or target_name is None:
                errors.append(f"{name}: invalid map connection {connection}")
                continue
            reverse_links = [
                link for link in (maps[target_name].get("connections") or [])
                if link.get("map") == m["id"] and link.get("direction") == opposites[direction]
            ]
            if not reverse_links:
                errors.append(f"{name}: missing reverse connection in {target_name}")
            elif not any(int(link.get("offset", 0)) == -int(connection.get("offset", 0)) for link in reverse_links):
                errors.append(f"{name}: inconsistent connection offset with {target_name}")
            target_layout = layouts.get(maps[target_name]["layout"])
            if target_layout:
                target_width, target_height = target_layout["width"], target_layout["height"]
                overlap = min(width, target_width) if direction in ("up", "down") else min(height, target_height)
                if overlap <= 0 or abs(int(connection.get("offset", 0))) >= max(width, height, target_width, target_height):
                    errors.append(f"{name}: impossible connection offset to {target_name}")
        for index, warp in enumerate(m.get("warp_events", [])):
            if not (0 <= warp["x"] < width and 0 <= warp["y"] < height):
                errors.append(f"{name}: warp {index} outside {width}x{height}")
            target = maps.get(ids.get(warp["dest_map"], ""))
            if target is None:
                errors.append(f"{name}: warp {index} unknown destination {warp['dest_map']}")
            elif not (0 <= int(warp["dest_warp_id"]) < len(target.get("warp_events", []))):
                errors.append(f"{name}: warp {index} invalid destination index")
            else:
                reverse = target["warp_events"][int(warp["dest_warp_id"])]
                if reverse["dest_map"] != m["id"] or int(reverse["dest_warp_id"]) != index:
                    errors.append(f"{name}: warp {index} has no reciprocal return warp")
        # Multiple events on one tile can make interactions ambiguous.
        occupied = {}
        for kind, events in (
            ("warp", m.get("warp_events", [])),
            ("NPC", m.get("object_events", [])),
            ("background", m.get("bg_events", [])),
        ):
            for index, event in enumerate(events):
                pos = (event["x"], event["y"])
                if pos in occupied:
                    errors.append(
                        f"{name}: {kind} event {index} overlaps {occupied[pos]} at {pos}"
                    )
                else:
                    occupied[pos] = f"{kind} event {index}"
        # Validate all map scripts once, even on maps with no NPCs.
        script_file = ROOT / "data/maps" / name / "scripts.inc"
        script_text = script_file.read_text(encoding="utf-8") if script_file.exists() else ""
        if f"data/maps/{name}/scripts.inc" not in scripts:
            errors.append(f"{name}: map scripts not included by data/event_scripts.s")
        if "\\\\p" in script_text or "\\\\n" in script_text:
            errors.append(f"{name}: doubled dialogue escapes")
        for index, bg in enumerate(m.get("bg_events", [])):
            if not (0 <= bg["x"] < width and 0 <= bg["y"] < height):
                errors.append(f"{name}: background event {index} outside {width}x{height}")
            if bg.get("type") == "sign":
                label = bg.get("script", "")
                if not re.search(r"(?m)^" + re.escape(label) + r"::", script_text):
                    errors.append(f"{name}: missing background event script {label}")
            elif bg.get("type") == "hidden_item":
                if not bg.get("item") or not bg.get("flag"):
                    errors.append(f"{name}: incomplete hidden item {index}")
        for index, obj in enumerate(m.get("object_events", [])):
            if not (0 <= obj["x"] < width and 0 <= obj["y"] < height):
                errors.append(f"{name}: NPC {index} outside {width}x{height}")
            if obj.get("script") != "0x0":
                label = obj.get("script", "")
                if not re.search(r"(?m)^" + re.escape(label) + r"::", script_text):
                    errors.append(f"{name}: missing NPC script {label}")
    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1
    print(f"PASS: {len(maps)} Eryon opening maps; IDs, NPC scripts, warp indices and encounter slots consistent")
    print("NOTE: collision, tiles, encounters, gameplay and compilation remain untested")
    return 0


if __name__ == "__main__":
    sys.exit(main())
