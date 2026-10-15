"""Check Route 04 binary map, landmarks, and one-time supplies."""
import json
import re
import struct
import unittest
from collections import deque
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
TILE={"#":0x3C01,".":0x3001,",":0x3002,":":0x3003}


class Route04Completion(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.m=json.loads((ROOT/"data/maps/Eryon_Rota04/map.json").read_text())
        cls.s=(ROOT/"data/maps/Eryon_Rota04/scripts.inc").read_text()
        cls.rows=(ROOT/"docs/eryon/rota_04_terrain_plan.txt").read_text().splitlines()[4:]

    def test_registered_binary_matches_plan(self):
        self.assertEqual(len(self.rows),44)
        self.assertTrue(all(len(r)==48 for r in self.rows))
        data=struct.pack("<2112H",*(TILE[ch] for row in self.rows for ch in row))
        self.assertEqual(len(data),4224)
        self.assertEqual(data,(ROOT/"data/layouts/Eryon_Rota04/map.bin").read_bytes())

    def test_all_landmarks_reachable_and_warps_preserved(self):
        self.assertEqual([(w["x"],w["y"]) for w in self.m["warp_events"]],[(0,22),(47,22)])
        self.assertEqual({(x["x"],x["y"]) for x in self.m["bg_events"]},
                         {(10,9),(35,32),(23,10),(21,34)})
        q=deque([(0,22)])
        seen={(0,22)}
        while q:
            x,y=q.popleft()
            for nx,ny in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
                if 0<=nx<48 and 0<=ny<44 and self.rows[ny][nx]!="#" and (nx,ny) not in seen:
                    seen.add((nx,ny))
                    q.append((nx,ny))
        self.assertGreaterEqual(len(seen),570)
        for group in ("object_events","bg_events","warp_events"):
            for e in self.m[group]:
                self.assertIn((e["x"],e["y"]),seen)
                if "script" in e:
                    self.assertIn(e["script"]+"::",self.s)

    def test_one_time_cache_can_be_retried_if_bag_is_full(self):
        flags=(ROOT/"include/constants/flags.h").read_text()
        self.assertRegex(flags,r"#define FLAG_ERYON_ORCHARD_CARAVAN_CACHE_TAKEN\s+0x4BC")
        self.assertEqual(len(re.findall(r"(?m)^#define FLAG_\w+\s+0x4BC\b",flags)),1)
        body=self.s.split("EryonRota04_EventScript_CaravanCache::",1)[1].split(
            "EryonRota04_EventScript_CaravanCacheFull::",1)[0]
        self.assertIn("giveitem ITEM_FULL_HEAL",body)
        self.assertLess(body.index("goto_if_eq VAR_RESULT, FALSE"),body.index("setflag FLAG_ERYON_ORCHARD_CARAVAN_CACHE_TAKEN"))
        self.assertIn("goto_if_set FLAG_ERYON_ECLIPSE_NETWORK_SHUT_DOWN",self.s)


if __name__=="__main__":
    unittest.main()
