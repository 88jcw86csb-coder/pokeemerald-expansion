#!/usr/bin/env python3
"""Check that every regional map concept has a source plan."""
import unittest
from eryon_world_audit import audit


class WorldAuditTests(unittest.TestCase):
    def test_every_planned_concept_exists(self):
        self.assertEqual(audit(), [])


if __name__=="__main__":
    unittest.main()
