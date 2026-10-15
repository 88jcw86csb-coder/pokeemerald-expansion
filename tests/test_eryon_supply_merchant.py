"""Guard Eryon's first purchase point without changing battles or story.

This is a source/terrain check, NOT a runtime purchase or emulator test.
"""
import json
from pathlib import Path
import struct
import unittest

ROOT = Path(__file__).resolve().parents[1]
NAME = "Eryon_Verdelume"
NPC_SCRIPT = "EryonVerdelume_EventScript_SupplyMerchant"


class EryonSupplyMerchantTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        folder = ROOT / "data/maps" / NAME
        cls.info = json.loads((folder / "map.json").read_text(encoding="utf-8"))
        cls.script = (folder / "scripts.inc").read_text(encoding="utf-8")
        cls.layout = next(
            entry for entry in json.loads(
                (ROOT / "data/layouts/layouts.json").read_text(encoding="utf-8")
            )["layouts"] if entry["id"] == cls.info["layout"]
        )

    def test_merchant_is_unique_and_on_safe_walkable_ground(self):
        events = [e for e in self.info["object_events"] if e["script"] == NPC_SCRIPT]
        self.assertEqual(len(events), 1)
        self.assertEqual((events[0]["x"], events[0]["y"]), (25, 19))
        self.assertEqual(events[0]["flag"], "0")
        occupied = [
            (e["x"], e["y"]) for group in
            ("object_events", "warp_events", "bg_events", "coord_events")
            for e in self.info[group]
        ]
        self.assertEqual(len(occupied), len(set(occupied)))
        width, height = self.layout["width"], self.layout["height"]
        raw = (ROOT / self.layout["blockdata_filepath"]).read_bytes()
        self.assertEqual(len(raw), width * height * 2)
        blocks = struct.unpack(f"<{width * height}H", raw)
        for x, y in ((25, 19), (25, 18), (25, 20), (24, 19), (26, 19)):
            self.assertEqual(blocks[y * width + x] & 0x0C00, 0)

    def test_badge_scaled_inventory_and_shop_commands(self):
        source = self.script
        self.assertEqual(source.count(NPC_SCRIPT + "::"), 1)
        merchant = source.split(NPC_SCRIPT + "::", 1)[1]
        self.assertIn("goto_if_set FLAG_BADGE03_GET", merchant)
        self.assertIn("goto_if_set FLAG_BADGE06_GET", merchant)
        for tier in ("Basic", "Expanded", "Advanced"):
            name = "EryonVerdelume_Pokemart_" + tier
            self.assertIn("pokemart " + name, merchant)
            self.assertEqual(source.count(name + ":"), 1)
            stock = source.split(name + ":", 1)[1].split("pokemartlistend", 1)[0]
            self.assertIn("ITEM_POKE_BALL", stock)
        self.assertIn("ITEM_ULTRA_BALL", merchant)
        self.assertIn("ITEM_HYPER_POTION", merchant)
        self.assertNotIn("clearflag FLAG_BADGE", merchant)
        self.assertNotIn("setflag FLAG_BADGE", merchant)


if __name__ == "__main__":
    unittest.main()
