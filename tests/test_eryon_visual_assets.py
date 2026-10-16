"""Ensure Eryon's new GBA portraits are generated and actually used."""
import importlib.util
import json
from pathlib import Path
import re
import struct
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
GENERATOR = ROOT / "tools/eryon_visual_assets.py"
spec = importlib.util.spec_from_file_location("eryon_visual_assets", GENERATOR)
visuals = importlib.util.module_from_spec(spec)
spec.loader.exec_module(visuals)

LEADERS = {
    "TRAINER_ERYON_KAEL": "Eryon Kael",
    "TRAINER_ERYON_GYM_NEONARA": "Eryon Volt",
    "TRAINER_ERYON_GYM_FROSTHEIM": "Eryon Bjorn",
    "TRAINER_ERYON_GYM_ARKHARA": "Eryon Tessa",
    "TRAINER_ERYON_GYM_UMBRA": "Eryon Nyx",
    "TRAINER_ERYON_GYM_IGNIVAR": "Eryon Kaio",
    "TRAINER_ERYON_GYM_LUNARIS": "Eryon Lyra",
    "TRAINER_ERYON_GYM_DRAKONIA": "Eryon Ryu",
}
class VisualAssetTests(unittest.TestCase):
    def test_original_gba_4bpp_images_are_distinct_and_palette_safe(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths=visuals.generate(Path(tmp))
            self.assertEqual(len(paths), 16)
            unique=set()
            for path in paths:
                png=path.read_bytes()
                self.assertEqual(png[:8], b"\x89PNG\r\n\x1a\n")
                width,height,depth,typ,*_=struct.unpack(">IIBBBBB",png[16:29])
                self.assertEqual((width,height,depth,typ),(64,64,4,3))
                self.assertEqual(int.from_bytes(png[33:37],"big"),48)
                unique.add(png)
            self.assertEqual(len(unique),16,"every leader/Eclipse/League portrait needs its own design")
    def test_all_eight_leaders_use_original_portraits_without_replacing_teams(self):
        trainers=(ROOT/"src/data/trainers.party").read_text()
        enums=(ROOT/"include/constants/trainers.h").read_text()
        graphics=(ROOT/"src/data/graphics/trainers.h").read_text()
        for trainer,pic in LEADERS.items():
            with self.subTest(trainer=trainer):
                body=trainers.split("=== "+trainer+" ===",1)[1].split("\n===",1)[0]
                self.assertIn("Pic: "+pic,body)
                self.assertIn("\nLevel: ",body)
                macro="TRAINER_PIC_"+pic.replace(" ","_").upper()
                self.assertIn(macro+",",enums)
                self.assertIn("["+macro+"] =",graphics)
    def test_eclipse_commander_and_patrol_have_new_identity(self):
        data=(ROOT/"src/data/trainers.party").read_text()
        cmd=data.split("=== TRAINER_ERYON_DRAKONIA_ECLIPSE ===",1)[1].split("\n===",1)[0]
        self.assertIn("Pic: Eryon Commander",cmd)
        self.assertIn("Pic: Eryon Eclipse",data)
        self.assertIn("gTrainerFrontPic_EryonEclipse", (ROOT/"src/data/graphics/trainers.h").read_text())
    def test_eclipse_field_sprite_has_eight_native_gba_frames(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = visuals.make_eclipse_field_sprite(Path(tmp) / "eclipse.png")
            raw = path.read_bytes()
            self.assertEqual(raw[:8], b"\x89PNG\r\n\x1a\n")
            self.assertEqual(struct.unpack(">IIBBBBB", raw[16:29])[:4],
                             (32, 128, 4, 3))
            graphics = (ROOT / "src/data/object_events/object_event_graphics.h").read_text()
            info = (ROOT / "src/data/object_events/object_event_graphics_info.h").read_text()
            pointers = (ROOT / "src/data/object_events/object_event_graphics_info_pointers.h").read_text()
            const = (ROOT / "include/constants/event_objects.h").read_text()
            self.assertIn("gObjectEventPic_EryonEclipse[]", graphics)
            self.assertIn(".images = sPicTable_EryonEclipse,", info)
            self.assertIn("[OBJ_EVENT_GFX_ERYON_ECLIPSE]", pointers)
            self.assertIn("    OBJ_EVENT_GFX_ERYON_ECLIPSE,", const)

    def test_eclipse_agent_references_are_replaced_but_others_preserved(self):
        maps = json.loads((ROOT / "data/maps/map_groups.json").read_text())["gMapGroup_Eryon"]
        modified = 0
        for name in maps:
            info = json.loads((ROOT / "data/maps" / name / "map.json").read_text())
            for npc in info["object_events"]:
                if "Eclipse" in npc.get("script", "") or "CoreGuardian" in npc.get("script", ""):
                    if npc["graphics_id"] == "OBJ_EVENT_GFX_ERYON_ECLIPSE":
                        modified += 1
                    self.assertNotEqual(npc["graphics_id"], "OBJ_EVENT_GFX_AQUA_MEMBER_M")
        self.assertGreaterEqual(modified, 16)

    def test_eryon_protagonist_has_complete_field_animation_sizes(self):
        base=ROOT/"graphics/object_events/pics/people/eryon_hero"
        expected={"walking":144,"running":144,"field_move":160,
                  "surfing":192,"mach_bike":288,"acro_bike":864,
                  "fishing":384,"underwater":128}
        for name,width in expected.items():
            with self.subTest(action=name):
                pic=(base/(name+".png")).read_bytes()
                self.assertEqual(pic[:8],b"\x89PNG\r\n\x1a\n")
                info=struct.unpack(">IIBBBBB",pic[16:29])
                self.assertEqual(info[:4],(width,32,4,3))
        self.assertTrue((ROOT/"graphics/object_events/palettes/eryon_hero.pal").is_file())
        obj=(ROOT/"src/data/object_events/object_event_graphics.h").read_text()
        for name in expected:
            self.assertIn("/eryon_hero/"+name+".",obj)

    def test_eryon_protagonist_battle_front_back_portraits(self):
        base=ROOT/"graphics/trainers"
        for relative,size in (("front_pics/eryon_hero.png",(64,64)),
                               ("back_pics/eryon_hero.png",(64,256))):
            data=(base/relative).read_bytes()
            self.assertEqual(struct.unpack(">II",data[16:24]),size)
        refs=(ROOT/"src/data/graphics/trainers.h").read_text()
        self.assertIn('gTrainerFrontPic_Brendan[] = INCGFX_U32("graphics/trainers/front_pics/eryon_hero.png"',refs)
        self.assertIn('gTrainerBackPic_Brendan[] = INCGFX_U8("graphics/trainers/back_pics/eryon_hero.png"',refs)

    def test_female_hero_keeps_may_special_anim_frame_counts(self):
        root=ROOT/"graphics/object_events/pics/people/eryon_hero_f"
        expected={"walking":144,"running":144,"field_move":160,
                  "surfing":192,"mach_bike":288,"acro_bike":864,
                  "fishing":384,"underwater":128,
                  "watering":192,"decorating":16}
        for name,width in expected.items():
            with self.subTest(name=name):
                b=(root/(name+".png")).read_bytes()
                self.assertEqual(struct.unpack(">IIBBBBB",b[16:29])[:4],
                                 (width,32,4,3))
        obj=(ROOT/"src/data/object_events/object_event_graphics.h").read_text()
        for name in expected:
            self.assertIn("/eryon_hero_f/"+name+".",obj)
        for name in ("brendan_reflection","may_reflection"):
            self.assertNotIn("palettes/"+name+".pal",obj)
        portraits=(ROOT/"src/data/graphics/trainers.h").read_text()
        self.assertIn("front_pics/eryon_hero_f.png",portraits)
        self.assertIn("back_pics/eryon_hero_f.png",portraits)
        self.assertEqual(struct.unpack(">II",(
            ROOT/"graphics/trainers/back_pics/eryon_hero_f.png").read_bytes()[16:24]),
            (64,256))

    def test_all_eight_leaders_have_unique_reachable_field_sprites(self):
        loc = {
            "Eryon_Verdelume": "KAEL",
            "Eryon_Neonara": "VOLT",
            "Eryon_Frostheim": "BJORN",
            "Eryon_Arkhara": "TESSA",
            "Eryon_Umbra": "NYX",
            "Eryon_Ignivar": "KAIO",
            "Eryon_Lunaris": "LYRA",
            "Eryon_Drakonia": "RYU",
        }
        ids=set()
        for city,leader in loc.items():
            with self.subTest(city=city):
                info=json.loads((ROOT/"data/maps"/city/"map.json").read_text())
                matches=[e for e in info["object_events"] if
                         ("GymLeader" in e["script"] or
                          e["script"].endswith(("Kael","Bjorn","Tessa")))]
                self.assertEqual(len(matches),1)
                gfx="OBJ_EVENT_GFX_ERYON_LEADER_"+leader
                self.assertEqual(matches[0]["graphics_id"],gfx)
                ids.add(gfx)
                img=ROOT/"graphics/object_events/pics/people/eryon_leaders"/(
                    "eryon_"+leader.lower()+".png")
                self.assertEqual(struct.unpack(">IIBBBBB",img.read_bytes()[16:29])[:4],
                                 (32,128,4,3))
        self.assertEqual(len(ids),8)
        ptr=(ROOT/"src/data/object_events/object_event_graphics_info_pointers.h").read_text()
        info=(ROOT/"src/data/object_events/object_event_graphics_info.h").read_text()
        for id in ids:
            self.assertIn("["+id+"]",ptr)
            self.assertIn("gObjectEventGraphicsInfo_EryonLeader",info)

    def test_image_generator_runs_before_make(self):
        script=(ROOT/"tools/build_eryon.sh").read_text()
        self.assertIn("python3 tools/eryon_visual_assets.py",script)
        self.assertLess(script.index("python3 tools/eryon_visual_assets.py"),
                        script.index('make -j"$jobs" -O all'))

if __name__=="__main__":
    unittest.main()
