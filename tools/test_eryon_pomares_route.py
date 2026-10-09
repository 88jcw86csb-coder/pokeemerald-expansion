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
        frostheim=json.loads((ROOT/"data/maps/Eryon_Frostheim/map.json").read_text())
        east=glacial["warp_events"][1]
        west=frostheim["warp_events"][0]
        self.assertEqual((east["dest_map"],east["dest_warp_id"]),("MAP_ERYON_FROSTHEIM","0"))
        self.assertEqual((west["dest_map"],west["dest_warp_id"]),("MAP_ERYON_TRILHA_GLACIAL","1"))
        self.assertNotEqual(glacial_rows[22][47],"#")
        frostheim_plan=ROOT/"docs/eryon/cidades/frostheim_city_plan.txt"
        city_tiles={**TILES,"=":TILES["."],**{k:TILES["."] for k in "GCMHP"}}
        self.assertEqual(len(compile_plan(frostheim_plan,city_tiles,64,56)),7168)
        frostheim_rows=frostheim_plan.read_text(encoding="utf-8").splitlines()[4:]
        self.assertNotEqual(frostheim_rows[12][0],"#")
        for map_data,terrain,script_path in (
            (glacial,glacial_rows,ROOT/"data/maps/Eryon_TrilhaGlacial/scripts.inc"),
            (frostheim,frostheim_rows,ROOT/"data/maps/Eryon_Frostheim/scripts.inc"),
        ):
            scripts=script_path.read_text(encoding="utf-8")
            for npc in map_data["object_events"]:
                self.assertNotEqual(terrain[npc["y"]][npc["x"]],"#")
                self.assertIn(npc["script"]+"::",scripts)
        self.assertIn("Bjorn", (ROOT/"data/maps/Eryon_Frostheim/scripts.inc").read_text())
        ridge=json.loads((ROOT/"data/maps/Eryon_SerraDosCristais/map.json").read_text())
        ridge_plan=ROOT/"docs/eryon/serra_dos_cristais_terrain_plan.txt"
        ridge_rows=ridge_plan.read_text(encoding="utf-8").splitlines()[4:]
        city_east=frostheim["warp_events"][1]
        ridge_west=ridge["warp_events"][2]
        self.assertEqual((city_east["dest_map"],city_east["dest_warp_id"]),("MAP_ERYON_SERRA_DOS_CRISTAIS","2"))
        self.assertEqual((ridge_west["dest_map"],ridge_west["dest_warp_id"]),("MAP_ERYON_FROSTHEIM","1"))
        self.assertNotEqual(frostheim_rows[12][63],"#")
        self.assertNotEqual(ridge_rows[24][0],"#")
        frostheim_scripts=(ROOT/"data/maps/Eryon_Frostheim/scripts.inc").read_text()
        bjorn=next(n for n in frostheim["object_events"] if n["script"]=="EryonFrostheim_EventScript_Bjorn")
        self.assertNotEqual(frostheim_rows[bjorn["y"]][bjorn["x"]],"#")
        self.assertIn("EryonFrostheim_EventScript_BjornAfterClue::",frostheim_scripts)
        refuge=json.loads((ROOT/"data/maps/Eryon_RefugioCristal/map.json").read_text())
        ridge_to_refuge=ridge["warp_events"][3]
        refuge_to_ridge=refuge["warp_events"][0]
        self.assertEqual((ridge_to_refuge["dest_map"],ridge_to_refuge["dest_warp_id"]),("MAP_ERYON_REFUGIO_CRISTAL","0"))
        self.assertEqual((refuge_to_ridge["dest_map"],refuge_to_ridge["dest_warp_id"]),("MAP_ERYON_SERRA_DOS_CRISTAIS","3"))
        self.assertNotEqual(ridge_rows[27][47],"#")
        refuge_plan=ROOT/"docs/eryon/vilas/refugio_cristal_village_plan.txt"
        village_tiles={**TILES,**{k:TILES["."] for k in "PCMHI"}}
        self.assertEqual(len(compile_plan(refuge_plan,village_tiles,36,30)),2160)
        refuge_rows=refuge_plan.read_text(encoding="utf-8").splitlines()[4:]
        self.assertNotEqual(refuge_rows[13][0],"#")
        caretaker=refuge["object_events"][0]
        self.assertNotEqual(refuge_rows[caretaker["y"]][caretaker["x"]],"#")
        refuge_scripts=(ROOT/"data/maps/Eryon_RefugioCristal/scripts.inc").read_text()
        self.assertIn(caretaker["script"]+"::",refuge_scripts)
        self.assertIn("goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND",refuge_scripts)

        self.assertIn("VAR_ERYON_SERRA_CLUE_FOUND",frostheim_scripts)
        neonara=json.loads((ROOT/"data/maps/Eryon_Neonara/map.json").read_text())
        neonara_rows=(ROOT/"docs/eryon/cidades/neonara_city_plan.txt").read_text().splitlines()[4:]
        neonara_scripts=(ROOT/"data/maps/Eryon_Neonara/scripts.inc").read_text()
        for npc in neonara["object_events"]:
            self.assertNotEqual(neonara_rows[npc["y"]][npc["x"]],"#")
            self.assertIn(npc["script"]+"::",neonara_scripts)
        self.assertIn("EryonNeonara_EventScript_TechnicianAfterClue::",neonara_scripts)
        self.assertIn("EryonNeonara_EventScript_GymStewardClue::",neonara_scripts)
        passage=json.loads((ROOT/"data/maps/Eryon_PassagemRochosa/map.json").read_text())
        passage_rows=(ROOT/"docs/eryon/passagem_rochosa_terrain_plan.txt").read_text().splitlines()[4:]
        manifest=next(e for e in passage["bg_events"] if e["script"]=="EryonPassagem_EventScript_CargoManifest")
        self.assertNotEqual(passage_rows[manifest["y"]][manifest["x"]],"#")
        passage_scripts=(ROOT/"data/maps/Eryon_PassagemRochosa/scripts.inc").read_text()
        self.assertIn("EryonPassagem_EventScript_CargoManifestClue::",passage_scripts)


        for script in ("Eryon_TrilhaGlacial", "Eryon_Frostheim"):
            content=(ROOT/f"data/maps/{script}/scripts.inc").read_text()
            self.assertIn("goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND",content)
            self.assertIn("ResearcherExposed" if script=="Eryon_TrilhaGlacial" else "ResearcherAfterClue",content)










if __name__=="__main__":
    unittest.main()
