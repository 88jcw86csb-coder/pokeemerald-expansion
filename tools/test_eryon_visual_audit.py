"""Sanity checks for Eryon's visual-identity debt inventory (not final art approval)."""
import unittest
from eryon_visual_audit import audit


class VisualInventoryTests(unittest.TestCase):
    def test_inventory_covers_registered_eryon_maps(self):
        result = audit()
        self.assertGreaterEqual(result["regional_maps"], 42)
        self.assertEqual(result["regional_maps"], result["regional_layouts"])
        self.assertEqual(len(result["maps"]), result["regional_maps"])
        self.assertTrue(result["trainer_portraits"])

    def test_terrain_metrics_are_well_formed(self):
        for item in audit()["maps"]:
            with self.subTest(map=item["name"]):
                self.assertGreater(item["width"], 0)
                self.assertGreater(item["height"], 0)
                self.assertGreater(item["distinct_metatiles"], 0)
                self.assertGreater(item["dominant_tile_fraction"], 0)
                self.assertLessEqual(item["dominant_tile_fraction"], 1)

    def test_report_explicitly_disclaims_art_approval(self):
        self.assertEqual(audit()["purpose"],
                         "inventory_only_not_originality_certification")


if __name__ == "__main__":
    unittest.main()
