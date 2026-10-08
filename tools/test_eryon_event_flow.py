#!/usr/bin/env python3
"""Static tests for Eryon's scripted opening; does not emulate the game."""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAPS = ("Eryon_VilaAurora", "Eryon_Rota01", "Eryon_BosqueDeLumina",
        "Eryon_Rota02", "Eryon_Verdelume")
LABEL = re.compile(r"(?m)^([A-Za-z][A-Za-z0-9_]*)::?\s*$")
JUMP = re.compile(r"^\s*(?:goto|goto_if_eq|goto_if_ne|goto_if_ge|goto_if_le|goto_if_gt|goto_if_lt)\s+(.+)$")


class EryonEventFlowTests(unittest.TestCase):
    def test_jump_destinations_exist(self):
        for name in MAPS:
            script = (ROOT / "data/maps" / name / "scripts.inc").read_text()
            labels = set(LABEL.findall(script))
            for lineno, line in enumerate(script.splitlines(), 1):
                match = JUMP.match(line)
                if not match:
                    continue
                destination = match.group(1).split(",")[-1].strip().split()[0]
                with self.subTest(map=name, line=lineno, target=destination):
                    self.assertIn(destination, labels)

    def test_dialogue_has_no_doubled_control_escapes(self):
        for name in MAPS:
            script = (ROOT / "data/maps" / name / "scripts.inc").read_text()
            for escape in (r"\\\\n", r"\\\\p", r"\\\\l"):
                with self.subTest(map=name, escape=escape):
                    self.assertNotIn(escape, script)

    def test_kael_battle_is_reachable_after_briefing(self):
        script = (ROOT / "data/maps/Eryon_Verdelume/scripts.inc").read_text()
        self.assertIn("goto_if_ge VAR_ERYON_KAEL_BRIEFED, 1, EryonVerdelume_EventScript_KaelFollowup", script)
        followup = script.split("EryonVerdelume_EventScript_KaelFollowup::", 1)[1].split("EryonVerdelume_EventScript_KaelVictory::", 1)[0]
        self.assertIn("trainerbattle_single TRAINER_ERYON_KAEL", followup)
        self.assertIn("EryonVerdelume_EventScript_KaelVictory", followup)
        victory = script.split("EryonVerdelume_EventScript_KaelVictory::", 1)[1].split("EryonVerdelume_EventScript_KaelAfterBattle::", 1)[0]
        self.assertIn("setvar VAR_ERYON_KAEL_DEFEATED, 1", victory)

    def test_eryon_progress_vars_are_unique_and_defined(self):
        vars_text = (ROOT / "include/constants/vars.h").read_text()
        definitions = re.findall(r"(?m)^#define\\s+(VAR_[A-Z0-9_]+)\\s+(0x[0-9A-Fa-f]+)", vars_text)
        by_value = {}
        for name, value in definitions:
            if name.startswith("VAR_ERYON_"):
                with self.subTest(name=name):
                    self.assertNotIn(value, by_value, f"{name} shares {value} with {by_value.get(value)}")
                by_value[value] = name
        scripts = "\\n".join((ROOT / "data/maps" / name / "scripts.inc").read_text() for name in MAPS)
        for name in set(re.findall(r"VAR_ERYON_[A-Z0-9_]+", scripts)):
            with self.subTest(name=name):
                self.assertIn(name, dict(definitions), f"Undefined Eryon variable: {name}")

    def test_no_duplicate_labels(self):
        for name in MAPS:
            script = (ROOT / "data/maps" / name / "scripts.inc").read_text()
            labels = LABEL.findall(script)
            with self.subTest(map=name):
                self.assertEqual(len(labels), len(set(labels)))


if __name__ == "__main__":
    unittest.main()
