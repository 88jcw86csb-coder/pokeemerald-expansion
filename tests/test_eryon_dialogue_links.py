"""Validate event links and dialogue safety across every registered Eryon map.

This is static source validation. It does NOT check text pixel widths,
Portuguese grammar, message timing, or branching behavior inside an emulator.
"""
import json
from collections import Counter
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
LABEL = re.compile(r"(?m)^([A-Za-z_][A-Za-z_0-9]*)::?\s*$")
STRING = re.compile(r'^\s*\.string\s+"((?:[^"\\]|\\.)*)"\s*$')
# Character count is a conservative heuristic, not exact proportional-font
# pixel width; all Eryon line segments should leave breathing room on GBA.
MAX_VISIBLE_CHARS = 35


def registered_maps():
    groups = json.loads((ROOT / "data/maps/map_groups.json").read_text(
        encoding="utf-8"))
    region = groups["gMapGroup_Eryon"]
    gyms = groups["gMapGroup_GymEryon"]
    if len(region) != 42 or len(gyms) != 8:
        raise ValueError("Unexpected Eryon world/gym inventory")
    names = region + gyms
    if len(set(names)) != 50:
        raise ValueError("Duplicate Eryon map names")
    return names


def visible_segments(line):
    # Remove GBA dialogue newline/page directives and final text terminator.
    # Count characters between the directives, not the escape sequences.
    return re.split(r"\\[npNl]|\$", line)


class EryonDialogueLinksTests(unittest.TestCase):
    def test_all_50_registered_maps_have_valid_event_script_labels(self):
        for name in registered_maps():
            with self.subTest(map=name):
                folder = ROOT / "data/maps" / name
                meta = json.loads((folder / "map.json").read_text(
                    encoding="utf-8"))
                source = (folder / "scripts.inc").read_text(
                    encoding="utf-8")
                labels = LABEL.findall(source)
                duplicates = [
                    key for key, count in Counter(labels).items()
                    if count > 1
                ]
                self.assertEqual(
                    duplicates, [], f"{name}: duplicate script labels")
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

    def test_all_50_maps_have_terminated_well_formed_dialogues(self):
        for name in registered_maps():
            with self.subTest(map=name):
                source = (ROOT / "data/maps" / name /
                          "scripts.inc").read_text(encoding="utf-8")
                open_block = False
                blocks = 0
                for number, line in enumerate(source.splitlines(), 1):
                    if line.lstrip().startswith(".string"):
                        parsed = STRING.fullmatch(line)
                        self.assertIsNotNone(
                            parsed, f"{name}:{number} malformed .string")
                        payload = parsed.group(1)
                        if not open_block:
                            blocks += 1
                        # Catch accidental lines too long for GBA dialogue.
                        for segment in visible_segments(payload):
                            self.assertLessEqual(
                                len(segment), MAX_VISIBLE_CHARS,
                                f"{name}:{number} text line too long: {segment!r}",
                            )
                        open_block = "$" not in payload
                    elif open_block and line.strip() and not line.lstrip().startswith("//"):
                        self.fail(f"{name}:{number} previous text missing '$'")
                self.assertFalse(open_block, f"{name}: text unfinished at EOF")
                self.assertGreater(blocks, 0, f"{name}: no dialogue blocks")


if __name__ == "__main__":
    unittest.main()
