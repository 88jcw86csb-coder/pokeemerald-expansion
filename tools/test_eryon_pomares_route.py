#!/usr/bin/env python3
"""Static regression for the Pomares-to-Route-04 expansion."""
import json
import unittest
from pathlib import Path
from build_eryon_map_bins import compile_plan

ROOT=Path(__file__).resolve().parents[1]
TILES={"#":0x3C01,".":0x3001,",":0x3002,":":0x3003}


class PomaresRouteTests(unittest.TestCase):
    def test_route_04_terrain_and_reciprocal_warps(self):
        plan=ROOT/"docs/eryon/rota_04_terrain_plan.txt"
        payload=compile_plan(plan,TILES,width=48,height=44)
        self.assertEqual(len(payload),4224)
        rows=plan.read_text(encoding="utf-8").splitlines()[4:]
        self.assertEqual(rows[22][0],".")
        self.assertEqual(rows[22][47],".")
        village=json.loads((ROOT/"data/maps/Eryon_VilaDosPomares/map.json").read_text())
        route=json.loads((ROOT/"data/maps/Eryon_Rota04/map.json").read_text())
        out=village["warp_events"][1]
        back=route["warp_events"][0]
        self.assertEqual((out["dest_map"],out["dest_warp_id"]),("MAP_ERYON_ROTA04","0"))
        self.assertEqual((back["dest_map"],back["dest_warp_id"]),("MAP_ERYON_VILA_DOS_POMARES","1"))
        self.assertEqual((out["x"],out["y"]),(35,14))
        self.assertEqual((back["x"],back["y"]),(0,22))
        route03=json.loads((ROOT/"data/maps/Eryon_Rota03/map.json").read_text())
        forward=route["warp_events"][1]
        reverse=route03["warp_events"][2]
        self.assertEqual((forward["dest_map"],forward["dest_warp_id"]),("MAP_ERYON_ROTA03","2"))
        self.assertEqual((reverse["dest_map"],reverse["dest_warp_id"]),("MAP_ERYON_ROTA04","1"))
        self.assertEqual((forward["x"],forward["y"]),(47,22))
        self.assertEqual((reverse["x"],reverse["y"]),(0,11))
        scout=route["object_events"][0]
        self.assertEqual((scout["x"],scout["y"]),(24,21))
        self.assertNotEqual(rows[scout["y"]][scout["x"]],"#")
        scripts=(ROOT/"data/maps/Eryon_Rota04/scripts.inc").read_text()
        self.assertIn(scout["script"]+"::",scripts)
        neonara=json.loads((ROOT/"data/maps/Eryon_Neonara/map.json").read_text())
        east=route03["warp_events"][3]
        west=neonara["warp_events"][0]
        self.assertEqual((east["dest_map"],east["dest_warp_id"]),("MAP_ERYON_NEONARA","0"))
        self.assertEqual((west["dest_map"],west["dest_warp_id"]),("MAP_ERYON_ROTA03","3"))
        self.assertEqual((east["x"],east["y"]),(49,11))
        self.assertEqual((west["x"],west["y"]),(0,28))
        city_plan=ROOT/"docs/eryon/cidades/neonara_city_plan.txt"
        city_tiles={**TILES,"=":TILES["."],**{k:TILES["."] for k in "GCMHP"}}
        self.assertEqual(len(compile_plan(city_plan,city_tiles,64,56)),7168)
        city_rows=city_plan.read_text(encoding="utf-8").splitlines()[4:]
        self.assertNotEqual(city_rows[28][0],"#")
        resident=neonara["object_events"][0]
        self.assertNotEqual(city_rows[resident["y"]][resident["x"]],"#")
        city_scripts=(ROOT/"data/maps/Eryon_Neonara/scripts.inc").read_text()
        self.assertIn(resident["script"]+"::",city_scripts)

        self.assertNotIn(r"\\\\n", scripts)
        hills=json.loads((ROOT/"data/maps/Eryon_ColinasDaNeblina/map.json").read_text())
        city_exit=neonara["warp_events"][1]
        hill_entry=hills["warp_events"][0]
        self.assertEqual((city_exit["dest_map"],city_exit["dest_warp_id"]),("MAP_ERYON_COLINAS_DA_NEBLINA","0"))
        self.assertEqual((hill_entry["dest_map"],hill_entry["dest_warp_id"]),("MAP_ERYON_NEONARA","1"))
        self.assertEqual((city_exit["x"],city_exit["y"]),(63,28))
        self.assertEqual((hill_entry["x"],hill_entry["y"]),(0,22))
        hill_plan=ROOT/"docs/eryon/colinas_da_neblina_terrain_plan.txt"
        self.assertEqual(len(compile_plan(hill_plan,TILES,48,44)),4224)
        self.assertNotEqual(hill_plan.read_text(encoding="utf-8").splitlines()[4+22][0],"#")
        village2=json.loads((ROOT/"data/maps/Eryon_VilaDaNeblina/map.json").read_text())
        hill_exit=hills["warp_events"][1]
        village_entry=village2["warp_events"][0]
        self.assertEqual((hill_exit["dest_map"],hill_exit["dest_warp_id"]),("MAP_ERYON_VILA_DA_NEBLINA","0"))
        self.assertEqual((village_entry["dest_map"],village_entry["dest_warp_id"]),("MAP_ERYON_COLINAS_DA_NEBLINA","1"))
        self.assertEqual((hill_exit["x"],hill_exit["y"]),(47,22))
        self.assertEqual((village_entry["x"],village_entry["y"]),(0,14))
        village_plan=ROOT/"docs/eryon/vilas/vila_da_neblina_village_plan.txt"
        village_tiles={**TILES,**{k:TILES["."] for k in "PCMHI"}}
        self.assertEqual(len(compile_plan(village_plan,village_tiles,36,30)),2160)
        village_rows=village_plan.read_text(encoding="utf-8").splitlines()[4:]
        self.assertNotEqual(village_rows[14][0],"#")
        elder=village2["object_events"][0]
        self.assertNotEqual(village_rows[elder["y"]][elder["x"]],"#")
        village_scripts=(ROOT/"data/maps/Eryon_VilaDaNeblina/scripts.inc").read_text(encoding="utf-8")
        self.assertIn(elder["script"]+"::",village_scripts)
        glacial=json.loads((ROOT/"data/maps/Eryon_TrilhaGlacial/map.json").read_text())
        village_exit=village2["warp_events"][1]
        glacial_entry=glacial["warp_events"][0]
        self.assertEqual((village_exit["dest_map"],village_exit["dest_warp_id"]),("MAP_ERYON_TRILHA_GLACIAL","0"))
        self.assertEqual((glacial_entry["dest_map"],glacial_entry["dest_warp_id"]),("MAP_ERYON_VILA_DA_NEBLINA","1"))
        glacial_plan=ROOT/"docs/eryon/trilha_glacial_terrain_plan.txt"
        self.assertEqual(len(compile_plan(glacial_plan,TILES,48,44)),4224)
        glacial_rows=glacial_plan.read_text(encoding="utf-8").splitlines()[4:]
        self.assertNotEqual(glacial_rows[22][0],"#")
        guide=glacial["object_events"][0]
        self.assertNotEqual(glacial_rows[guide["y"]][guide["x"]],"#")
        guide_script=(ROOT/"data/maps/Eryon_TrilhaGlacial/scripts.inc").read_text()
        self.assertIn(guide["script"]+"::",guide_script)
        self.assertIn("eclipse",guide_script.lower())








if __name__=="__main__":
    unittest.main()
