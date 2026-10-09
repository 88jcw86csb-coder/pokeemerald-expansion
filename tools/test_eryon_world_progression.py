#!/usr/bin/env python3
"""Regression checks for Eryon's proposed regional progression."""
import unittest
from eryon_world_progression import STAGES, GYMS, render, validate, ROOT


class WorldProgressionTests(unittest.TestCase):
    def test_interleaved_journey(self):
        self.assertTrue(validate())
        kinds = [kind for _, kind in STAGES]
        self.assertEqual(kinds.count("gym"), 8)
        self.assertGreaterEqual(kinds.count("village"), 7)
        self.assertGreaterEqual(kinds.count("route"), 9)
        self.assertEqual([name for name, kind in STAGES if kind == "gym"], GYMS)
        self.assertEqual(STAGES[2][0], "bosque_de_lumina")
        self.assertEqual(len(STAGES), 37)
        names = [name for name, _ in STAGES]
        self.assertEqual(names[names.index("aldeia_dos_ecos")+1], "trilha_lunar")
        self.assertEqual(names[names.index("trilha_lunar")+1], "lunaris")
        self.assertEqual(names[names.index("vila_das_aguas")+1], "trilha_do_oasis")
        self.assertEqual(names[names.index("trilha_do_oasis")+1], "deserto_de_solaris")
        self.assertEqual(names[names.index("drakonia")+1], "gruta_das_estrelas")
        self.assertEqual(names[names.index("gruta_das_estrelas")+1], "caminho_da_liga")
        for i in range(len(kinds) - 1):
            self.assertFalse(kinds[i] == kinds[i + 1] == "gym")

    def test_document_is_current(self):
        path = ROOT / "docs/eryon/progressao_regional.md"
        self.assertEqual(path.read_text(encoding="utf-8"), render())


if __name__ == "__main__":
    unittest.main()
