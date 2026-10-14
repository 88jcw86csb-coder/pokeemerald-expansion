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
