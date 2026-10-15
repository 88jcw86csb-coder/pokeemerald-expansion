#!/usr/bin/env python3
"""Validate planned League and Victory Road layouts and their exits."""
import unittest
from eryon_league_maps import ROOT, route, league, connected, render


class LeagueMapTests(unittest.TestCase):
    def test_league_approach_and_hub(self):
        for name, fn, start, exit in (
            ("caminho_da_liga", route, (0,22), (47,22)),
            ("liga_eryon", league, (0,36), (48,36)),
        ):
            with self.subTest(name=name):
                t=fn()
                reached=connected(t,start)
                floor={(x,y) for y,row in enumerate(t) for x,c in enumerate(row) if c!="#"}
                self.assertGreater(len(reached), 300)
                self.assertIn(exit,reached)
                path=ROOT/"docs/eryon"/f"{name}_terrain_plan.txt"
                self.assertEqual(path.read_text(encoding="utf-8"),render(name,t))


    def test_winding_high_ridge_and_southern_loop(self):
        """North rim and lower detour genuinely connect without removing original warps."""
        from collections import deque
        from build_eryon_map_bins import compile_plan
        import struct, json

        t=route()
        free={(x,y) for y,row in enumerate(t) for x,c in enumerate(row) if c!="#"}
        self.assertEqual(connected(t,(0,22)),free)
        self.assertIn((47,22),free)
        def limited(start,condition):
            visited={start}
            queue=deque([start])
            while queue:
                x,y=queue.popleft()
                for nx,ny in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
                    pos=(nx,ny)
                    if pos in free and condition(nx,ny) and pos not in visited:
                        visited.add(pos);queue.append(pos)
            return visited
        self.assertIn((38,8),limited((10,8),lambda x,y:y<=17))
        self.assertIn((23,8),limited((10,8),lambda x,y:y<=17))
        self.assertIn((40,23),limited((25,36),lambda x,y:x>=24))
        info=json.loads((ROOT/"data/maps/Eryon_CaminhoDaLiga/map.json").read_text())
        self.assertEqual([(e["x"],e["y"]) for e in info["bg_events"]
                          if e["script"]=="EryonLigaCaminho_EventScript_StarMemorial"],[(23,8)])
        script=(ROOT/"data/maps/Eryon_CaminhoDaLiga/scripts.inc").read_text()
        self.assertIn("EryonLigaCaminho_EventScript_StarMemorial::",script)
        plan=ROOT/"docs/eryon/caminho_da_liga_terrain_plan.txt"
        self.assertEqual(plan.read_text(),render("caminho_da_liga",t))
        expected=compile_plan(plan, {"#":0x3c01,".":0x3001,":":0x3003,
                                     "P":0x3001,"C":0x3001,"M":0x3001,"L":0x3001,"H":0x3001})
        data=(ROOT/"data/layouts/Eryon_CaminhoDaLiga/map.bin").read_bytes()
        self.assertEqual(data,expected)
        for x,y in ((0,22),(47,22),(23,8),(10,8),(38,8),(30,26)):
            self.assertEqual(struct.unpack_from("<H",data,2*(y*48+x))[0]&0x0c00,0)


    def test_eastern_summit_switchback_reaches_both_rims(self):
        terrain = route()
        for y in range(8, 13):
            self.assertEqual(terrain[y][32], ":")
        for x in range(32, 40):
            self.assertEqual(terrain[12][x], ":")
        reached = connected(terrain, (0, 22))
        for point in ((32, 7), (32, 12), (38, 13), (47, 22)):
            self.assertIn(point, reached)
        self.assertEqual(
            (ROOT / "docs/eryon/caminho_da_liga_terrain_plan.txt").read_text(),
            render("caminho_da_liga", terrain),
        )

    def test_northern_shortcut_links_memorial_and_eastern_ridge(self):
        from collections import deque
        terrain = route()
        for x in range(25, 33):
            self.assertEqual(terrain[11][x], ":")
        for y in range(11, 15):
            self.assertEqual(terrain[y][26], ":")
        free = {(x, y) for y, row in enumerate(terrain)
                for x, tile in enumerate(row) if tile != "#"}
        start, goal = (25, 14), (32, 11)
        pending = deque([start])
        visited = {start}
        while pending:
            x, y = pending.popleft()
            for pos in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                if pos not in free or pos in visited:
                    continue
                visited.add(pos)
                pending.append(pos)
        self.assertIn(goal, visited)
        self.assertIn((47, 22), connected(terrain, (0, 22)))
        self.assertEqual(
            (ROOT / "docs/eryon/caminho_da_liga_terrain_plan.txt").read_text(),
            render("caminho_da_liga", terrain),
        )

    def test_north_shortcut_story_landmark_is_accessible(self):
        import json
        terrain = route()
        data = json.loads((ROOT / "data/maps/Eryon_CaminhoDaLiga/map.json").read_text())
        events = [e for e in data["bg_events"] if
                  e["script"] == "EryonLigaCaminho_EventScript_NorthShortcut"]
        self.assertEqual(len(events), 1)
        self.assertEqual((events[0]["x"], events[0]["y"]), (29, 11))
        self.assertEqual(terrain[11][29], ":")
        self.assertIn((29, 11), connected(terrain, (0, 22)))
        script = (ROOT / "data/maps/Eryon_CaminhoDaLiga/scripts.inc").read_text()
        self.assertEqual(script.count("EryonLigaCaminho_EventScript_NorthShortcut::"), 1)
        entry = script.split("EryonLigaCaminho_EventScript_NorthShortcut::", 1)[1].split(
            "EryonLigaCaminho_EventScript_NorthShortcutChart::", 1)[0]
        for flag in ("FLAG_ERYON_CHAMPION_CROWNED",
                     "FLAG_ERYON_ECLIPSE_EVIDENCE_REPORTED",
                     "FLAG_ERYON_STAR_CHART_READ"):
            self.assertIn(flag, entry)
        self.assertNotIn("setflag ", entry)
        self.assertIn((47, 22), connected(terrain, (0, 22)))

    def test_northern_marker_prioritizes_champion_and_qualifier(self):
        script = (ROOT / "data/maps/Eryon_CaminhoDaLiga/scripts.inc").read_text()
        entry = script.split("EryonLigaCaminho_EventScript_NorthShortcut::", 1)[1].split(
            "EryonLigaCaminho_EventScript_NorthShortcutChart::", 1)[0]
        conditions = ("FLAG_ERYON_CHAMPION_CROWNED", "FLAG_ERYON_QUALIFIED",
                      "FLAG_ERYON_ECLIPSE_EVIDENCE_REPORTED", "FLAG_ERYON_STAR_CHART_READ")
        self.assertEqual([entry.index(flag) for flag in conditions],
                         sorted(entry.index(flag) for flag in conditions))
        self.assertIn("EryonLigaCaminho_EventScript_NorthShortcutQualified::", script)
        self.assertIn("EryonLigaCaminho_Text_NorthShortcutQualified:", script)
        self.assertNotIn("setflag ", entry)

    def test_northern_ridge_fletchling_battle_is_optional_and_accessible(self):
        import json
        terrain = route()
        map_data = json.loads((ROOT / "data/maps/Eryon_CaminhoDaLiga/map.json").read_text())
        signs = [e for e in map_data["bg_events"] if
                 e["script"] == "EryonLigaCaminho_EventScript_RidgeFletchling"]
        self.assertEqual(len(signs), 1)
        self.assertEqual((signs[0]["x"], signs[0]["y"]), (27, 11))
        self.assertEqual(terrain[11][27], ":")
        reached = connected(terrain, (0, 22))
        self.assertIn((27, 11), reached)
        self.assertIn((47, 22), reached)
        script = (ROOT / "data/maps/Eryon_CaminhoDaLiga/scripts.inc").read_text()
        body = script.split("EryonLigaCaminho_EventScript_RidgeFletchling::", 1)[1].split(
            "EryonLigaCaminho_EventScript_RidgeFletchlingDone::", 1)[0]
        self.assertIn("MSGBOX_YESNO", body)
        self.assertIn("setwildbattle SPECIES_FLETCHLING, 56", body)
        self.assertIn("dowildbattle", body)
        self.assertIn("specialvar VAR_RESULT, GetBattleOutcome", body)
        for outcome in ("B_OUTCOME_CAUGHT", "B_OUTCOME_WON",
                        "B_OUTCOME_RAN", "B_OUTCOME_PLAYER_TELEPORTED"):
            self.assertIn(outcome, body)
        self.assertNotIn("setflag ", body)
        species = (ROOT / "include/constants/species.h").read_text()
        self.assertIn("SPECIES_FLETCHLING", species)

    def test_birdwatch_clearing_is_generated_and_accessible(self):
        import json
        terrain = route()
        for y in range(8, 11):
            for x in range(27, 30):
                self.assertEqual(terrain[y][x], ".")
        self.assertIn((28, 9), connected(terrain, (0, 22)))
        self.assertIn((47, 22), connected(terrain, (0, 22)))
        map_file = ROOT / "data/maps/Eryon_CaminhoDaLiga/map.json"
        info = json.loads(map_file.read_text())
        signs = [e for e in info["bg_events"] if
                 e["script"] == "EryonLigaCaminho_EventScript_BirdwatchClearing"]
        self.assertEqual([(e["x"], e["y"]) for e in signs], [(28, 9)])
        scripts = (ROOT / "data/maps/Eryon_CaminhoDaLiga/scripts.inc").read_text()
        self.assertEqual(scripts.count("EryonLigaCaminho_EventScript_BirdwatchClearing::"), 1)
        self.assertEqual(
            (ROOT / "docs/eryon/caminho_da_liga_terrain_plan.txt").read_text(),
            render("caminho_da_liga", terrain),
        )

    def test_optional_birdwatcher_trainer_is_registered_and_reachable(self):
        import json
        terrain = route()
        data = json.loads((ROOT / "data/maps/Eryon_CaminhoDaLiga/map.json").read_text())
        people = [e for e in data["object_events"] if
                  e["script"] == "EryonLigaCaminho_EventScript_RidgeBirdwatcher"]
        self.assertEqual(len(people), 1)
        self.assertEqual((people[0]["x"], people[0]["y"]), (28, 8))
        reached = connected(terrain, (0, 22))
        self.assertIn((28, 8), reached)
        self.assertIn((27, 8), reached)
        self.assertIn((47, 22), reached)
        script = (ROOT / "data/maps/Eryon_CaminhoDaLiga/scripts.inc").read_text()
        entry = script.split("EryonLigaCaminho_EventScript_RidgeBirdwatcher::", 1)[1].split(
            "EryonLigaCaminho_EventScript_RidgeBirdwatcherDecline::", 1)[0]
        self.assertIn("MSGBOX_YESNO", entry)
        self.assertIn("trainerbattle_single TRAINER_ERYON_RIDGE_BIRDWATCHER", entry)
        self.assertIn("FLAG_ERYON_RIDGE_BIRDWATCHER_DEFEATED", entry)
        opponents = (ROOT / "include/constants/opponents.h").read_text()
        flags = (ROOT / "include/constants/flags.h").read_text()
        engine = (ROOT / "src/battle_setup.c").read_text()
        party = (ROOT / "src/data/trainers.party").read_text()
        self.assertIn("#define TRAINER_ERYON_RIDGE_BIRDWATCHER 889", opponents)
        self.assertIn("#define TRAINERS_COUNT_EMERALD     890", opponents)
        self.assertIn("#define FLAG_ERYON_RIDGE_BIRDWATCHER_DEFEATED", flags)
        self.assertIn("return FLAG_ERYON_RIDGE_BIRDWATCHER_DEFEATED;", engine)
        self.assertIn("=== TRAINER_ERYON_RIDGE_BIRDWATCHER ===", party)

    def test_summit_alcove_event_walkability_and_unique_script(self):
        import json
        t = route()
        data = json.loads((ROOT / "data/maps/Eryon_CaminhoDaLiga/map.json").read_text())
        signs = [e for e in data["bg_events"]
                 if e["script"] == "EryonLigaCaminho_EventScript_SummitAlcove"]
        self.assertEqual(len(signs), 1)
        pos = (signs[0]["x"], signs[0]["y"])
        self.assertEqual(pos, (38, 13))
        self.assertNotEqual(t[pos[1]][pos[0]], "#")
        occupied = {(e["x"], e["y"]) for e in data["object_events"]}
        walkable = {(x, y) for y, row in enumerate(t)
                    for x, cell in enumerate(row) if cell != "#"}
        seen = connected(t, (0, 22))
        self.assertIn((47, 22), seen)
        self.assertTrue(any(p in seen and p not in occupied
                            for p in ((37, 13), (39, 13), (38, 12), (38, 14))))
        self.assertIn((32, 8), seen)
        scripts = (ROOT / "data/maps/Eryon_CaminhoDaLiga/scripts.inc").read_text()
        self.assertEqual(scripts.count("EryonLigaCaminho_EventScript_SummitAlcove::"), 1)
        self.assertNotIn("setflag ", scripts.split(
            "EryonLigaCaminho_EventScript_SummitAlcove::", 1)[1].split(
            "EryonLigaCaminho_EventScript_SummitAlcoveFiled::", 1)[0])

    def test_western_ravine_loop_is_a_second_access_to_south_peak(self):
        terrain = route()
        for y in range(25, 32):
            self.assertEqual(terrain[y][20], ":")
        for x in range(20, 26):
            self.assertEqual(terrain[31][x], ":")
        reached = connected(terrain, (0, 22))
        for point in ((20, 25), (20, 31), (25, 31), (25, 36), (47, 22)):
            self.assertIn(point, reached)
        self.assertEqual(
            (ROOT / "docs/eryon/caminho_da_liga_terrain_plan.txt").read_text(),
            render("caminho_da_liga", terrain),
        )

    def test_western_ravine_inscription_on_distinct_accessible_branch(self):
        import json
        terrain = route()
        data = json.loads((ROOT / "data/maps/Eryon_CaminhoDaLiga/map.json").read_text())
        events = [e for e in data["bg_events"] if
                  e["script"] == "EryonLigaCaminho_EventScript_WestRavine"]
        self.assertEqual([(e["x"], e["y"]) for e in events], [(20, 29)])
        self.assertEqual(terrain[29][20], ":")
        connected_tiles = connected(terrain, (0, 22))
        self.assertIn((20, 29), connected_tiles)
        self.assertIn((25, 36), connected_tiles)
        self.assertIn((47, 22), connected_tiles)
        script = (ROOT / "data/maps/Eryon_CaminhoDaLiga/scripts.inc").read_text()
        entry = script.split("EryonLigaCaminho_EventScript_WestRavine::", 1)[1].split(
            "EryonLigaCaminho_EventScript_WestRavineChart::", 1)[0]
        for flag in ("FLAG_ERYON_CHAMPION_CROWNED",
                     "FLAG_ERYON_ECLIPSE_EVIDENCE_REPORTED",
                     "FLAG_ERYON_STAR_CHART_READ"):
            self.assertIn(flag, entry)
        self.assertNotIn("setflag ", entry)
        self.assertNotIn("trainerbattle_", entry)

    def test_western_ravine_healing_shelter_is_optional_and_accessible(self):
        import json
        t = route()
        data = json.loads((ROOT / "data/maps/Eryon_CaminhoDaLiga/map.json").read_text())
        signs = [event for event in data["bg_events"]
                 if event["script"] == "EryonLigaCaminho_EventScript_RavineRest"]
        self.assertEqual([(event["x"], event["y"]) for event in signs], [(20, 30)])
        self.assertEqual(t[30][20], ":")
        self.assertIn((20, 30), connected(t, (0, 22)))
        self.assertIn((47, 22), connected(t, (0, 22)))
        source = (ROOT / "data/maps/Eryon_CaminhoDaLiga/scripts.inc").read_text()
        body = source.split("EryonLigaCaminho_EventScript_RavineRest::", 1)[1].split(
            "EryonLigaCaminho_EventScript_RavineRestDecline::", 1)[0]
        self.assertIn("MSGBOX_YESNO", body)
        self.assertIn("special HealPlayerParty", body)
        self.assertIn("goto_if_eq VAR_RESULT, NO", body)
        self.assertNotIn("setflag ", body)
        self.assertNotIn("trainerbattle_", body)

    def test_original_west_ravine_side_pocket_is_walkable(self):
        terrain = route()
        reachable = connected(terrain, (0, 22))
        for y in range(27, 30):
            for x in range(16, 20):
                self.assertEqual(terrain[y][x], ".")
                self.assertIn((x, y), reachable)
        self.assertIn((20, 28), reachable)
        self.assertIn((47, 22), reachable)
        self.assertEqual(
            (ROOT / "docs/eryon/caminho_da_liga_terrain_plan.txt").read_text(),
            render("caminho_da_liga", terrain),
        )

    def test_rock_refuge_relic_is_walkable_and_does_not_gate_league(self):
        import json
        terrain = route()
        data = json.loads((ROOT / "data/maps/Eryon_CaminhoDaLiga/map.json").read_text())
        signs = [event for event in data["bg_events"]
                 if event["script"] == "EryonLigaCaminho_EventScript_RockRefuge"]
        self.assertEqual([(event["x"], event["y"]) for event in signs], [(17, 28)])
        self.assertEqual(terrain[28][17], ".")
        reached = connected(terrain, (0, 22))
        self.assertIn((17, 28), reached)
        self.assertIn((47, 22), reached)
        scripts = (ROOT / "data/maps/Eryon_CaminhoDaLiga/scripts.inc").read_text()
        entry = scripts.split("EryonLigaCaminho_EventScript_RockRefuge::", 1)[1].split(
            "EryonLigaCaminho_EventScript_RockRefugeChart::", 1)[0]
        for flag in ("FLAG_ERYON_CHAMPION_CROWNED",
                     "FLAG_ERYON_ECLIPSE_EVIDENCE_REPORTED",
                     "FLAG_ERYON_STAR_CHART_READ"):
            self.assertIn(flag, entry)
        self.assertNotIn("setflag ", entry)
        self.assertNotIn("trainerbattle_", entry)

    def test_original_northwest_city_promenade_and_story_event(self):
        import json
        terrain = league()
        connected_tiles = connected(terrain, (0, 36))
        for point in ((15, 19), (24, 25), (25, 27), (32, 32), (35, 34), (48, 36)):
            self.assertIn(point, connected_tiles)
        self.assertEqual(terrain[25][24], ".")
        self.assertEqual(
            (ROOT / "docs/eryon/liga_eryon_terrain_plan.txt").read_text(),
            render("liga_eryon", terrain),
        )
        data = json.loads((ROOT / "data/maps/Eryon_CidadeDaLiga/map.json").read_text())
        events = [e for e in data["bg_events"] if
                  e["script"] == "EryonCidadeLiga_EventScript_HillsidePromenade"]
        self.assertEqual([(e["x"], e["y"]) for e in events], [(24, 25)])
        scripts = (ROOT / "data/maps/Eryon_CidadeDaLiga/scripts.inc").read_text()
        entry = scripts.split("EryonCidadeLiga_EventScript_HillsidePromenade::", 1)[1].split(
            "EryonCidadeLiga_EventScript_HillsideEvidence::", 1)[0]
        self.assertIn("FLAG_ERYON_CHAMPION_CROWNED", entry)
        self.assertIn("FLAG_ERYON_ECLIPSE_EVIDENCE_REPORTED", entry)
        self.assertNotIn("setflag ", entry)

    def test_southwest_amphitheatre_route_and_narrative(self):
        import json
        terrain = league()
        reached = connected(terrain, (0, 36))
        for point in ((35, 43), (32, 45), (28, 47), (26, 48), (22, 53), (48, 36)):
            self.assertIn(point, reached)
        self.assertEqual(terrain[48][26], ".")
        self.assertEqual(
            (ROOT / "docs/eryon/liga_eryon_terrain_plan.txt").read_text(),
            render("liga_eryon", terrain),
        )
        data = json.loads((ROOT / "data/maps/Eryon_CidadeDaLiga/map.json").read_text())
        places = [e for e in data["bg_events"] if
                  e["script"] == "EryonCidadeLiga_EventScript_Amphitheatre"]
        self.assertEqual([(e["x"], e["y"]) for e in places], [(26, 48)])
        script = (ROOT / "data/maps/Eryon_CidadeDaLiga/scripts.inc").read_text()
        entry = script.split("EryonCidadeLiga_EventScript_Amphitheatre::", 1)[1].split(
            "EryonCidadeLiga_EventScript_AmphitheatreEvidence::", 1)[0]
        for flag in ("FLAG_ERYON_CHAMPION_CROWNED", "FLAG_ERYON_QUALIFIED",
                     "FLAG_ERYON_ECLIPSE_EVIDENCE_REPORTED"):
            self.assertIn(flag, entry)
        self.assertNotIn("setflag ", entry)

    def test_amphitheatre_medic_is_optional_and_accessible(self):
        import json
        terrain = league()
        data = json.loads((ROOT / "data/maps/Eryon_CidadeDaLiga/map.json").read_text())
        medics = [e for e in data["object_events"] if
                  e["script"] == "EryonCidadeLiga_EventScript_AmphitheatreMedic"]
        self.assertEqual([(e["x"], e["y"]) for e in medics], [(27, 48)])
        self.assertIn((27, 48), connected(terrain, (0, 36)))
        self.assertIn((48, 36), connected(terrain, (0, 36)))
        script = (ROOT / "data/maps/Eryon_CidadeDaLiga/scripts.inc").read_text()
        body = script.split("EryonCidadeLiga_EventScript_AmphitheatreMedic::", 1)[1].split(
            "EryonCidadeLiga_EventScript_AmphitheatreMedicDecline::", 1)[0]
        self.assertIn("MSGBOX_YESNO", body)
        self.assertIn("special HealPlayerParty", body)
        self.assertIn("goto_if_eq VAR_RESULT, NO", body)
        self.assertNotIn("setflag ", body)
        self.assertNotIn("trainerbattle_", body)

    def test_eight_stars_terrace_connected_city(self):
        """Check the new skyline park, unchanged League building, and exact terrain."""
        import json,struct
        from build_eryon_map_bins import compile_plan
        t=league()
        self.assertIn((70,25),connected(t,(0,36)))
        self.assertIn((80,28),connected(t,(0,36)))
        self.assertIn((48,36),connected(t,(0,36)))
        info=json.loads((ROOT/"data/maps/Eryon_CidadeDaLiga/map.json").read_text())
        self.assertEqual([(e["x"],e["y"]) for e in info["warp_events"]],[(0,36),(48,36)])
        signs=[e for e in info["bg_events"] if e["script"]=="EryonCidadeLiga_EventScript_EightStarsTerrace"]
        self.assertEqual([(e["x"],e["y"]) for e in signs],[(70,25)])
        scripts=(ROOT/"data/maps/Eryon_CidadeDaLiga/scripts.inc").read_text()
        self.assertIn("EryonCidadeLiga_EventScript_EightStarsTerrace::",scripts)
        plan=ROOT/"docs/eryon/liga_eryon_terrain_plan.txt"
        self.assertEqual(plan.read_text(),render("liga_eryon",t))
        expected=compile_plan(plan,{"#":0x3c01,".":0x3001,",":0x3002,"L":0x3001},
                              width=96,height=72)
        bin=(ROOT/"data/layouts/Eryon_CidadeDaLiga/map.bin").read_bytes()
        self.assertEqual(bin,expected)
        for x,y in ((0,36),(48,36),(70,25),(80,28)):
            self.assertEqual(struct.unpack_from("<H",bin,2*(y*96+x))[0]&0x0c00,0)


if __name__=="__main__":
    unittest.main()
