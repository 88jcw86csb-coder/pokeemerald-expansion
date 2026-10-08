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

    def test_no_duplicate_labels(self):
        for name in MAPS:
            script = (ROOT / "data/maps" / name / "scripts.inc").read_text()
            labels = LABEL.findall(script)
            with self.subTest(map=name):
                self.assertEqual(len(labels), len(set(labels)))


if __name__ == "__main__":
    unittest.main()
