#!/usr/bin/env python3
"""Static regression checks for the optional valley-to-Lunaris study.

Passing does not prove pixel art, movement, item pickup or save state in Delta.
"""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVENTS = (
    ("Eryon_ValeDosEcos", "bg_events", "EryonEcoVale_EventScript_PulseRecorder", 32, 22),
    ("Eryon_TrilhaLunar", "bg_events", "EryonLunar_EventScript_StarCalibration", 34, 22),
    ("Eryon_Lunaris", "object_events", "EryonLunaris_EventScript_ObservatoryScholar", 45, 28),
)


class EchoStudyTests(unittest.TestCase):
    def test_persistent_flags_do_not_overlap_existing_reserved_names(self):
        source = (ROOT / "include/constants/flags.h").read_text(encoding="utf-8")
        for flag, address in (
            ("FLAG_ERYON_ECHO_TRACE_RECORDED", "0x4A2"),
            ("FLAG_ERYON_ECHO_ARCHIVE_REWARD_CLAIMED", "0x4A3"),
        ):
            self.assertEqual(len(re.findall(
                rf"(?m)^#define\s+{flag}\s+{address}\b", source)), 1)
            self.assertNotIn(f"#define FLAG_UNUSED_{address}", source)

    def test_landmarks_have_usable_positions_and_unique_scripts(self):
        data = json.loads((ROOT / "data/layouts/layouts.json").read_text(encoding="utf-8"))
        layouts = {x["id"]: x for x in data["layouts"]}
        for name, field, symbol, x, y in EVENTS:
            with self.subTest(map=name):
                folder = ROOT / "data/maps" / name
                map_info = json.loads((folder / "map.json").read_text(encoding="utf-8"))
                found = [e for e in map_info[field] if e["script"] == symbol]
                self.assertEqual(len(found), 1)
                self.assertEqual((found[0]["x"], found[0]["y"]), (x, y))
                scripts = (folder / "scripts.inc").read_text(encoding="utf-8")
                self.assertEqual(scripts.count(symbol + "::"), 1)
                layout = layouts[map_info["layout"]]
                raw = (ROOT / layout["blockdata_filepath"]).read_bytes()
                offset = 2 * (y * layout["width"] + x)
                self.assertEqual(int.from_bytes(raw[offset:offset + 2], "little") & 0xC00, 0)

    def test_recording_is_optional_and_can_only_be_saved_after_serra_clue(self):
        text = (ROOT / "data/maps/Eryon_ValeDosEcos/scripts.inc").read_text(encoding="utf-8")
        section = text.split("EryonEcoVale_EventScript_PulseRecorder::", 1)[1]
        section = section.split("EryonEcoVale_EventScript_PulseRecorderDone::", 1)[0]
        self.assertIn("goto_if_set FLAG_ERYON_ECHO_TRACE_RECORDED", section)
        self.assertIn("goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1", section)
        offer = section.split("EryonEcoVale_EventScript_PulseRecorderOffer::", 1)[1]
        self.assertLess(offer.index("goto_if_eq VAR_RESULT, NO"),
                        offer.index("setflag FLAG_ERYON_ECHO_TRACE_RECORDED"))
        self.assertIn("MSGBOX_YESNO", offer)

    def test_archive_reward_is_retryable_and_not_duplicate(self):
        text = (ROOT / "data/maps/Eryon_AldeiaDosEcos/scripts.inc").read_text(encoding="utf-8")
        archivist = text.split("EryonAldeia_EventScript_Archivist::", 1)[1]
        archivist = archivist.split("EryonAldeia_EventScript_ArchivistClue::", 1)[0]
        self.assertLess(
            archivist.index("FLAG_ERYON_ECHO_ARCHIVE_REWARD_CLAIMED"),
            archivist.index("FLAG_ERYON_ECHO_TRACE_RECORDED"))
        reward = text.split("EryonAldeia_EventScript_ArchivistReceiveTrace::", 1)[1]
        reward = reward.split("EryonAldeia_EventScript_ArchivistBagFull::", 1)[0]
        self.assertIn("giveitem ITEM_STAR_PIECE", reward)
        self.assertLess(reward.index("giveitem ITEM_STAR_PIECE"),
                        reward.index("goto_if_eq VAR_RESULT, FALSE"))
        self.assertLess(reward.index("goto_if_eq VAR_RESULT, FALSE"),
                        reward.index("setflag FLAG_ERYON_ECHO_ARCHIVE_REWARD_CLAIMED"))

    def test_lunar_route_city_react_without_modifying_seventh_gym(self):
        route = (ROOT / "data/maps/Eryon_TrilhaLunar/scripts.inc").read_text(encoding="utf-8")
        city = (ROOT / "data/maps/Eryon_Lunaris/scripts.inc").read_text(encoding="utf-8")
        self.assertIn("EryonLunar_EventScript_StarCalibration::", route)
        self.assertIn("FLAG_ERYON_ECHO_ARCHIVE_REWARD_CLAIMED", route)
        scholar = city.split("EryonLunaris_EventScript_ObservatoryScholar::", 1)[1]
        self.assertLess(scholar.index("FLAG_BADGE07_GET"),
                        scholar.index("FLAG_ERYON_ECHO_ARCHIVE_REWARD_CLAIMED"))
        self.assertIn("FLAG_ERYON_ECHO_TRACE_RECORDED", scholar)
        gym = city.split("EryonLunaris_EventScript_GymLeader::", 1)[1]
        gym = gym.split("EryonLunaris_Text_GymOffer:", 1)[0]
        self.assertIn("trainerbattle_single TRAINER_ERYON_GYM_LUNARIS", gym)
        self.assertIn("setflag FLAG_BADGE07_GET", gym)
        drakonia = (ROOT / "data/maps/Eryon_Drakonia/scripts.inc").read_text(encoding="utf-8")
        researcher = drakonia.split("EryonDrakonia_EventScript_RuneResearcher::", 1)[1]
        researcher = researcher.split("EryonDrakonia_EventScript_EclipseAgent::", 1)[0]
        self.assertIn("FLAG_ERYON_ECHO_ARCHIVE_REWARD_CLAIMED", researcher)
        self.assertLess(researcher.index("FLAG_ERYON_STAR_GROTTO_RELAY_DISABLED"),
                        researcher.index("FLAG_ERYON_ECHO_ARCHIVE_REWARD_CLAIMED"))
        self.assertIn("EryonDrakonia_EventScript_ResearcherEchoArchive::", drakonia)


if __name__ == "__main__":
    unittest.main()
