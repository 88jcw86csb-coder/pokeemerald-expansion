"""Prevent recurrence of Eryon blocked events, lost roads, or broken warps.

This is a collision-bit structural test only, not a substitute for Delta.
"""
import unittest

from tools.eryon_map_traversal_audit import inspect


class EryonWorldTraversalContract(unittest.TestCase):
    def test_all_registered_maps_and_region_edges_have_reachable_events(self):
        names, results, errors = inspect()
        self.assertEqual(len(names), 42)
        self.assertEqual(len(results), 42)
        self.assertFalse(errors, "\n".join(errors))

    def test_league_and_echo_village_are_reachable(self):
        _, results, errors = inspect()
        self.assertFalse(errors, "\n".join(errors))
        for name in ("Eryon_AldeiaDosEcos", "Eryon_ValeDosEcos",
                     "Eryon_CaminhoDaLiga", "Eryon_CidadeDaLiga",
                     "Eryon_LigaClassificatoria", "Eryon_LigaEliteFour"):
            with self.subTest(map=name):
                self.assertIn(name, results)
                self.assertGreater(results[name][2], 50)


    def test_registered_terrain_matches_authoritative_plans_byte_for_byte(self):
        from pathlib import Path
        import struct

        root = Path(__file__).resolve().parents[1]
        plan_specs = {
            "Eryon_BosqueDeLumina": ("bosque_de_lumina_terrain_plan.txt", 48, 44),
            "Eryon_PassagemRochosa": ("passagem_rochosa_terrain_plan.txt", 48, 44),
            "Eryon_EstradaOriental": ("estrada_oriental_terrain_plan.txt", 48, 44),
            "Eryon_ValeDosVentos": ("vale_dos_ventos_terrain_plan.txt", 48, 44),
            "Eryon_EstradaDosPomares": ("estrada_dos_pomares_terrain_plan.txt", 48, 44),
            "Eryon_ColinasDaNeblina": ("colinas_da_neblina_terrain_plan.txt", 48, 44),
            "Eryon_RotaDasCachoeiras": ("rota_das_cachoeiras_terrain_plan.txt", 48, 44),
            "Eryon_TrilhaDoOasis": ("trilha_do_oasis_terrain_plan.txt", 48, 44),
            "Eryon_DesertoDeSolaris": ("deserto_de_solaris_terrain_plan.txt", 48, 44),
            "Eryon_Rota04": ("rota_04_terrain_plan.txt", 48, 44),
            "Eryon_CaminhoDaLiga": ("caminho_da_liga_terrain_plan.txt", 48, 44),
            "Eryon_CidadeDaLiga": ("liga_eryon_terrain_plan.txt", 96, 72),
        }
        for name, short in (
            ("Eryon_VilaDosPomares", "vila_dos_pomares"),
            ("Eryon_VilaDaNeblina", "vila_da_neblina"),
            ("Eryon_RefugioCristal", "refugio_cristal"),
            ("Eryon_PostoOriental", "posto_oriental"),
            ("Eryon_VilaDasAguas", "vila_das_aguas"),
            ("Eryon_AldeiaDosEcos", "aldeia_dos_ecos"),
        ):
            plan_specs[name] = (f"vilas/{short}_village_plan.txt", 36, 30)
        glyphs = {"#": 0x3C01, ".": 0x3001, ",": 0x3002, ":": 0x3003}
        glyphs.update({c: 0x3001 for c in "GCMHPIL="})
        for name, (plan_name, w, h) in plan_specs.items():
            with self.subTest(map=name):
                plan = root / "docs/eryon" / plan_name
                rows = plan.read_text(encoding="utf-8").splitlines()[4:]
                self.assertEqual(len(rows), h)
                self.assertTrue(all(len(row) == w for row in rows))
                expected = struct.pack(f"<{w*h}H",
                                       *(glyphs[c] for row in rows for c in row))
                actual = (root / "data/layouts" / name / "map.bin").read_bytes()
                self.assertEqual(actual, expected, f"{name} is stale versus {plan_name}")

    def test_echo_valley_barriers_have_collision_bits(self):
        import struct
        from pathlib import Path

        root = Path(__file__).resolve().parents[1]
        raw = (root / "data/layouts/Eryon_ValeDosEcos/map.bin").read_bytes()
        values = struct.unpack("<2112H", raw)
        self.assertNotIn(0x300D, values, "Echo Valley barriers lost collision")
        self.assertIn(0x3C0D, values, "Echo Valley barrier tiles disappeared")


if __name__ == "__main__":
    unittest.main()
