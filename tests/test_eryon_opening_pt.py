"""Regression contracts for Eryon's intro, title and Portuguese menu.

This is static/source validation, NOT a claim of graphical playtesting in Delta.
"""
from pathlib import Path
import struct
import unittest
import zlib

ROOT=Path(__file__).resolve().parents[1]
def src(path):
    return (ROOT / path).read_text(encoding="utf-8")

class EryonOpeningTests(unittest.TestCase):
    def test_opening_skips_original_hoenn_movie(self):
        c=src("src/intro.c")
        opening=c.split("case COPYRIGHT_START_INTRO:",1)[1].split("return 0;",1)[0]
        self.assertIn("SetMainCallback2(CB2_InitTitleScreen)",opening)
        self.assertNotIn("CreateTask(Task_Scene1_Load",opening)
        self.assertNotIn("CreateTask(Task_HandleExpansionIntro",opening)

    def test_eryon_title_and_legacy_rayquaza_hidden(self):
        from importlib.util import spec_from_file_location, module_from_spec
        spec=spec_from_file_location("eryon_boot_assets",ROOT/"tools/eryon_boot_assets.py")
        mod=module_from_spec(spec)
        spec.loader.exec_module(mod)
        p=mod.generate()
        data=p.read_bytes()
        self.assertEqual(data[:8],b"\x89PNG\r\n\x1a\n")
        self.assertEqual(struct.unpack(">IIBBBBB",data[16:29])[:4],(128,32,8,3))
        self.assertEqual(zlib.crc32(data[37+48+12:37+48+12])&0xffffffff,0)
        self.assertEqual(src("src/graphics.c").count("title_screen/eryon_version.png"),2)
        self.assertNotIn("title_screen/emerald_version.png",src("src/graphics.c"))
        title=src("src/title_screen.c")
        self.assertIn("hide old Rayquaza silhouette",title)
        self.assertNotIn("| DISPCNT_BG0_ON\n                                    | DISPCNT_BG1_ON",title)

    def test_professor_elya_selected_heroes_and_portuguese(self):
        menu=src("src/main_menu.c")
        for fragment in ("TRAINER_PIC_ERYON_ELYA","CreateTrainerSprite(TRAINER_PIC_BRENDAN",
                         "CreateTrainerSprite(TRAINER_PIC_MAY","NOVO JOGO","CONTINUAR","OPCOES"):
            self.assertIn(fragment,menu)
        self.assertNotIn("birchSpriteId = AddNewGameBirchObject(",menu)
        intro=src("data/text/birch_speech.inc")
        self.assertIn("Meu nome e ELYA",intro)
        self.assertIn("Vila Aurora",intro)
        self.assertNotIn("LITTLEROOT",intro)
        self.assertNotIn("My name is BIRCH",intro)
        self.assertIn("TRAINER_PIC_ERYON_ELYA",src("include/constants/trainers.h"))
        self.assertIn("TRAINER_PIC_ERYON_ELYA",src("src/data/graphics/trainers.h"))
        for value in ("GAROTO","GAROTA","Voce escolhe este POKéMON?"):
            self.assertIn(value,src("src/strings.c"))

    def test_graphic_generator_runs_before_compilation(self):
        b=src("tools/build_eryon.sh")
        self.assertLess(b.index("python3 tools/eryon_boot_assets.py"),b.index('make -j"'))
        workflow=src(".github/workflows/build.yml")
        self.assertIn("python3 tools/eryon_boot_assets.py",workflow)

if __name__=="__main__":
    unittest.main()
