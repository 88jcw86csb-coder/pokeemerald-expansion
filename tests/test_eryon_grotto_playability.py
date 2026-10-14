"""Gameplay structural regression for Star Grotto terrain and Eclipse battle.

Run from repository root:
    python3 -m unittest discover -s tests -p 'test_eryon_grotto_playability.py'

Uses actual map.bin cells, but is not a substitute for compiling or emulator play.
"""
import json
import re
import unittest
from collections import deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CAVE = ROOT / "data/maps/Eryon_GrutaDasEstrelas"
ROAD = ROOT / "data/maps/Eryon_CaminhoDaLiga"
W, H = 48, 44
BATTLE = "TRAINER_ERYON_GROTTO_ECLIPSE"
DEFEAT_FLAG = "FLAG_ERYON_GROTTO_ECLIPSE_SCOUT_DEFEATED"


class EryonGrottoPlayability(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        raw = (ROOT / "data/layouts/Eryon_GrutaDasEstrelas/map.bin").read_bytes()
        assert len(raw) == W * H * 2, "Unexpected grotto layout dimensions"
        cls.floor = set()
        for y in range(H):
            for x in range(W):
                offset = 2 * (y * W + x)
                metatile = int.from_bytes(raw[offset:offset + 2], "little")
                if metatile & 0x3FF == 3:  # Existing walkable grotto metatile
                    cls.floor.add((x, y))
        cls.map = json.loads((CAVE / "map.json").read_text(encoding="utf-8"))
        cls.script = (CAVE / "scripts.inc").read_text(encoding="utf-8")

    @staticmethod
    def flood(start, floor):
        seen = {start}
        pending = deque([start])
        while pending:
            x, y = pending.popleft()
            for node in ((x-1, y), (x+1, y), (x, y-1), (x, y+1)):
                if node in floor and node not in seen:
                    seen.add(node)
                    pending.append(node)
        return seen

    def test_connected_exits_even_with_stationary_npcs(self):
        start, end = ((w["x"], w["y"]) for w in self.map["warp_events"])
        self.assertIn(start, self.floor)
        self.assertIn(end, self.floor)
        self.assertIn(end, self.flood(start, self.floor))
        occupied = {(o["x"], o["y"]) for o in self.map["object_events"]}
        self.assertIn(end, self.flood(start, self.floor - occupied))

    def test_each_npc_and_optional_event_is_accessible(self):
        start = (self.map["warp_events"][0]["x"], self.map["warp_events"][0]["y"])
        reachable = self.flood(start, self.floor)
        for obj in self.map["object_events"]:
            with self.subTest(script=obj["script"]):
                point = (obj["x"], obj["y"])
                self.assertIn(point, self.floor)
                self.assertTrue(any(p in reachable for p in (
                    (point[0]-1, point[1]), (point[0]+1, point[1]),
                    (point[0], point[1]-1), (point[0], point[1]+1)
                )))
        for event in self.map["bg_events"]:
            with self.subTest(script=event["script"]):
                point = (event["x"], event["y"])
                self.assertTrue(any(p in reachable for p in (
                    (point[0]-1, point[1]), (point[0]+1, point[1]),
                    (point[0], point[1]-1), (point[0], point[1]+1)
                )))

    def test_isolated_flag_and_trainer_party(self):
        flags = (ROOT / "include/constants/flags.h").read_text(encoding="utf-8")
        opponents = (ROOT / "include/constants/opponents.h").read_text(encoding="utf-8")
        setup = (ROOT / "src/battle_setup.c").read_text(encoding="utf-8")
        parties = (ROOT / "src/data/trainers.party").read_text(encoding="utf-8")
        self.assertIn(f"#define {DEFEAT_FLAG} 0x42", flags)
        self.assertIn(f"#define {BATTLE} 872", opponents)
        self.assertGreaterEqual(
            int(re.search(r"(?m)^#define TRAINERS_COUNT_EMERALD\s+(\d+)", opponents).group(1)),
            873,
        )
        self.assertIn(f"if (trainerId == {BATTLE})", setup)
        self.assertIn(f"return {DEFEAT_FLAG};", setup)
        self.assertIn(f"=== {BATTLE} ===", parties)
        trainer_block = parties.split(f"=== {BATTLE} ===", 1)[1]
        for mon in ("Houndoom", "Golbat", "Magneton"):
            self.assertRegex(trainer_block, rf"(?m)^{mon}$")
        self.assertEqual(len(re.findall(rf"(?m)^=== {BATTLE} ===$", parties)), 1)

    def test_battle_is_optional_and_chart_gated(self):
        self.assertIn(
            "goto_if_set FLAG_ERYON_STAR_CHART_READ, "
            "EryonEstrelas_EventScript_ScoutBattleOffer", self.script)
        self.assertIn(
            "goto_if_set FLAG_ERYON_STAR_GROTTO_RELAY_DISABLED, "
            "EryonEstrelas_EventScript_ScoutRelayOff", self.script)
        self.assertIn(
            "goto_if_set FLAG_ERYON_GROTTO_ECLIPSE_SCOUT_DEFEATED, "
            "EryonEstrelas_EventScript_ScoutDefeated", self.script)
        self.assertIn(
            f"trainerbattle_single {BATTLE},", self.script)
        self.assertIn("MSGBOX_YESNO", self.script)
        road_script = (ROAD / "scripts.inc").read_text(encoding="utf-8")
        self.assertIn(
            "goto_if_set FLAG_ERYON_GROTTO_ECLIPSE_SCOUT_DEFEATED, "
            "EryonLigaCaminho_EventScript_GuardianScoutDefeated", road_script)

    def test_astronomer_story_prioritizes_league_epilogue(self):
        obj = [o for o in self.map["object_events"]
               if o["script"] == "EryonEstrelas_EventScript_Astronomer"]
        self.assertEqual(len(obj), 1)
        block = self.script.split("EryonEstrelas_EventScript_Astronomer::", 1)[1].split(
            "EryonEstrelas_EventScript_AstronomerAfterChart::", 1)[0]
        ordered = (
            "FLAG_ERYON_CHAMPION_CROWNED",
            "FLAG_ERYON_ECLIPSE_EVIDENCE_REPORTED",
            "FLAG_ERYON_STAR_GROTTO_RELAY_DISABLED",
            "FLAG_ERYON_STAR_CHART_READ",
        )
        self.assertEqual(list(map(block.index, ordered)), sorted(map(block.index, ordered)))
        for suffix in ("RelayOff", "Evidence", "Champion"):
            self.assertIn("EryonEstrelas_EventScript_Astronomer" + suffix + "::", self.script)
            self.assertIn("EryonEstrelas_Text_Astronomer" + suffix + ":", self.script)
        self.assertNotIn("setflag ", block)
        self.assertNotIn("trainerbattle_", block)


if __name__ == "__main__":
    unittest.main()
