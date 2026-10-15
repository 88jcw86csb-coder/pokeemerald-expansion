"""Guard all registered Eryon NPC/sign/coordinate event script and dialogue links.

This checks assembly source declarations, not text rendering, player choices or
runtime NPC behavior. It is automatically collected by build_eryon.sh.
"""
import json
from collections import Counter
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
LABEL = re.compile(r"(?m)^([A-Za-z_][A-Za-z_0-9]*)::?\s*$")
STRING = re.compile(r'^\s*\.string\s+"(?:[^"\\]|\\.)*"\s*$')


class EryonDialogueLinksTests(unittest.TestCase):
    def test_all_42_registered_maps_have_valid_event_script_labels(self):
        names = json.loads(
            (ROOT / "data/maps/map_groups.json").read_text(encoding="utf-8")
        )["gMapGroup_Eryon"]
        self.assertEqual(len(names), 42)
        self.assertEqual(len(set(names)), 42)
        for name in names:
            with self.subTest(map=name):
                folder = ROOT / "data/maps" / name
                meta = json.loads((folder / "map.json").read_text(encoding="utf-8"))
                source = (folder / "scripts.inc").read_text(encoding="utf-8")
                labels = LABEL.findall(source)
                duplicates = [key for key, count in Counter(labels).items() if count > 1]
                self.assertEqual(duplicates, [], f"{name}: duplicate script labels")
                known = set(labels)
                self.assertEqual(meta["name"], name)
                for kind in ("object_events", "bg_events", "coord_events"):
                    for index, event in enumerate(meta[kind]):
                        label = event.get("script")
                        if label:
                            self.assertIn(
                                label, known,
                                f"{name}: {kind}[{index}] references undefined {label}",
                            )

    def test_map_dialogue_directives_are_syntactically_balanced(self):
        names = json.loads(
            (ROOT / "data/maps/map_groups.json").read_text(encoding="utf-8")
        )["gMapGroup_Eryon"]
        for name in names:
            source = (
                ROOT / "data/maps" / name / "scripts.inc"
            ).read_text(encoding="utf-8")
            for number, line in enumerate(source.splitlines(), 1):
                if line.lstrip().startswith(".string"):
                    with self.subTest(map=name, line=number):
                        self.assertRegex(
                            line.strip(), STRING,
                            f"{name}:{number} malformed .string declaration",
                        )


if __name__ == "__main__":
    unittest.main()
