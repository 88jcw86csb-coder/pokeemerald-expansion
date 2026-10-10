#!/usr/bin/env python3
"""Static tests for Eryon's scripted opening; does not emulate the game."""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAPS = ("Eryon_VilaAurora", "Eryon_Rota01", "Eryon_BosqueDeLumina",
        "Eryon_Rota02", "Eryon_Verdelume", "Eryon_Rota03",
        "Eryon_SerraDosCristais", "Eryon_PassagemRochosa",
        "Eryon_EstradaOriental", "Eryon_ValeDosVentos",
        "Eryon_EstradaDosPomares", "Eryon_VilaDosPomares", "Eryon_Rota04", "Eryon_Neonara", "Eryon_ColinasDaNeblina", "Eryon_VilaDaNeblina", "Eryon_TrilhaGlacial", "Eryon_Frostheim", "Eryon_RefugioCristal", "Eryon_PostoOriental", "Eryon_Umbra", "Eryon_RotaDasCachoeiras", "Eryon_VilaDasAguas", "Eryon_TrilhaDoOasis", "Eryon_DesertoDeSolaris", "Eryon_Ignivar", "Eryon_FlorestaDosEcos")
LABEL = re.compile(r"(?m)^([A-Za-z][A-Za-z0-9_]*)::?\s*$")
JUMP = re.compile(r"^\s*(?:goto|goto_if_eq|goto_if_ne|goto_if_ge|goto_if_le|goto_if_gt|goto_if_lt)\s+(.+)$")


