"""Static tests of optional Route 04 Eclipse cargo investigation."""
import json
import re
import unittest
from collections import deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FLAGS = ("FLAG_ERYON_ORCHARD_LEDGER_READ", "FLAG_ERYON_ORCHARD_RELAY_TRACED")


class Route04InvestigationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.m = json.loads((ROOT / "data/maps/Eryon_Rota04/map.json").read_text())
        cls.s = (ROOT / "data/maps/Eryon_Rota04/scripts.inc").read_text()
        cls.rows = (ROOT / "docs/eryon/rota_04_terrain_plan.txt").read_text().splitlines()[4:]

    def test_all_events_accessible_from_west_entrance(self):
        self.assertEqual(len(self.rows), 44)
        self.assertTrue(all(len(row) == 48 for row in self.rows))
        q = deque([(0, 22)])
        reachable = {(0, 22)}
        while q:
            x, y = q.popleft()
            for nx, ny in ((x-1,y), (x+1,y), (x,y-1), (x,y+1)):
                if 0 <= nx < 48 and 0 <= ny < 44 and self.rows[ny][nx] != "#" and (nx,ny) not in reachable:
                    reachable.add((nx,ny))
                    q.append((nx,ny))
        for category in ("object_events", "bg_events", "warp_events"):
            for e in self.m[category]:
                with self.subTest(event=e):
                    self.assertIn((e["x"],e["y"]), reachable)
        # The orchard now includes a new grove and caravan cache. Retain
        # original clues without forbidding additional reachable landmarks.
        self.assertTrue({(10,9),(35,32)} <=
                        {(e["x"],e["y"]) for e in self.m["bg_events"]})
        self.assertEqual(len(self.m["warp_events"]), 2)
        self.assertIn((11,10),{(e["x"],e["y"]) for e in self.m["object_events"]})
        self.assertEqual((self.m["object_events"][0]["x"],self.m["object_events"][0]["y"]),(24,21))

    def test_event_script_definitions_and_no_duplicate_positions(self):
        npcs = [(e["x"],e["y"]) for e in self.m["object_events"]]
        self.assertEqual(len(npcs),len(set(npcs)))
        for group in ("object_events", "bg_events"):
            for e in self.m[group]:
                self.assertIn(e["script"]+"::",self.s)

    def test_ordered_persistent_clues_and_unique_flags(self):
        raw=(ROOT/"include/constants/flags.h").read_text()
        defs=re.findall(r"^#define\s+(FLAG_\w+)\s+(0x[0-9A-Fa-f]+)",raw,re.MULTILINE)
        for value,name in zip((0x4B9,0x4BA),FLAGS):
            self.assertEqual([n for n,v in defs if int(v,16)==value],[name])
        self.assertIn("setflag "+FLAGS[0],self.s)
        self.assertIn("goto_if_unset "+FLAGS[0]+", EryonRota04_EventScript_RelayUnclear",self.s)
        self.assertIn("setflag "+FLAGS[1],self.s)

    def test_dialogue_follows_clues_without_badge_gating(self):
        vila=(ROOT/"data/maps/Eryon_VilaDosPomares/scripts.inc").read_text()
        neon=(ROOT/"data/maps/Eryon_Neonara/scripts.inc").read_text()
        route03=(ROOT/"data/maps/Eryon_Rota03/scripts.inc").read_text()
        self.assertIn("goto_if_set "+FLAGS[1]+", EryonRota03_EventScript_ResearcherOrchardRelay",route03)
        self.assertIn("EryonRota03_EventScript_ResearcherOrchardRelay::",route03)
        self.assertIn("goto_if_set "+FLAGS[0],vila)
        self.assertIn("goto_if_set "+FLAGS[1],vila)
        self.assertIn("goto_if_set "+FLAGS[1],neon)
        self.assertIn("EryonNeonara_EventScript_TechnicianOrchard::",neon)
        self.assertIn("goto_if_unset FLAG_BADGE01_GET",neon)
        self.assertIn("setflag FLAG_BADGE02_GET",neon)


if __name__=="__main__":
    unittest.main()
