"""Ensure the first Eryon town uses the original professor, never Birch."""
from pathlib import Path
import json
import unittest
from test_eryon_png_integrity import decode_indexed_png
ROOT=Path(__file__).resolve().parents[1]

class ProfessorElyaVisualContract(unittest.TestCase):
    def test_intro_and_village_are_consistently_elya(self):
        city=json.loads((ROOT/"data/maps/Eryon_VilaAurora/map.json").read_text())
        professor=[e for e in city["object_events"] if "ProfessorElya" in e["script"]]
        self.assertEqual(len(professor),1)
        self.assertEqual(professor[0]["graphics_id"],"OBJ_EVENT_GFX_ERYON_ELYA")
        src=(ROOT/"src/main_menu.c").read_text()
        self.assertIn("CreateTrainerSprite(TRAINER_PIC_ERYON_ELYA",src)
        self.assertNotIn("OBJ_EVENT_GFX_PROF_BIRCH",json.dumps(city))

    def test_dedicated_professor_sprite_has_all_eight_gba_frames(self):
        path=ROOT/"graphics/object_events/pics/people/eryon_elya.png"
        w,h,px=decode_indexed_png(path)
        self.assertEqual((w,h),(32,128))
        for n in range(8):
            x=(n%2)*16;y=(n//2)*32
            visible=sum(px[yy*w+xx]!=0 for yy in range(y,y+32) for xx in range(x,x+16))
            self.assertGreater(visible,100,(n,visible))

    def test_registered_gba_object_palette_and_animation_table(self):
        base=ROOT/"src/data/object_events"
        for name,part in (
            ("object_event_graphics.h","gObjectEventPic_EryonElya"),
            ("object_event_pic_tables.h","sPicTable_EryonElya"),
            ("object_event_graphics_info.h","gObjectEventGraphicsInfo_EryonElya"),
            ("object_event_graphics_info_pointers.h","OBJ_EVENT_GFX_ERYON_ELYA"),
        ):
            self.assertIn(part,(base/name).read_text())
        self.assertIn("OBJ_EVENT_GFX_ERYON_ELYA,",
                      (ROOT/"include/constants/event_objects.h").read_text())
if __name__=="__main__":unittest.main()