class EryonEventFlowTests(unittest.TestCase):
    def test_all_map_npc_and_sign_scripts_exist(self):
        import json
        for name in MAPS:
            with self.subTest(map=name):
                folder = ROOT / "data/maps" / name
                data = json.loads((folder / "map.json").read_text(encoding="utf-8"))
                script = (folder / "scripts.inc").read_text(encoding="utf-8")
                labels = set(LABEL.findall(script))
                for kind in ("object_events", "bg_events", "coord_events"):
                    for index, event in enumerate(data.get(kind, [])):
                        label = event.get("script")
                        if label and label.startswith("Eryon"):
                            self.assertIn(label, labels, f"{name} {kind}[{index}] has no script")

    def test_solaris_to_ignivar_story_and_emergency_medic(self):
        import json
        chain = ("Eryon_TrilhaDoOasis", "Eryon_DesertoDeSolaris",
                 "Eryon_Ignivar", "Eryon_FlorestaDosEcos")
        maps = {
            name: json.loads((ROOT / "data/maps" / name / "map.json").read_text(encoding="utf-8"))
            for name in chain
        }
        for left, right in zip(chain, chain[1:]):
            with self.subTest(from_map=left, to_map=right):
                exits = maps[left]["warp_events"]
                entries = maps[right]["warp_events"]
                self.assertTrue(any(
                    warp["dest_map"] == maps[right]["id"]
                    and entries[int(warp["dest_warp_id"])]["dest_map"] == maps[left]["id"]
                    for warp in exits
                ))
        city = maps["Eryon_Ignivar"]
        medic = "EryonIgnivar_EventScript_EmergencyMedic"
        self.assertEqual(sum(npc.get("script") == medic for npc in city["object_events"]), 1)
        script = (ROOT / "data/maps/Eryon_Ignivar/scripts.inc").read_text(encoding="utf-8")
        self.assertIn(medic + "::", script)
        self.assertIn("special HealPlayerParty", script)
        for name, clue in (
            ("Eryon_DesertoDeSolaris", "EryonSolaris_EventScript_BuriedDevice"),
            ("Eryon_Ignivar", "EryonIgnivar_EventScript_PowerGridNotice"),
            ("Eryon_FlorestaDosEcos", "EryonEcos_EventScript_ResonantStone"),
        ):
            with self.subTest(clue=name):
                events = maps[name]["bg_events"]
                self.assertTrue(any(event.get("script") == clue for event in events))

    def test_solaris_ignivar_ecos_additional_witnesses(self):
        import json
        cases = (
            ("Eryon_DesertoDeSolaris", "EryonSolaris_EventScript_CaravanScout"),
            ("Eryon_Ignivar", "EryonIgnivar_EventScript_GridInspector"),
            ("Eryon_FlorestaDosEcos", "EryonEcos_EventScript_ForestRanger"),
        )
        for map_name, label in cases:
            with self.subTest(map=map_name):
                folder = ROOT / "data/maps" / map_name
                data = json.loads((folder / "map.json").read_text(encoding="utf-8"))
                scripts = (folder / "scripts.inc").read_text(encoding="utf-8")
                self.assertEqual(sum(
                    event.get("script") == label for event in data["object_events"]
                ), 1)
                self.assertIn(label + "::", scripts)
                text_label = label.replace("_EventScript_", "_Text_")
                self.assertIn(text_label + ":", scripts)
                self.assertIn("msgbox " + text_label, scripts)

    def test_ignivar_medic_text_escapes_are_single(self):
        source = (ROOT / "data/maps/Eryon_Ignivar/scripts.inc").read_text(encoding="utf-8")
        self.assertIn('SOCORRISTA: A usina\\n', source)
        self.assertNotIn('SOCORRISTA: A usina\\\\n', source)

    def test_post_ignivar_story_npcs_and_clue_branch(self):
        import json
        cases = (
            ("Eryon_Ignivar", "EryonIgnivar_EventScript_EvacuationCoordinator"),
            ("Eryon_FlorestaDosEcos", "EryonEcos_EventScript_SignalSurveyor"),
        )
        for name, label in cases:
            with self.subTest(map=name):
                folder = ROOT / "data/maps" / name
                data = json.loads((folder / "map.json").read_text(encoding="utf-8"))
                script = (folder / "scripts.inc").read_text(encoding="utf-8")
                self.assertEqual(sum(e.get("script") == label for e in data["object_events"]), 1)
                self.assertIn(label + "::", script)
                self.assertIn(label + "Informed::", script)
                self.assertIn(
                    "goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1, " + label + "Informed",
                    script,
                )
                text_label = label.replace("_EventScript_", "_Text_")
                self.assertIn(text_label + "Before:", script)
                self.assertIn(text_label + ":", script)

    def test_ignivar_emergency_board_is_placed_and_reactive(self):
        import json
        root = ROOT / "data/maps/Eryon_Ignivar"
        data = json.loads((root / "map.json").read_text(encoding="utf-8"))
        scripts = (root / "scripts.inc").read_text(encoding="utf-8")
        label = "EryonIgnivar_EventScript_EmergencyBoard"
        self.assertEqual(sum(e.get("script") == label for e in data["bg_events"]), 1)
        self.assertIn(label + "::", scripts)
        self.assertIn("goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1, " + label + "Alert", scripts)
        self.assertIn("EryonIgnivar_Text_EmergencyBoardAlert:", scripts)
        self.assertIn("EryonIgnivar_Text_EmergencyBoardQuiet:", scripts)

    def test_passagem_healer_and_two_trainers(self):
        import json
        folder = ROOT / "data/maps/Eryon_PassagemRochosa"
        data = json.loads((folder / "map.json").read_text(encoding="utf-8"))
        script = (folder / "scripts.inc").read_text(encoding="utf-8")
        placements = [obj["script"] for obj in data["object_events"]]
        for label in ("EryonPassagem_EventScript_HikerBattle",
                      "EryonPassagem_EventScript_EclipseBattle",
                      "EryonPassagem_EventScript_Medic"):
            self.assertEqual(placements.count(label), 1)
        self.assertIn("trainerbattle_single TRAINER_ERYON_PASSAGEM_HIKER", script)
        self.assertIn("trainerbattle_single TRAINER_ERYON_PASSAGEM_ECLIPSE", script)
        self.assertIn("special HealPlayerParty", script)

    def test_eryon_maps_are_registered_with_matching_layouts(self):
        import json
        groups = json.loads((ROOT / "data/maps/map_groups.json").read_text(encoding="utf-8"))
        layouts = json.loads((ROOT / "data/layouts/layouts.json").read_text(encoding="utf-8"))
        layout_by_id = {item["id"]: item for item in layouts["layouts"]}
        self.assertEqual(set(groups["gMapGroup_Eryon"]), set(MAPS))
        for name in MAPS:
            with self.subTest(map=name):
                path = ROOT / "data/maps" / name / "map.json"
                data = json.loads(path.read_text(encoding="utf-8"))
                self.assertIn(data["layout"], layout_by_id)
                layout = layout_by_id[data["layout"]]
                block = ROOT / layout["blockdata_filepath"]
                self.assertTrue(block.is_file())
                self.assertEqual(block.stat().st_size, 2 * layout["width"] * layout["height"])

    def test_eryon_warps_are_reciprocal(self):
        import json
        maps = {
            name: json.loads((ROOT / "data/maps" / name / "map.json").read_text(encoding="utf-8"))
            for name in MAPS
        }
        by_id = {data["id"]: data for data in maps.values()}
        for name, data in maps.items():
            for index, warp in enumerate(data.get("warp_events", [])):
                with self.subTest(map=name, warp=index):
                    self.assertIn(warp["dest_map"], by_id)
                    destination = by_id[warp["dest_map"]]
                    dest_index = int(warp["dest_warp_id"])
                    self.assertLess(dest_index, len(destination.get("warp_events", [])))
                    back = destination["warp_events"][dest_index]
                    self.assertEqual(back["dest_map"], data["id"])
                    self.assertEqual(int(back["dest_warp_id"]), index)

    def test_eryon_border_connections_are_reciprocal(self):
        import json
        maps = {
            name: json.loads((ROOT / "data/maps" / name / "map.json").read_text(encoding="utf-8"))
            for name in MAPS
        }
        by_id = {data["id"]: data for data in maps.values()}
        opposite = {"up": "down", "down": "up", "left": "right", "right": "left"}
        for name, data in maps.items():
            for index, connection in enumerate(data.get("connections") or []):
                with self.subTest(map=name, connection=index):
                    self.assertIn(connection["direction"], opposite)
                    self.assertIn(connection["map"], by_id)
                    destination = by_id[connection["map"]]
                    matches = [
                        back for back in (destination.get("connections") or [])
                        if back.get("map") == data["id"]
                        and back.get("direction") == opposite[connection["direction"]]
                        and back.get("offset") == connection["offset"]
                    ]
                    self.assertEqual(len(matches), 1, "missing or ambiguous return connection")

    def test_validator_accepts_expanded_trainer_count(self):
        validator = (ROOT / "tools/eryon_validate.py").read_text(encoding="utf-8")
        opponents = (ROOT / "include/constants/opponents.h").read_text(encoding="utf-8")
        count = int(re.search(r"(?m)^#define TRAINERS_COUNT_EMERALD\s+(\d+)", opponents).group(1))
        self.assertGreaterEqual(count, 863)
        self.assertNotIn('TRAINERS_COUNT_EMERALD\\s+858', validator)

    def test_serra_camp_clue_and_supply_are_persistent(self):
        import json
        vars_text = (ROOT / "include/constants/vars.h").read_text(encoding="utf-8")
        scripts = (ROOT / "data/maps/Eryon_SerraDosCristais/scripts.inc").read_text(
            encoding="utf-8"
        )
        map_data = json.loads(
            (ROOT / "data/maps/Eryon_SerraDosCristais/map.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertIn("#define VAR_ERYON_SERRA_CLUE_FOUND", vars_text)
        self.assertIn("#define VAR_ERYON_SERRA_SUPPLY_FOUND", vars_text)
        self.assertIn("setvar VAR_ERYON_SERRA_CLUE_FOUND, 1", scripts)
        self.assertIn("giveitem ITEM_SUPER_POTION", scripts)
        self.assertIn("setvar VAR_ERYON_SERRA_SUPPLY_FOUND, 1", scripts)
        self.assertIn(
            "goto_if_eq VAR_RESULT, FALSE, EryonSerra_EventScript_SupplyCrateFull",
            scripts,
        )
        self.assertTrue(any(
            event.get("script") == "EryonSerra_EventScript_SupplyCrate"
            for event in map_data["bg_events"]
        ))

    def test_new_eryon_trainers_are_connected_to_maps(self):
        import json
        opponents = (ROOT / "include/constants/opponents.h").read_text(encoding="utf-8")
        parties = (ROOT / "src/data/trainers.party").read_text(encoding="utf-8")
        cases = (
            ("Eryon_Rota01", "TRAINER_ERYON_ROUTE01_YOUNGSTER",
             "EryonRota01_EventScript_Youngster"),
            ("Eryon_Rota03", "TRAINER_ERYON_ROUTE03_RANGER",
             "EryonRota03_EventScript_Ranger"),
            ("Eryon_SerraDosCristais", "TRAINER_ERYON_SERRA_ECLIPSE",
             "EryonSerra_EventScript_EclipseScout"),
            ("Eryon_PassagemRochosa", "TRAINER_ERYON_PASSAGEM_HIKER",
             "EryonPassagem_EventScript_HikerBattle"),
            ("Eryon_PassagemRochosa", "TRAINER_ERYON_PASSAGEM_ECLIPSE",
             "EryonPassagem_EventScript_EclipseBattle"),
        )
        for map_name, trainer, script_label in cases:
            with self.subTest(map=map_name):
                self.assertIn("#define " + trainer, opponents)
                self.assertIn("=== " + trainer + " ===", parties)
                path = ROOT / "data/maps" / map_name
                map_data = json.loads((path / "map.json").read_text(encoding="utf-8"))
                self.assertTrue(any(
                    npc.get("script") == script_label
                    for npc in map_data["object_events"]
                ))
                scripts = (path / "scripts.inc").read_text(encoding="utf-8")
                self.assertIn(script_label + "::", scripts)
                self.assertIn("trainerbattle_single " + trainer, scripts)

    def test_caravan_witness_is_placed_and_reacts_to_badge(self):
        import json
        town = json.loads(
            (ROOT / "data/maps/Eryon_Verdelume/map.json").read_text(encoding="utf-8")
        )
        script_name = "EryonVerdelume_EventScript_CaravanWitness"
        witnesses = [
            obj for obj in town["object_events"] if obj["script"] == script_name
        ]
        self.assertEqual(len(witnesses), 1)
        script = (ROOT / "data/maps/Eryon_Verdelume/scripts.inc").read_text(
            encoding="utf-8"
        )
        self.assertIn(script_name + "::", script)
        self.assertIn(
            "goto_if_ge VAR_ERYON_KAEL_DEFEATED, 1, "
            "EryonVerdelume_EventScript_CaravanWitnessAfterBadge",
            script,
        )
        self.assertIn("EryonVerdelume_Text_CaravanWitnessAfterBadge:", script)
        self.assertIn("EryonVerdelume_Text_CaravanWitnessBeforeBadge:", script)

    def test_new_game_starts_in_eryon_village(self):
        source = (ROOT / "src/new_game.c").read_text(encoding="utf-8")
        warp_function = source.split("static void WarpToTruck(void)", 1)[1].split(
            "void Sav2_ClearSetDefault(void)", 1
        )[0]
        self.assertIn(
            "SetWarpDestination(MAP_GROUP(MAP_ERYON_VILA_AURORA), "
            "MAP_NUM(MAP_ERYON_VILA_AURORA), WARP_ID_NONE, 10, 10)",
            warp_function,
        )
        import json
        village = json.loads(
            (ROOT / "data/maps/Eryon_VilaAurora/map.json").read_text(encoding="utf-8")
        )
        layouts = json.loads(
            (ROOT / "data/layouts/layouts.json").read_text(encoding="utf-8")
        )["layouts"]
        layout = next(entry for entry in layouts if entry["id"] == village["layout"])
        self.assertLess(10, layout["width"])
        self.assertLess(10, layout["height"])
        self.assertEqual(village["id"], "MAP_ERYON_VILA_AURORA")
        # Starting on an NPC or a warp can block or immediately move the player.
        occupied = [
            (event["x"], event["y"])
            for kind in ("object_events", "warp_events", "bg_events", "coord_events")
            for event in village.get(kind, [])
        ]
        self.assertNotIn((10, 10), occupied, "New-game spawn overlaps a map event")


    def test_jump_destinations_exist(self):
        for name in MAPS:
            script = (ROOT / "data/maps" / name / "scripts.inc").read_text()
            labels = set(LABEL.findall(script))
            for lineno, line in enumerate(script.splitlines(), 1):
                match = JUMP.match(line)
                if not match:
                    continue
                destination = match.group(1).split(",")[-1].strip().split()[0]
                with self.subTest(map=name, line=lineno, target=destination):
                    self.assertIn(destination, labels)

    def test_dialogue_has_no_doubled_control_escapes(self):
        for name in MAPS:
            script = (ROOT / "data/maps" / name / "scripts.inc").read_text()
            for escape in (r"\\n", r"\\p", r"\\l"):
                with self.subTest(map=name, escape=escape):
                    self.assertNotIn(escape, script)

    def test_eryon_trainer_battles_use_supported_macro(self):
        macro_source = (ROOT / "asm/macros/event.inc").read_text(encoding="utf-8")
        macro = re.search(
            r"(?m)^\s*\.macro trainerbattle_single\s+([^\n]+)",
            macro_source,
        )
        self.assertIsNotNone(macro, "trainerbattle_single macro missing")
        arguments = [part.strip() for part in macro.group(1).split(",")]
        self.assertEqual(
            [arg.split(":")[0].split("=")[0] for arg in arguments],
            ["trainer", "intro_text", "lose_text", "event_script", "music"],
        )
        for name in ("Eryon_Verdelume", "Eryon_BosqueDeLumina", "Eryon_Rota02"):
            script = (ROOT / "data/maps" / name / "scripts.inc").read_text(encoding="utf-8")
            for line in script.splitlines():
                if not line.strip().startswith("trainerbattle_single "):
                    continue
                args = [part.strip() for part in line.split("trainerbattle_single", 1)[1].split(",")]
                with self.subTest(map=name, trainer=args[0]):
                    self.assertEqual(len(args), 5)
                    self.assertIn(args[4], ("TRUE", "FALSE"))
                    self.assertIn(args[3] + "::", script)

    def test_scout_victory_does_not_grant_kael_badge(self):
        forest = (ROOT / "data/maps/Eryon_BosqueDeLumina/scripts.inc").read_text(encoding="utf-8")
        start = forest.index("EryonBosque_EventScript_EclipseScoutVictory::")
        end = forest.index("EryonBosque_EventScript_EclipseScoutAfterBadge::", start)
        victory = forest[start:end]
        self.assertNotIn("FLAG_BADGE01_GET", victory)
        self.assertNotIn("VAR_ERYON_KAEL_DEFEATED", victory)
        self.assertNotIn("giveitem", victory)
        self.assertIn("release", victory)
        city = (ROOT / "data/maps/Eryon_Verdelume/scripts.inc").read_text(encoding="utf-8")
        kael = city.split("EryonVerdelume_EventScript_KaelVictory::", 1)[1].split(
            "EryonVerdelume_EventScript_KaelAfterBattle::", 1
        )[0]
        self.assertIn("setflag FLAG_BADGE01_GET", kael)
        self.assertIn("setvar VAR_ERYON_KAEL_DEFEATED, 1", kael)

    def test_opening_maps_have_route_from_village_to_verdelume(self):
        import json
        maps = {
            name: json.loads((ROOT / "data/maps" / name / "map.json").read_text())
            for name in MAPS
        }
        by_id = {data["id"]: name for name, data in maps.items()}
        adjacency = {name: set() for name in MAPS}
        for name, data in maps.items():
            for connection in data.get("connections") or []:
                if connection["map"] in by_id:
                    adjacency[name].add(by_id[connection["map"]])
            for warp in data.get("warp_events", []):
                if warp["dest_map"] in by_id:
                    adjacency[name].add(by_id[warp["dest_map"]])
        seen = {"Eryon_VilaAurora"}
        queue = ["Eryon_VilaAurora"]
        while queue:
            current = queue.pop()
            for neighbor in adjacency[current] - seen:
                seen.add(neighbor)
                queue.append(neighbor)
        self.assertEqual(seen, set(MAPS))
        self.assertIn("Eryon_Verdelume", seen)

    def test_opening_warps_have_reciprocal_destinations(self):
        import json

        maps = {
            name: json.loads((ROOT / "data/maps" / name / "map.json").read_text(encoding="utf-8"))
            for name in MAPS
        }
        by_id = {data["id"]: data for data in maps.values()}
        for source in maps.values():
            for source_warp_id, warp in enumerate(source.get("warp_events", [])):
                destination = by_id.get(warp["dest_map"])
                if destination is None:
                    continue
                target_warps = destination.get("warp_events", [])
                target_id = int(warp["dest_warp_id"])
                with self.subTest(map=source["id"], warp=source_warp_id):
                    self.assertGreaterEqual(target_id, 0)
                    self.assertLess(target_id, len(target_warps))
                    if target_id < 0 or target_id >= len(target_warps):
                        continue
                    reverse = target_warps[target_id]
                    self.assertEqual(reverse["dest_map"], source["id"])
                    self.assertEqual(int(reverse["dest_warp_id"]), source_warp_id)

    def test_all_eryon_battle_trainers_have_unique_party_and_id(self):
        scripts = "\n".join(
            (ROOT / "data/maps" / name / "scripts.inc").read_text()
            for name in MAPS
        )
        referenced = set(re.findall(
            r"\btrainerbattle_single\s+(TRAINER_ERYON_[A-Z0-9_]+)",
            scripts,
        ))
        self.assertGreaterEqual(len(referenced), 3)
        opponents = (ROOT / "include/constants/opponents.h").read_text()
        ids = {
            name: int(value)
            for name, value in re.findall(
                r"(?m)^#define\s+(TRAINER_ERYON_[A-Z0-9_]+)\s+(\d+)\s*$",
                opponents,
            )
        }
        party = (ROOT / "src/data/trainers.party").read_text()
        for name in referenced:
            with self.subTest(trainer=name):
                self.assertIn(name, ids)
                self.assertEqual(party.count(f"=== {name} ==="), 1)
        self.assertEqual(len(ids), len(set(ids.values())))
        count = int(re.search(
            r"(?m)^#define TRAINERS_COUNT_EMERALD\s+(\d+)", opponents
        ).group(1))
        capacity = int(re.search(
            r"(?m)^#define MAX_TRAINERS_COUNT_EMERALD\s+(\d+)", opponents
        ).group(1))
        self.assertLessEqual(count, capacity)
        self.assertLess(max(ids.values()), count)

    def test_dario_validator_checks_match_trainer_definitions(self):
        validator = (ROOT / "tools/eryon_validate.py").read_text()
        self.assertIn('dario_label = "EryonRota02_EventScript_Dario"', validator)
        self.assertIn('TRAINER_ERYON_ROUTE02_HIKER', validator)
        self.assertIn('TRAINERS_COUNT_EMERALD', validator)
        self.assertNotIn(r'TRAINER_ERYON_ROUTE02_HIKER\\\\s+', validator)
        self.assertNotIn(r'TRAINERS_COUNT_EMERALD\\\\s+', validator)

    def test_route02_hiker_offers_repeatable_optional_healing(self):
        script = (ROOT / "data/maps/Eryon_Rota02/scripts.inc").read_text()
        hiker = script.split("EryonRota02_EventScript_Hiker::", 1)[1].split(
            "EryonRota02_Text_Hiker:", 1
        )[0]
        self.assertIn("MSGBOX_YESNO", hiker)
        self.assertIn("goto_if_eq VAR_RESULT, NO", hiker)
        self.assertIn("special HealPlayerParty", hiker)
        self.assertIn("EryonRota02_EventScript_HikerDecline::", hiker)
        self.assertNotIn("setvar VAR_ERYON_", hiker)
        self.assertNotIn("giveitem ", hiker)
        self.assertIn("def_special HealPlayerParty",
                      (ROOT / "data/specials.inc").read_text())

    def test_route02_dario_battle_is_optional_and_has_two_pokemon(self):
        import json
        map_data = json.loads((ROOT / "data/maps/Eryon_Rota02/map.json").read_text())
        self.assertEqual(
            sum(e["script"] == "EryonRota02_EventScript_Dario"
                for e in map_data["object_events"]), 1
        )
        script = (ROOT / "data/maps/Eryon_Rota02/scripts.inc").read_text()
        self.assertIn("trainerbattle_single TRAINER_ERYON_ROUTE02_HIKER", script)
        party = (ROOT / "src/data/trainers.party").read_text()
        team = party.split("=== TRAINER_ERYON_ROUTE02_HIKER ===", 1)[1]
        self.assertIn("Geodude\nLevel: 13", team)
        self.assertIn("Machop\nLevel: 14", team)
        self.assertNotIn("setflag FLAG_BADGE01_GET", script)
        opponents = (ROOT / "include/constants/opponents.h").read_text()
        self.assertRegex(opponents, r"TRAINER_ERYON_ROUTE02_HIKER\s+857")
        self.assertRegex(opponents, r"TRAINERS_COUNT_EMERALD\s+863")

    def test_kael_battle_is_reachable_after_briefing(self):
        script = (ROOT / "data/maps/Eryon_Verdelume/scripts.inc").read_text()
        self.assertIn("goto_if_ge VAR_ERYON_KAEL_BRIEFED, 1, EryonVerdelume_EventScript_KaelFollowup", script)
        followup = script.split("EryonVerdelume_EventScript_KaelFollowup::", 1)[1].split("EryonVerdelume_EventScript_KaelVictory::", 1)[0]
        self.assertIn("trainerbattle_single TRAINER_ERYON_KAEL", followup)
        self.assertIn("EryonVerdelume_EventScript_KaelVictory", followup)
        victory = script.split("EryonVerdelume_EventScript_KaelVictory::", 1)[1].split("EryonVerdelume_EventScript_KaelAfterBattle::", 1)[0]
        self.assertIn("setvar VAR_ERYON_KAEL_DEFEATED, 1", victory)
        self.assertIn("call Common_EventScript_PlayGymBadgeFanfare", victory)
        self.assertIn("setflag FLAG_BADGE01_GET", victory)

    def test_eryon_progress_vars_are_unique_and_defined(self):
        vars_text = (ROOT / "include/constants/vars.h").read_text()
        definitions = re.findall(r"(?m)^#define\s+(VAR_[A-Z0-9_]+)\s+(0x[0-9A-Fa-f]+)", vars_text)
        by_value = {}
        for name, value in definitions:
            if name.startswith("VAR_ERYON_"):
                with self.subTest(name=name):
                    self.assertNotIn(value, by_value, f"{name} shares {value} with {by_value.get(value)}")
                by_value[value] = name
        scripts = "\n".join((ROOT / "data/maps" / name / "scripts.inc").read_text() for name in MAPS)
        for name in set(re.findall(r"VAR_ERYON_[A-Z0-9_]+", scripts)):
            with self.subTest(name=name):
                self.assertIn(name, dict(definitions), f"Undefined Eryon variable: {name}")

    def test_village_route_boundary_connections(self):
        import json
        village = json.loads((ROOT / "data/maps/Eryon_VilaAurora/map.json").read_text())
        route = json.loads((ROOT / "data/maps/Eryon_Rota01/map.json").read_text())
        self.assertIn({"map": "MAP_ERYON_ROTA01", "offset": 0, "direction": "up"}, village["connections"])
        self.assertIn({"map": "MAP_ERYON_VILA_AURORA", "offset": 0, "direction": "down"}, route["connections"])

    def test_opening_border_has_no_redundant_warps(self):
        import json
        village = json.loads((ROOT / "data/maps/Eryon_VilaAurora/map.json").read_text())
        route = json.loads((ROOT / "data/maps/Eryon_Rota01/map.json").read_text())
        forest = json.loads((ROOT / "data/maps/Eryon_BosqueDeLumina/map.json").read_text())
        self.assertEqual(village["warp_events"], [])
        self.assertEqual(len(route["warp_events"]), 1)
        self.assertEqual(route["warp_events"][0]["dest_map"], "MAP_ERYON_BOSQUE_DE_LUMINA")
        self.assertEqual(int(route["warp_events"][0]["dest_warp_id"]), 0)
        self.assertEqual(forest["warp_events"][0]["dest_map"], "MAP_ERYON_ROTA01")
        self.assertEqual(int(forest["warp_events"][0]["dest_warp_id"]), 0)

    def test_opening_map_connections_are_reciprocal(self):
        import json
        maps = {
            name: json.loads((ROOT / "data/maps" / name / "map.json").read_text())
            for name in MAPS
        }
        by_id = {data["id"]: data for data in maps.values()}
        opposites = {"up": "down", "down": "up", "left": "right", "right": "left"}
        for name, data in maps.items():
            for connection in data.get("connections") or []:
                with self.subTest(map=name, target=connection["map"]):
                    self.assertIn(connection["map"], by_id)
                    if connection["map"] not in by_id:
                        continue
                    self.assertIn(connection["direction"], opposites)
                    reverse = [
                        other for other in by_id[connection["map"]].get("connections") or []
                        if other["map"] == data["id"]
                        and other["direction"] == opposites.get(connection["direction"])
                        and int(other["offset"]) == -int(connection["offset"])
                    ]
                    self.assertEqual(len(reverse), 1, "Expected exactly one reciprocal connection")

    def test_opening_maps_form_one_connected_region(self):
        import json
        maps = {
            name: json.loads((ROOT / "data/maps" / name / "map.json").read_text(encoding="utf-8"))
            for name in MAPS
        }
        by_id = {data["id"]: name for name, data in maps.items()}
        graph = {name: set() for name in maps}
        for name, data in maps.items():
            destinations = [
                connection["map"] for connection in (data.get("connections") or [])
            ] + [
                warp["dest_map"] for warp in (data.get("warp_events") or [])
            ]
            for destination in destinations:
                with self.subTest(source=name, destination=destination):
                    self.assertIn(destination, by_id)
                if destination in by_id:
                    graph[name].add(by_id[destination])
        visited = set()
        pending = ["Eryon_VilaAurora"]
        while pending:
            name = pending.pop()
            if name in visited:
                continue
            visited.add(name)
            pending.extend(graph[name] - visited)
        self.assertEqual(visited, set(MAPS), "An opening map is unreachable from Vila Aurora")

    def test_opening_events_do_not_share_tile_coordinates(self):
        import json
        for name in MAPS:
            data = json.loads((ROOT / "data/maps" / name / "map.json").read_text(encoding="utf-8"))
            used = {}
            for kind, events in (
                ("NPC", data.get("object_events") or []),
                ("warp", data.get("warp_events") or []),
                ("background", data.get("bg_events") or []),
            ):
                for index, event in enumerate(events):
                    position = (int(event["x"]), int(event["y"]))
                    with self.subTest(map=name, kind=kind, index=index):
                        self.assertNotIn(position, used, f"Event overlaps {used.get(position)}")
                    used[position] = f"{kind} {index}"

    def test_opening_warps_are_inside_layout_bounds(self):
        import json
        maps = {
            name: json.loads((ROOT / "data/maps" / name / "map.json").read_text())
            for name in MAPS
        }
        layouts = {
            layout["id"]: layout
            for layout in json.loads((ROOT / "data/layouts/layouts.json").read_text())["layouts"]
        }
        for name, data in maps.items():
            with self.subTest(map=name, field="layout"):
                self.assertIn(data["layout"], layouts)
            if data["layout"] not in layouts:
                continue
            layout = layouts[data["layout"]]
            for index, warp in enumerate(data.get("warp_events") or []):
                with self.subTest(map=name, warp=index):
                    self.assertGreaterEqual(int(warp["x"]), 0)
                    self.assertLess(int(warp["x"]), int(layout["width"]))
                    self.assertGreaterEqual(int(warp["y"]), 0)
                    self.assertLess(int(warp["y"]), int(layout["height"]))

    def test_opening_warps_are_reciprocal(self):
        import json
        maps = {
            name: json.loads((ROOT / "data/maps" / name / "map.json").read_text())
            for name in MAPS
        }
        by_constant = {data["id"]: name for name, data in maps.items()}
        for name, data in maps.items():
            for warp_id, warp in enumerate(data.get("warp_events", [])):
                with self.subTest(map=name, warp=warp_id):
                    target_name = by_constant.get(warp["dest_map"])
                    self.assertIsNotNone(target_name, "Warp leaves opening map set")
                    if target_name is None:
                        continue
                    target_warps = maps[target_name].get("warp_events", [])
                    destination_id = int(warp["dest_warp_id"])
                    self.assertLess(destination_id, len(target_warps))
                    if destination_id >= len(target_warps):
                        continue
                    return_warp = target_warps[destination_id]
                    self.assertEqual(return_warp["dest_map"], data["id"])
                    self.assertEqual(int(return_warp["dest_warp_id"]), warp_id)

    def test_kael_badge_only_after_victory(self):
        script = (ROOT / "data/maps/Eryon_Verdelume/scripts.inc").read_text()
        entry = script.split("EryonVerdelume_EventScript_Kael::", 1)[1].split("EryonVerdelume_EventScript_KaelClue::", 1)[0]
        victory = script.split("EryonVerdelume_EventScript_KaelVictory::", 1)[1].split("EryonVerdelume_EventScript_KaelAfterBattle::", 1)[0]
        self.assertIn("goto_if_ge VAR_ERYON_KAEL_DEFEATED, 1, EryonVerdelume_EventScript_KaelAfterBattle", entry)
        self.assertIn("setvar VAR_ERYON_KAEL_DEFEATED, 1", victory)
        self.assertEqual(script.count("setflag FLAG_BADGE01_GET"), 1)
        self.assertIn("setflag FLAG_BADGE01_GET", victory)
        self.assertIn("call Common_EventScript_PlayGymBadgeFanfare", victory)

    def test_guide_reacts_to_first_badge(self):
        script = (ROOT / "data/maps/Eryon_Verdelume/scripts.inc").read_text(encoding="utf-8")
        entry = script.split("EryonVerdelume_EventScript_Guide::", 1)[1].split(
            "EryonVerdelume_EventScript_GuideBadge::", 1
        )[0]
        self.assertIn(
            "goto_if_ge VAR_ERYON_KAEL_DEFEATED, 1, EryonVerdelume_EventScript_GuideBadge",
            entry,
        )
        self.assertLess(entry.index("VAR_ERYON_KAEL_DEFEATED"), entry.index("VAR_ERYON_LUMINA_CLUE_FOUND"))
        self.assertIn("EryonVerdelume_Text_GuideBadge:", script)

    def test_professor_heals_without_skipping_starter_or_capture_kit(self):
        script = (ROOT / "data/maps/Eryon_VilaAurora/scripts.inc").read_text(encoding="utf-8")
        starter = script.split("EryonVilaAurora_EventScript_ProfessorElya::", 1)[1].split(
            "EryonVilaAurora_EventScript_RioluToParty::", 1
        )[0]
        self.assertIn("givemon SPECIES_RIOLU, 5", starter)
        after_starter = script.split("EryonVilaAurora_EventScript_ElyaAfterStarter::", 1)[1].split(
            "EryonVilaAurora_EventScript_ElyaAfterBadge::", 1
        )[0]
        self.assertLess(
            after_starter.index("VAR_ERYON_CAPTURE_KIT_RECEIVED"),
            after_starter.index("EryonVilaAurora_EventScript_ElyaHealOffer"),
        )
        offer = script.split("EryonVilaAurora_EventScript_ElyaHealOffer::", 1)[1].split(
            "EryonVilaAurora_EventScript_ElyaHealDeclined::", 1
        )[0]
        self.assertIn("MSGBOX_YESNO", offer)
        self.assertIn("goto_if_eq VAR_RESULT, NO", offer)
        self.assertIn("special HealPlayerParty", offer)
        self.assertNotIn("setvar VAR_ERYON_", offer)
        self.assertNotIn("giveitem", offer)
        self.assertIn("def_special HealPlayerParty", (ROOT / "data/specials.inc").read_text())

    def test_verdelume_medic_offers_repeatable_optional_healing(self):
        import json
        data = json.loads((ROOT / "data/maps/Eryon_Verdelume/map.json").read_text(encoding="utf-8"))
        medics = [
            obj for obj in data["object_events"]
            if obj["script"] == "EryonVerdelume_EventScript_FieldMedic"
        ]
        self.assertEqual(len(medics), 1)
        script = (ROOT / "data/maps/Eryon_Verdelume/scripts.inc").read_text(encoding="utf-8")
        entry = script.split("EryonVerdelume_EventScript_FieldMedic::", 1)[1].split(
            "EryonVerdelume_EventScript_FieldMedicDecline::", 1
        )[0]
        self.assertIn("MSGBOX_YESNO", entry)
        self.assertIn("goto_if_eq VAR_RESULT, NO, EryonVerdelume_EventScript_FieldMedicDecline", entry)
        self.assertIn("special HealPlayerParty", entry)
        self.assertNotIn("setvar VAR_ERYON_", entry)
        self.assertNotIn("giveitem", entry)
        self.assertIn("EryonVerdelume_Text_FieldMedicHealed:", script)
        specials = (ROOT / "data/specials.inc").read_text(encoding="utf-8")
        self.assertIn("def_special HealPlayerParty", specials)

    def test_trainer_slot_capacity_covers_eryon_scout(self):
        opponents = (ROOT / "include/constants/opponents.h").read_text(encoding="utf-8")
        def constant(name):
            match = re.search(r"(?m)^#define\s+" + re.escape(name) + r"\s+(\d+)\b", opponents)
            self.assertIsNotNone(match, name)
            return int(match.group(1))
        self.assertEqual(constant("TRAINER_ERYON_SCOUT"), constant("TRAINER_ERYON_KAEL") + 1)
        self.assertGreater(constant("TRAINERS_COUNT_EMERALD"), constant("TRAINER_ERYON_SCOUT"))
        self.assertLessEqual(constant("TRAINERS_COUNT_EMERALD"), constant("MAX_TRAINERS_COUNT_EMERALD"))

    def test_scout_battle_remains_available_after_kael(self):
        script = (ROOT / "data/maps/Eryon_BosqueDeLumina/scripts.inc").read_text(encoding="utf-8")
        entry = script.split("EryonBosque_EventScript_EclipseScout::", 1)[1].split(
            "EryonBosque_EventScript_EclipseScoutAfterClue::", 1
        )[0]
        self.assertIn(
            "goto_if_ge VAR_ERYON_KAEL_DEFEATED, 1, EryonBosque_EventScript_EclipseScoutAfterBadge",
            entry,
        )
        after_badge = script.split("EryonBosque_EventScript_EclipseScoutAfterBadge::", 1)[1].split(
            "EryonBosque_Text_EclipseScoutBeforeClue:", 1
        )[0]
        self.assertIn("trainerbattle_single TRAINER_ERYON_SCOUT", after_badge)
        self.assertIn("EryonBosque_EventScript_EclipseScoutVictory, FALSE", after_badge)

    def test_eclipse_scout_has_optional_two_pokemon_battle(self):
        script = (ROOT / "data/maps/Eryon_BosqueDeLumina/scripts.inc").read_text(encoding="utf-8")
        entry = script.split("EryonBosque_EventScript_EclipseScoutAfterClue::", 1)[1].split(
            "EryonBosque_EventScript_EclipseScoutVictory::", 1
        )[0]
        self.assertIn("trainerbattle_single TRAINER_ERYON_SCOUT", entry)
        self.assertIn("EryonBosque_EventScript_EclipseScoutVictory, FALSE", entry)
        self.assertIn("EryonBosque_Text_EclipseScoutChallenge:", script)
        self.assertIn("EryonBosque_Text_EclipseScoutDefeat:", script)
        opponents = (ROOT / "include/constants/opponents.h").read_text(encoding="utf-8")
        self.assertRegex(opponents, r"(?m)^#define\s+TRAINER_ERYON_SCOUT\s+856\b")
        parties = (ROOT / "src/data/trainers.party").read_text(encoding="utf-8")
        team = parties.split("=== TRAINER_ERYON_SCOUT ===", 1)[1].split("\n=== ", 1)[0]
        self.assertRegex(team, r"(?m)^Poochyena\nLevel: 12$")
        self.assertRegex(team, r"(?m)^Zubat\nLevel: 13$")

    def test_eclipse_scout_has_three_nonblocking_story_stages(self):
        import json
        map_data = json.loads((ROOT / "data/maps/Eryon_BosqueDeLumina/map.json").read_text(encoding="utf-8"))
        scouts = [
            event for event in map_data["object_events"]
            if event["script"] == "EryonBosque_EventScript_EclipseScout"
        ]
        self.assertEqual(len(scouts), 1)
        script = (ROOT / "data/maps/Eryon_BosqueDeLumina/scripts.inc").read_text(encoding="utf-8")
        entry = script.split("EryonBosque_EventScript_EclipseScout::", 1)[1].split(
            "EryonBosque_EventScript_EclipseScoutAfterClue::", 1
        )[0]
        self.assertIn("goto_if_ge VAR_ERYON_KAEL_DEFEATED, 1, EryonBosque_EventScript_EclipseScoutAfterBadge", entry)
        self.assertIn("goto_if_ge VAR_ERYON_LUMINA_CLUE_FOUND, 1, EryonBosque_EventScript_EclipseScoutAfterClue", entry)
        self.assertLess(entry.index("VAR_ERYON_KAEL_DEFEATED"), entry.index("VAR_ERYON_LUMINA_CLUE_FOUND"))
        for label in (
            "EryonBosque_EventScript_EclipseScoutAfterClue::",
            "EryonBosque_EventScript_EclipseScoutAfterBadge::",
        ):
            self.assertIn(label, script)
        for label in (
            "EryonBosque_Text_EclipseScoutBeforeClue:",
            "EryonBosque_Text_EclipseScoutAfterClue:",
            "EryonBosque_Text_EclipseScoutAfterBadge:",
        ):
            self.assertIn(label, script)

    def test_forest_researcher_unlocks_new_clue_after_badge(self):
        script = (ROOT / "data/maps/Eryon_BosqueDeLumina/scripts.inc").read_text(encoding="utf-8")
        entry = script.split("EryonBosque_EventScript_Researcher::", 1)[1].split(
            "EryonBosque_EventScript_ResearcherKnownClue::", 1
        )[0]
        self.assertIn(
            "goto_if_ge VAR_ERYON_LUMINA_CLUE_FOUND, 1, EryonBosque_EventScript_ResearcherKnownClue",
            entry,
        )
        self.assertIn("setvar VAR_ERYON_LUMINA_CLUE_FOUND, 1", entry)
        self.assertLess(entry.index("VAR_ERYON_LUMINA_CLUE_FOUND"), entry.index("setvar VAR_ERYON_LUMINA_CLUE_FOUND"))
        known = script.split("EryonBosque_EventScript_ResearcherKnownClue::", 1)[1].split(
            "EryonBosque_EventScript_ResearcherAfterBadge::", 1
        )[0]
        self.assertIn(
            "goto_if_ge VAR_ERYON_KAEL_DEFEATED, 1, EryonBosque_EventScript_ResearcherAfterBadge",
            known,
        )
        self.assertIn("goto EryonBosque_EventScript_ResearcherFollowup", known)
        self.assertIn("msgbox EryonBosque_Text_ResearcherAfterBadge", script)

    def test_professor_homecoming_preserves_capture_kit_priority(self):
        script = (ROOT / "data/maps/Eryon_VilaAurora/scripts.inc").read_text(encoding="utf-8")
        section = script.split("EryonVilaAurora_EventScript_ElyaAfterStarter::", 1)[1].split(
            "EryonVilaAurora_EventScript_ElyaAfterBadge::", 1
        )[0]
        self.assertIn(
            "goto_if_eq VAR_ERYON_CAPTURE_KIT_RECEIVED, 0, EryonVilaAurora_EventScript_CaptureKit",
            section,
        )
        self.assertIn(
            "goto_if_ge VAR_ERYON_KAEL_DEFEATED, 1, EryonVilaAurora_EventScript_ElyaAfterBadge",
            section,
        )
        self.assertLess(section.index("VAR_ERYON_CAPTURE_KIT_RECEIVED"), section.index("VAR_ERYON_KAEL_DEFEATED"))
        self.assertIn("msgbox EryonVilaAurora_Text_ElyaAfterBadge", script)
        self.assertIn("EryonVilaAurora_Text_ElyaAfterBadge:", script)

    def test_route01_explorer_reacts_to_first_badge(self):
        script = (ROOT / "data/maps/Eryon_Rota01/scripts.inc").read_text(encoding="utf-8")
        entry = script.split("EryonRota01_EventScript_Explorer::", 1)[1].split(
            "EryonRota01_EventScript_ExplorerAfterBadge::", 1
        )[0]
        self.assertIn(
            "goto_if_ge VAR_ERYON_KAEL_DEFEATED, 1, EryonRota01_EventScript_ExplorerAfterBadge",
            entry,
        )
        self.assertLess(entry.index("VAR_ERYON_KAEL_DEFEATED"), entry.index("VAR_ERYON_STARTER_RECEIVED"))
        self.assertIn("EryonRota01_Text_ExplorerAfterBadge:", script)
        self.assertIn("msgbox EryonRota01_Text_ExplorerAfterBadge", script)

    def test_cartographer_reacts_to_first_badge(self):
        script = (ROOT / "data/maps/Eryon_Rota02/scripts.inc").read_text(encoding="utf-8")
        entry = script.split("EryonRota02_EventScript_Cartographer::", 1)[1].split(
            "EryonRota02_EventScript_CartographerAfterBadge::", 1
        )[0]
        self.assertIn(
            "goto_if_ge VAR_ERYON_KAEL_DEFEATED, 1, EryonRota02_EventScript_CartographerAfterBadge",
            entry,
        )
        self.assertLess(entry.index("VAR_ERYON_KAEL_DEFEATED"), entry.index("VAR_ERYON_KAEL_BRIEFED"))
        self.assertIn("EryonRota02_Text_CartographerAfterBadge:", script)
        self.assertIn("msgbox EryonRota02_Text_CartographerAfterBadge", script)

    def test_local_kid_reacts_to_first_badge(self):
        script = (ROOT / "data/maps/Eryon_Verdelume/scripts.inc").read_text(encoding="utf-8")
        entry = script.split("EryonVerdelume_EventScript_LocalKid::", 1)[1].split(
            "EryonVerdelume_EventScript_LocalKidBadge::", 1
        )[0]
        self.assertIn(
            "goto_if_ge VAR_ERYON_KAEL_DEFEATED, 1, EryonVerdelume_EventScript_LocalKidBadge",
            entry,
        )
        self.assertIn("msgbox EryonVerdelume_Text_LocalKid, MSGBOX_DEFAULT", entry)
        badge = script.split("EryonVerdelume_EventScript_LocalKidBadge::", 1)[1].split(
            "EryonVerdelume_Text_LocalKidBadge:", 1
        )[0]
        self.assertIn("msgbox EryonVerdelume_Text_LocalKidBadge", badge)

    def test_botanist_reacts_to_first_badge(self):
        script = (ROOT / "data/maps/Eryon_Verdelume/scripts.inc").read_text(encoding="utf-8")
        entry = script.split("EryonVerdelume_EventScript_Botanist::", 1)[1].split("EryonVerdelume_EventScript_BotanistAfterBadge::", 1)[0]
        self.assertIn(
            "goto_if_ge VAR_ERYON_KAEL_DEFEATED, 1, EryonVerdelume_EventScript_BotanistAfterBadge",
            entry,
        )
        self.assertLess(
            entry.index("VAR_ERYON_KAEL_DEFEATED"),
            entry.index("VAR_ERYON_KAEL_BRIEFED"),
        )
        badge_dialogue = script.split("EryonVerdelume_EventScript_BotanistAfterBadge::", 1)[1].split(
            "EryonVerdelume_EventScript_BotanistAfterClue::", 1
        )[0]
        self.assertIn("msgbox EryonVerdelume_Text_BotanistAfterBadge", badge_dialogue)
        self.assertIn("EryonVerdelume_Text_BotanistAfterBadge:", script)

    def test_approved_gym_level_curve(self):
        design = (ROOT / "docs/ERYON_DESIGN.md").read_text(encoding="utf-8")
        expected = [
            ("Kael", "Roserade", 18),
            ("Lyra", "Jolteon", 26),
            ("Bjorn", "Weavile", 33),
            ("Tessa", "Armaldo", 39),
            ("Nox", "Drapion", 45),
            ("Ragna", "Infernape", 51),
            ("Seraphine", "Gardevoir", 57),
            ("Draven", "Garchomp", 64),
        ]
        section = design.split("## Ginásios e balanceamento aprovado", 1)[1].split("\n## ", 1)[0]
        rows = re.findall(r"(?m)^\|\s*([1-8])\s*\|\s*([^|]+)\|[^\n]*?\|\s*([^|]+)\|\s*(\d+)\s*\|\s*$", section)
        actual = [(name.strip(), ace.strip(), int(level)) for _, name, ace, level in rows]
        self.assertEqual(actual, expected)
        self.assertEqual([int(number) for number, *_ in rows], list(range(1, 9)))

    def test_story_does_not_define_fake_legendary_species(self):
        design = (ROOT / "docs/ERYON_DESIGN.md").read_text(encoding="utf-8")
        checklist = (ROOT / "docs/ERYON_IMPLEMENTATION_CHECKLIST.md").read_text(encoding="utf-8")
        self.assertIn("não criar espécies de Pokémon", design)
        self.assertIn("não espécies ou formas de Pokémon", design)
        self.assertIn("não são espécies de Pokémon", checklist)
        self.assertIn("lendários oficiais até Kalos", checklist)

    def test_eryon_dialogues_have_no_double_escaped_controls(self):
        # GBA text control codes must use a single backslash in .string lines.
        # A doubled backslash can show literal escapes or break text assembly.
        for name in MAPS:
            script = (ROOT / "data/maps" / name / "scripts.inc").read_text(encoding="utf-8")
            for line_number, line in enumerate(script.splitlines(), start=1):
                if not line.lstrip().startswith(".string "):
                    continue
                with self.subTest(map=name, line=line_number):
                    for control in ("n", "p", "l"):
                        self.assertNotIn(
                            chr(92) * 2 + control,
                            line,
                            f"Double-escaped GBA text control in {name}:{line_number}",
                        )

    def test_ancient_stone_changes_after_first_badge(self):
        forest = (ROOT / "data/maps/Eryon_BosqueDeLumina/scripts.inc").read_text(encoding="utf-8")
        stone = forest.split("EryonBosque_EventScript_StoneRecognized::", 1)[1].split(
            "EryonBosque_EventScript_StoneAfterBadge::", 1
        )[0]
        self.assertIn(
            "goto_if_ge VAR_ERYON_KAEL_DEFEATED, 1, EryonBosque_EventScript_StoneAfterBadge",
            stone,
        )
        after_badge = forest.split("EryonBosque_EventScript_StoneAfterBadge::", 1)[1].split(
            "EryonBosque_Text_StoneUnknown:", 1
        )[0]
        self.assertIn("msgbox EryonBosque_Text_StoneAfterBadge", after_badge)
        self.assertIn("release", after_badge)
        self.assertIn("EryonBosque_Text_StoneAfterBadge:", forest)

    def test_forest_traveler_reacts_to_first_badge(self):
        forest = (ROOT / "data/maps/Eryon_BosqueDeLumina/scripts.inc").read_text(encoding="utf-8")
        entry = forest.split("EryonBosque_EventScript_TravelerAfterClue::", 1)[1].split(
            "EryonBosque_EventScript_TravelerAfterBadge::", 1
        )[0]
        self.assertIn(
            "goto_if_ge VAR_ERYON_KAEL_DEFEATED, 1, EryonBosque_EventScript_TravelerAfterBadge",
            entry,
        )
        after = forest.split("EryonBosque_EventScript_TravelerAfterBadge::", 1)[1].split(
            "EryonBosque_Text_TravelerBeforeClue:", 1
        )[0]
        self.assertIn("msgbox EryonBosque_Text_TravelerAfterBadge", after)
        self.assertIn("release", after)
        self.assertIn("EryonBosque_Text_TravelerAfterBadge:", forest)

    def test_dialogue_references_resolve_to_local_labels(self):
        for name in MAPS:
            script = (ROOT / "data/maps" / name / "scripts.inc").read_text(encoding="utf-8")
            labels = set(LABEL.findall(script))
            for line_number, line in enumerate(script.splitlines(), 1):
                instruction = line.strip().split(" ", 1)[0]
                if instruction not in ("msgbox", "message", "trainerbattle_single"):
                    continue
                for reference in re.findall(r"\bEryon[A-Za-z0-9_]*_Text_[A-Za-z0-9_]+\b", line):
                    with self.subTest(map=name, line=line_number, label=reference):
                        self.assertIn(reference, labels)

    def test_dialogue_blocks_end_with_text_terminator(self):
        # Every contiguous sequence of .string fragments needs a final terminator.
        for name in MAPS:
            script = (ROOT / "data/maps" / name / "scripts.inc").read_text(encoding="utf-8")
            fragments = []
            start_line = None
            for line_number, line in enumerate(script.splitlines() + [""], start=1):
                match = re.match(r'^\s*\.string\s+"(.*)"\s*$', line)
                if match:
                    if not fragments:
                        start_line = line_number
                    fragments.append(match.group(1))
                elif fragments:
                    with self.subTest(map=name, line=start_line):
                        self.assertTrue(
                            fragments[-1].endswith("$"),
                            f"{name}:{start_line}: dialogue block missing final terminator",
                        )
                    fragments = []
                    start_line = None

    def test_no_duplicate_text_symbols(self):
        for name in MAPS:
            script = (ROOT / "data/maps" / name / "scripts.inc").read_text()
            symbols = re.findall(r"(?m)^([A-Za-z][A-Za-z0-9_]*):(?!=|:)", script)
            duplicates = sorted({symbol for symbol in symbols if symbols.count(symbol) > 1})
            with self.subTest(map=name):
                self.assertEqual(duplicates, [], f"Duplicate script symbols: {duplicates}")

    def test_no_duplicate_labels(self):
        for name in MAPS:
            script = (ROOT / "data/maps" / name / "scripts.inc").read_text()
            labels = LABEL.findall(script)
            with self.subTest(map=name):
                self.assertEqual(len(labels), len(set(labels)))


if __name__ == "__main__":
    unittest.main()
