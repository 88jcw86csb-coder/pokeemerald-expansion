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
    # Event text control codes must contain one backslash, not a doubled escape.
    for name in NAMES:
        dialogue = (ROOT / f"data/maps/{name}/scripts.inc").read_text(encoding="utf-8")
        for malformed in (r"\\p", r"\\n", r"\\l"):
            if malformed in dialogue:
                errors.append(f"{name}: doubled dialogue control escape {malformed}")

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
    gift_section = starter_script.split("EryonVilaAurora_EventScript_RioluToParty::", 1)[0]
    if "goto_if_eq VAR_RESULT, FALSE" in gift_section:
        errors.append("Vila Aurora: incorrect boolean check for givemon result")
    if not any(event.get("script") == "EryonVilaAurora_EventScript_VillageNotice" for event in maps["Eryon_VilaAurora"].get("bg_events", [])):
        errors.append("Vila Aurora: village notice not placed on map")
    for required in (
        "EryonVilaAurora_EventScript_VillageNotice::",
        "goto_if_ge VAR_ERYON_STARTER_RECEIVED, 1",
        "goto_if_ge VAR_ERYON_LUMINA_CLUE_FOUND, 1",
    ):
        if required not in starter_script:
            errors.append(f"Vila Aurora: village notice missing: {required}")
    if "giveitem ITEM_POKE_BALL, 5" not in starter_script:
        errors.append("Vila Aurora: five Poke Balls not granted after starter")
    if "setvar VAR_ERYON_CAPTURE_KIT_RECEIVED, 1" not in starter_script:
        errors.append("Vila Aurora: capture kit progress not persisted")
    if "goto_if_eq VAR_ERYON_CAPTURE_KIT_RECEIVED, 0" not in starter_script:
        errors.append("Vila Aurora: capture kit cannot be retried after full bag")
    if "goto_if_eq VAR_RESULT, FALSE, EryonVilaAurora_EventScript_CaptureKitFull" not in starter_script:
        errors.append("Vila Aurora: capture kit full-bag handling missing")
    clue_var = (ROOT / "include/constants/vars.h").read_text(encoding="utf-8")
    forest_script = (ROOT / "data/maps/Eryon_BosqueDeLumina/scripts.inc").read_text(encoding="utf-8")
    town_script = (ROOT / "data/maps/Eryon_Verdelume/scripts.inc").read_text(encoding="utf-8")
    if not re.search(r"(?m)^#define VAR_ERYON_LUMINA_CLUE_FOUND\s+0x40F8\b", clue_var):
        errors.append("Lumina clue persistent variable missing")
    if "setvar VAR_ERYON_LUMINA_CLUE_FOUND, 1" not in forest_script:
        errors.append("Lumina clue discovery is not persisted")
    stone_section = forest_script.split("EryonBosque_EventScript_AncientStone::", 1)
    if len(stone_section) != 2:
        errors.append("Lumina: ancient stone event missing")
    else:
        stone_intro = stone_section[1].split("EryonBosque_EventScript_StoneRecognized::", 1)[0]
        if "setvar VAR_ERYON_LUMINA_CLUE_FOUND, 1" not in stone_intro:
            errors.append("Lumina: examining the ancient stone must record the clue")
        if "EryonBosque_Text_StoneDiscovery" not in stone_intro:
            errors.append("Lumina: ancient stone discovery feedback missing")
    if "goto_if_ge VAR_ERYON_LUMINA_CLUE_FOUND, 1" not in forest_script:
        errors.append("Lumina researcher lacks repeat-visit dialogue")
    if "goto_if_ge VAR_ERYON_LUMINA_CLUE_FOUND, 1" not in town_script:
        errors.append("Verdelume does not react to the Lumina clue")
    if not re.search(r"(?m)^#define VAR_ERYON_KAEL_BRIEFED\s+0x40FA\b", clue_var):
        errors.append("Kael briefing persistent variable missing")
    if "setvar VAR_ERYON_KAEL_BRIEFED, 1" not in town_script:
        errors.append("Kael briefing is not saved")
    if "goto_if_ge VAR_ERYON_KAEL_BRIEFED, 1" not in town_script:
        errors.append("Kael lacks repeat-visit dialogue after briefing")
    route02_script = (ROOT / "data/maps/Eryon_Rota02/scripts.inc").read_text(encoding="utf-8")
    if not re.search(r"(?m)^#define VAR_ERYON_ROTA02_SUPPLY_FOUND\s+0x40FC\b", clue_var):
        errors.append("Route 02 supply cache persistent variable missing")
    for required in (
        "giveitem ITEM_ANTIDOTE",
        "setvar VAR_ERYON_ROTA02_SUPPLY_FOUND, 1",
        "goto_if_ge VAR_ERYON_ROTA02_SUPPLY_FOUND, 1",
        "goto_if_eq VAR_RESULT, FALSE, EryonRota02_EventScript_RoadsideCacheFull",
    ):
        if required not in route02_script:
            errors.append(f"Route 02 supply cache missing: {required}")
    if not any(obj.get("script") == "EryonRota02_EventScript_Cartographer" for obj in maps["Eryon_Rota02"].get("object_events", [])):
        errors.append("Route 02: cartographer NPC missing from map")
    for required in (
        "EryonRota02_EventScript_Cartographer::",
        "goto_if_ge VAR_ERYON_KAEL_BRIEFED, 1, EryonRota02_EventScript_CartographerAfterKael",
        "goto_if_ge VAR_ERYON_LUMINA_CLUE_FOUND, 1, EryonRota02_EventScript_CartographerAfterClue",
    ):
        if required not in route02_script:
            errors.append(f"Route 02: cartographer dialogue missing: {required}")
    route01_script = (ROOT / "data/maps/Eryon_Rota01/scripts.inc").read_text(encoding="utf-8")
    for required in (
        "goto_if_eq VAR_ERYON_STARTER_RECEIVED, 0",
        "goto_if_ge VAR_ERYON_LUMINA_CLUE_FOUND, 1",
        "goto_if_ge VAR_ERYON_KAEL_BRIEFED, 1",
    ):
        if required not in route01_script:
            errors.append(f"Route 01 explorer progress dialogue missing: {required}")
    if not any(obj.get("script") == "EryonVerdelume_EventScript_Botanist" for obj in maps["Eryon_Verdelume"].get("object_events", [])):
        errors.append("Verdelume: botanist NPC missing from map")
    for required in (
        "EryonVerdelume_EventScript_Botanist::",
        "goto_if_ge VAR_ERYON_KAEL_BRIEFED, 1, EryonVerdelume_EventScript_BotanistAfterKael",
        "goto_if_ge VAR_ERYON_LUMINA_CLUE_FOUND, 1, EryonVerdelume_EventScript_BotanistAfterClue",
    ):
        if required not in town_script:
            errors.append(f"Verdelume: botanist dialogue missing: {required}")
    if "EryonVerdelume_EventScript_Kael::" not in town_script:
        errors.append("Verdelume is missing Kael's first encounter")
    if "EryonVerdelume_EventScript_KaelClue::" not in town_script:
        errors.append("Kael does not react to the Eclipse clue")
    if not any(obj.get("script") == "EryonVerdelume_EventScript_Kael" for obj in maps["Eryon_Verdelume"]["object_events"]):
        errors.append("Kael's NPC is missing from Verdelume")
    # Detect placeholder Hoenn map binaries: these are not original Eryon layouts.
    inherited = {}
    opponent_constants = (ROOT / "include/constants/opponents.h").read_text(encoding="utf-8")
    trainer_parties = (ROOT / "src/data/trainers.party").read_text(encoding="utf-8")
    if not re.search(r"(?m)^#define TRAINER_ERYON_KAEL\\s+855\\b", opponent_constants):
        errors.append("Kael trainer ID is missing")
    if "=== TRAINER_ERYON_KAEL ===" not in trainer_parties:
        errors.append("Kael trainer party is missing")
    else:
        kael_party = trainer_parties.split("=== TRAINER_ERYON_KAEL ===", 1)[1].split("\\n=== ", 1)[0]
        if not re.search(r"(?m)^Roserade\s*\nLevel:\s*18\s*$", kael_party):
            errors.append("Kael must have level 18 Roserade")
    if "trainerbattle_single TRAINER_ERYON_KAEL" not in town_script:
        errors.append("Kael battle is not linked to his NPC")
    if "setvar VAR_ERYON_KAEL_DEFEATED, 1" not in town_script:
        errors.append("Kael victory is not persisted")
    for name, m in maps.items():
        layout = layouts.get(m["layout"])
        if layout:
            blockmap = layout["blockdata_filepath"]
            if not blockmap.startswith("data/layouts/Eryon_"):
                inherited[name] = blockmap
    if inherited:
        for name, blockmap in inherited.items():
            print(f"WARNING: {name} still uses inherited map tiles: {blockmap}")
        print("WARNING: Original Eryon terrain and collision must be implemented before gameplay sign-off")
    # Lumina currently borrows Petalburg Woods terrain. Its exits must use
    # actual exit tiles until a custom Eryon forest layout replaces it.
    woods = maps["Eryon_BosqueDeLumina"]
    expected_forest_exits = {(16, 38), (14, 5)}
    actual_forest_exits = {(warp["x"], warp["y"]) for warp in woods.get("warp_events", [])}
    if actual_forest_exits != expected_forest_exits:
        errors.append("Lumina: forest exits are not on the inherited woods' exit tiles")
    for map_name, width, height in (
        ("Eryon_Rota01", 20, 20),
        ("Eryon_Rota02", 50, 20),
        ("Eryon_Verdelume", 40, 60),
    ):
        for index, warp in enumerate(maps[map_name].get("warp_events", [])):
            if warp["x"] in (0, width - 1) or warp["y"] in (0, height - 1):
                print(f"WARNING: {map_name} warp {index} uses a border tile; collision and warp behavior not verified")
    print("WARNING: route-side warp positions still require terrain/collision verification")
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
