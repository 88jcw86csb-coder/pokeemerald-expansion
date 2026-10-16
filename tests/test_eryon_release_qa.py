"""Check automatic localization debt reporting and guard translated UI."""
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"tools"))
from eryon_release_qa import collect

class EryonLanguageIntegrity(unittest.TestCase):
    def test_all_map_scripts_counted_in_language_inventory(self):
        report=collect()
        self.assertEqual(report["registered_eryon_maps"],42)
        self.assertEqual(report["gym_maps"],8)
        self.assertEqual(report["text_files_scanned"],53)
        self.assertGreater(report["strings_scanned"],100)

    def test_translated_critical_menus_and_professor(self):
        m=(ROOT/"src/main_menu.c").read_text(encoding="utf-8")
        t=(ROOT/"src/strings.c").read_text(encoding="utf-8")
        for value in ("NOVO JOGO","CONTINUAR","OPCOES","Save corrompido.","Bateria interna esgotada."):
            self.assertIn(value,m)
        for value in ("SALVANDO...","HALL DA FAMA","Descartar quantos","VOAR para onde?"):
            self.assertIn(value,t)
        self.assertIn("Meu nome e ELYA",(ROOT/"data/text/birch_speech.inc").read_text(encoding="utf-8"))

    def test_report_avoids_false_full_localization_claim(self):
        report=collect()
        self.assertEqual(report["check"],"advisory_not_fully_translated")
        self.assertEqual(report["translation_status"],"INCOMPLETE_WHILE_ENGLISH_TEXT_REMAINS")

if __name__=="__main__":unittest.main()
