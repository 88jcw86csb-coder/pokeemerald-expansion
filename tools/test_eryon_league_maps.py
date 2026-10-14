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


if __name__=="__main__":
    unittest.main()
