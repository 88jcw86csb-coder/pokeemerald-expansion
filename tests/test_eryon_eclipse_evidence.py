"""Static checks for the Eryon Eclipse evidence quest.

Run from the repository root:
python3 -m unittest discover -s tests -p 'test_eryon_eclipse_evidence.py'

Structural checks only; gameplay and save persistence require emulator tests.
"""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
FLAGS = ROOT / "include/constants/flags.h"
TRAIL = ROOT / "data/maps/Eryon_TrilhaDosDragoes/scripts.inc"
CITY = ROOT / "data/maps/Eryon_CidadeDaLiga/scripts.inc"
DRAKONIA = ROOT / "data/maps/Eryon_Drakonia/scripts.inc"
LUNARIS = ROOT / "data/maps/Eryon_Lunaris/scripts.inc"
PICO = ROOT / "data/maps/Eryon_VilaDoPico/scripts.inc"
LEAGUE_ROAD = ROOT / "data/maps/Eryon_CaminhoDaLiga/scripts.inc"
GROTTO = ROOT / "data/maps/Eryon_GrutaDasEstrelas/scripts.inc"


class EclipseEvidenceQuest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.flags = FLAGS.read_text(encoding="utf-8")
        cls.trail = TRAIL.read_text(encoding="utf-8")
        cls.city = CITY.read_text(encoding="utf-8")
        cls.drakonia = DRAKONIA.read_text(encoding="utf-8")
        cls.lunaris = LUNARIS.read_text(encoding="utf-8")
        cls.pico = PICO.read_text(encoding="utf-8")
        cls.league_road = LEAGUE_ROAD.read_text(encoding="utf-8")
        cls.grotto = GROTTO.read_text(encoding="utf-8")

    def test_persistent_flags_have_distinct_ids(self):
        self.assertIn("#define FLAG_ERYON_DRAGON_TRAIL_MANIFEST_READ 0x3D", self.flags)
        self.assertIn("#define FLAG_ERYON_ECLIPSE_EVIDENCE_REPORTED 0x3E", self.flags)

    def test_manifest_requires_star_chart_and_sets_flag(self):
        self.assertIn(
            "goto_if_set FLAG_ERYON_STAR_CHART_READ, EryonDragoes_EventScript_SupplyCrateChart",
            self.trail,
        )
        self.assertIn("setflag FLAG_ERYON_DRAGON_TRAIL_MANIFEST_READ", self.trail)

    def test_evidence_cannot_be_reported_without_manifest(self):
        self.assertIn(
            "goto_if_set FLAG_ERYON_DRAGON_TRAIL_MANIFEST_READ, "
            "EryonCidadeLiga_EventScript_InvestigatorManifest",
            self.city,
        )

    def test_reporting_once_changes_future_dialogue(self):
        self.assertIn("setflag FLAG_ERYON_ECLIPSE_EVIDENCE_REPORTED", self.city)
        self.assertIn(
            "goto_if_set FLAG_ERYON_ECLIPSE_EVIDENCE_REPORTED, "
            "EryonCidadeLiga_EventScript_InvestigatorEvidenceFiled",
            self.city,
        )
        self.assertIn("EryonCidadeLiga_EventScript_InvestigatorEvidenceFiled::", self.city)

    def test_evidence_has_consequences_in_both_cities(self):
        flag = "FLAG_ERYON_ECLIPSE_EVIDENCE_REPORTED"
        self.assertIn(
            f"goto_if_set {flag}, EryonCidadeLiga_EventScript_ReporterEvidence",
            self.city,
        )
        self.assertIn("EryonCidadeLiga_EventScript_ReporterEvidence::", self.city)
        self.assertIn(
            f"goto_if_set {flag}, EryonDrakonia_EventScript_SageEvidenceReported",
            self.drakonia,
        )
        self.assertIn("EryonDrakonia_EventScript_SageEvidenceReported::", self.drakonia)

    def test_lunaris_reacts_to_manifest_and_report(self):
        self.assertIn(
            "goto_if_set FLAG_ERYON_DRAGON_TRAIL_MANIFEST_READ, "
            "EryonLunaris_EventScript_AnalystManifest", self.lunaris)
        self.assertIn(
            "goto_if_set FLAG_ERYON_ECLIPSE_EVIDENCE_REPORTED, "
            "EryonLunaris_EventScript_AnalystAfterReport", self.lunaris)
        self.assertIn("EryonLunaris_EventScript_GeneratorManifest::", self.lunaris)

    def test_village_and_league_road_react_to_evidence(self):
        self.assertIn(
            "goto_if_set FLAG_ERYON_ECLIPSE_EVIDENCE_REPORTED, "
            "EryonPico_EventScript_RadioReport", self.pico)
        self.assertIn(
            "goto_if_set FLAG_ERYON_DRAGON_TRAIL_MANIFEST_READ, "
            "EryonPico_EventScript_RadioManifest", self.pico)
        self.assertIn(
            "goto_if_set FLAG_ERYON_ECLIPSE_EVIDENCE_REPORTED, "
            "EryonLigaCaminho_EventScript_ObserverReported", self.league_road)

    def test_star_grotto_reacts_to_evidence(self):
        self.assertIn(
            "goto_if_set FLAG_ERYON_DRAGON_TRAIL_MANIFEST_READ, "
            "EryonEstrelas_EventScript_ScoutManifest", self.grotto)
        self.assertIn(
            "goto_if_set FLAG_ERYON_ECLIPSE_EVIDENCE_REPORTED, "
            "EryonEstrelas_EventScript_ScoutAfterReport", self.grotto)
        self.assertIn(
            "goto_if_set FLAG_ERYON_ECLIPSE_EVIDENCE_REPORTED, "
            "EryonEstrelas_EventScript_ArchivistReported", self.grotto)


if __name__ == "__main__":
    unittest.main()
