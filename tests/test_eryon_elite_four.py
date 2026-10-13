"""Elite Four gallery integration, ordered battles and GBA map collision contract.

Run from the repository root:
    python3 -m unittest discover -s tests -p 'test_eryon_elite_four.py' -v

Static checks only: emulator battle/whiteout/save tests and ROM compilation
are separate requirements.
"""
import json
import re
import unittest
from collections import deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GALLERY = ROOT / "data/maps/Eryon_LigaEliteFour"
ELITE = GALLERY / "scripts.inc"
RECOVERY = ROOT / "data/maps/Eryon_LigaRecuperacao/scripts.inc"
CITY = ROOT / "data/maps/Eryon_CidadeDaLiga/scripts.inc"
W, H = 56, 40
NAMES = ["Aria", "Bastian", "Selene", "Darius", "Champion"]
TRAINERS = [f"TRAINER_ERYON_ELITE_{i}" for i in range(1, 5)] + ["TRAINER_ERYON_CHAMPION"]
FLAGS = [f"FLAG_ERYON_ELITE_TRAINER_{i}_DEFEATED" for i in range(1, 5)]
FLAGS.append("FLAG_ERYON_CHAMPION_TRAINER_DEFEATED")


def neighbors(p):
    x, y = p
    return ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1))


def body(src, name):
    m = re.search(
        rf"(?ms)^{re.escape(name)}::?\n(.*?)(?=^[A-Za-z_][A-Za-z_0-9]*::?\s*$|\Z)",
        src,
    )
    if m is None:
        raise AssertionError(f"Missing script {name}")
    return m.group(1)


class EliteFourContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.map = json.loads((GALLERY / "map.json").read_text(encoding="utf-8"))
        cls.script = ELITE.read_text(encoding="utf-8")
        cls.recovery = RECOVERY.read_text(encoding="utf-8")
        data = (ROOT / "data/layouts/Eryon_LigaEliteFour/map.bin").read_bytes()
        assert len(data) == W * H * 2
        cls.floor = set()
        for y in range(H):
            for x in range(W):
                i = 2 * (y * W + x)
                word = int.from_bytes(data[i:i + 2], "little")
                if (word >> 10) & 3 == 0:
                    cls.floor.add((x, y))

    def test_map_registered_and_scripts_included_in_assembly(self):
        groups = json.loads((ROOT / "data/maps/map_groups.json").read_text(encoding="utf-8"))
        layouts = json.loads((ROOT / "data/layouts/layouts.json").read_text(encoding="utf-8"))
        self.assertIn("Eryon_LigaEliteFour", groups["gMapGroup_Eryon"])
        self.assertTrue(any(x["id"] == "LAYOUT_ERYON_LIGA_ELITE_FOUR"
                            and (x["width"], x["height"]) == (W, H)
                            for x in layouts["layouts"]))
        includes = (ROOT / "data/event_scripts.s").read_text(encoding="utf-8")
        self.assertEqual(includes.count('data/maps/Eryon_LigaEliteFour/scripts.inc'), 1)
        self.assertIn("Eryon_LigaEliteFour_MapScripts::", self.script)

    def test_all_five_battle_podiums_reachable_from_entrance(self):
        origin = (28, 37)
        occupied = {(o["x"], o["y"]) for o in self.map["object_events"]}
        self.assertIn(origin, self.floor)
        visited = {origin}
        queue = deque((origin,))
        while queue:
            for p in neighbors(queue.popleft()):
                if p in self.floor and p not in occupied and p not in visited:
                    visited.add(p)
                    queue.append(p)
        self.assertEqual(len(self.map["object_events"]), 5)
        self.assertEqual({o["script"] for o in self.map["object_events"]},
                         {f"EryonLigaElite_EventScript_{n}" for n in NAMES})
        for event in self.map["object_events"] + self.map["bg_events"]:
            pt = (event["x"], event["y"])
            self.assertIn(pt, self.floor, event["script"])
            self.assertTrue(any(p in visited for p in neighbors(pt)),
                            f"Cannot approach {event['script']}")
        self.assertGreaterEqual(len(self.floor), 800)

    def test_qualification_and_order_never_bypassed(self):
        for i, (name, trainer, defeated) in enumerate(zip(NAMES, TRAINERS, FLAGS)):
            battle = body(self.script, f"EryonLigaElite_EventScript_{name}")
            self.assertIn("goto_if_unset FLAG_ERYON_QUALIFIED", battle)
            self.assertIn(f"goto_if_set {defeated}, EryonLigaElite_EventScript_Already",
                          battle)
            self.assertIn(f"trainerbattle_single {trainer},", battle)
            if i:
                self.assertIn(
                    f"goto_if_unset {FLAGS[i-1]}, EryonLigaElite_EventScript_Locked",
                    battle,
                )
            victory = body(self.script, f"EryonLigaElite_EventScript_Win{i+1}")
            self.assertIn(f"setflag {defeated}", victory)
        self.assertIn("setflag FLAG_ERYON_CHAMPION_CROWNED",
                      body(self.script, "EryonLigaElite_EventScript_Win5"))

    def test_elite_reset_does_not_erase_qualifier_flags(self):
        transition = body(self.script, "EryonLigaElite_OnTransition")
        self.assertIn("goto_if_set FLAG_ERYON_CHAMPION_CROWNED", transition)
        for trainer in TRAINERS:
            self.assertIn(f"cleartrainerflag {trainer}", transition)
        self.assertNotIn("TRAINER_ERYON_QUALIFIER_", transition)
        self.assertNotIn("FLAG_ERYON_QUALIFIED", transition)

    def test_healing_room_gate_and_safe_exit(self):
        gate = body(self.recovery, "EryonLigaRecover_EventScript_EliteGate")
        self.assertIn("goto_if_unset FLAG_ERYON_QUALIFIED", gate)
        self.assertIn("MSGBOX_YESNO", gate)
        self.assertIn("warp MAP_ERYON_LIGA_ELITE_FOUR, 28, 37", gate)
        exit_script = body(self.script, "EryonLigaElite_EventScript_Exit")
        self.assertIn("MSGBOX_YESNO", exit_script)
        self.assertIn("warp MAP_ERYON_LIGA_RECUPERACAO, 12, 14", exit_script)

    def test_save_flags_and_opponent_ids_are_isolated(self):
        flags = (ROOT / "include/constants/flags.h").read_text(encoding="utf-8")
        opponents = (ROOT / "include/constants/opponents.h").read_text(encoding="utf-8")
        setup = (ROOT / "src/battle_setup.c").read_text(encoding="utf-8")
        parties = (ROOT / "src/data/trainers.party").read_text(encoding="utf-8")
        for i, trainer in enumerate(TRAINERS):
            self.assertIn(f"#define {trainer} {875+i}", opponents)
            self.assertEqual(parties.count(f"=== {trainer} ==="), 1)
        self.assertGreaterEqual(
            int(re.search(r"(?m)^#define TRAINERS_COUNT_EMERALD\s+(\d+)", opponents).group(1)),
            880,
        )
        for fl, value in zip(FLAGS, (0x4D, 0x4E, 0x4F, 0x54, 0x55)):
            self.assertIn(f"#define {fl} 0x{value:X}", flags)
        self.assertIn("#define FLAG_ERYON_CHAMPION_CROWNED 0x68", flags)
        self.assertIn("if (trainerId >= TRAINER_ERYON_ELITE_1", setup)
        self.assertIn("return FLAG_ERYON_ELITE_TRAINER_4_DEFEATED;", setup)
        self.assertIn("return FLAG_ERYON_CHAMPION_TRAINER_DEFEATED;", setup)

    def test_story_reaches_league_capital(self):
        city = CITY.read_text(encoding="utf-8")
        self.assertIn("goto_if_set FLAG_ERYON_CHAMPION_CROWNED, "
                      "EryonCidadeLiga_EventScript_ReporterChampion", city)
        self.assertIn("goto_if_set FLAG_ERYON_CHAMPION_CROWNED, "
                      "EryonCidadeLiga_EventScript_FanChampion", city)
        self.assertIn("EryonCidadeLiga_EventScript_ReporterChampion::", city)


if __name__ == "__main__":
    unittest.main()
