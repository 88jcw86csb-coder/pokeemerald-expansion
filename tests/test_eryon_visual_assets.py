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
            self.assertEqual(len(paths), 11)
            unique=set()
            for path in paths:
                png=path.read_bytes()
                self.assertEqual(png[:8], b"\x89PNG\r\n\x1a\n")
                width,height,depth,typ,*_=struct.unpack(">IIBBBBB",png[16:29])
                self.assertEqual((width,height,depth,typ),(64,64,4,3))
                self.assertEqual(int.from_bytes(png[33:37],"big"),48)
                unique.add(png)
            self.assertEqual(len(unique),11,"every leader/Eclipse portrait needs its own design")
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
    def test_image_generator_runs_before_make(self):
        script=(ROOT/"tools/build_eryon.sh").read_text()
        self.assertIn("python3 tools/eryon_visual_assets.py",script)
        self.assertLess(script.index("python3 tools/eryon_visual_assets.py"),
                        script.index('make -j"$jobs" -O all'))

if __name__=="__main__":
    unittest.main()
