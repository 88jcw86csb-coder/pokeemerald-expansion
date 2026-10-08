#!/usr/bin/env python3
"""Static tests for Eryon's scripted opening; does not emulate the game."""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAPS = ("Eryon_VilaAurora", "Eryon_Rota01", "Eryon_BosqueDeLumina",
        "Eryon_Rota02", "Eryon_Verdelume")
LABEL = re.compile(r"(?m)^([A-Za-z][A-Za-z0-9_]*)::?\s*$")
JUMP = re.compile(r"^\s*(?:goto|goto_if_eq|goto_if_ne|goto_if_ge|goto_if_le|goto_if_gt|goto_if_lt)\s+(.+)$")


class EryonEventFlowTests(unittest.TestCase):
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

    def test_forest_researcher_unlocks_new_clue_after_badge(self):
        script = (ROOT / "data/maps/Eryon_BosqueDeLumina/scripts.inc").read_text(encoding="utf-8")
        entry = script.split("EryonBosque_EventScript_Researcher::", 1)[1].split(
            "EryonBosque_EventScript_ResearcherAfterBadge::", 1
        )[0]
        self.assertIn(
            "goto_if_ge VAR_ERYON_KAEL_DEFEATED, 1, EryonBosque_EventScript_ResearcherAfterBadge",
            entry,
        )
        self.assertLess(entry.index("VAR_ERYON_KAEL_DEFEATED"), entry.index("VAR_ERYON_LUMINA_CLUE_FOUND"))
        self.assertIn("msgbox EryonBosque_Text_ResearcherAfterBadge", script)
        self.assertIn("EryonBosque_Text_ResearcherAfterBadge:", script)

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
