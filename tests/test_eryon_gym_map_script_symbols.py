"""Prevent missing map-script symbol linker errors for eight gym interiors."""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class EryonGymMapScriptSymbols(unittest.TestCase):
    def test_registered_interiors_export_exact_engine_map_script_label(self):
        groups=json.loads((ROOT/"data/maps/map_groups.json").read_text())
        interiors=groups["gMapGroup_GymEryon"]
        self.assertEqual(len(interiors),8)
        event_sources=(ROOT/"data/event_scripts.s").read_text()
        for name in interiors:
            with self.subTest(map=name):
                mapinfo=json.loads((ROOT/"data/maps"/name/"map.json").read_text())
                self.assertEqual(mapinfo["name"],name)
                script=(ROOT/"data/maps"/name/"scripts.inc").read_text()
                self.assertRegex(script,r"(?m)^"+re.escape(name)+r"_MapScripts::$")
                self.assertIn(f'data/maps/{name}/scripts.inc',event_sources)
                self.assertTrue((ROOT/"data/layouts"/name).exists() or
                                (ROOT/"tools/eryon_gym_interiors.py").is_file())
    def test_build_and_terrain_validation_generate_gym_binaries(self):
        build=(ROOT/"tools/build_eryon.sh").read_text()
        workflow=(ROOT/".github/workflows/build.yml").read_text()
        terrain=(ROOT/".github/workflows/eryon-terrain.yml").read_text()
        for name,source in (("build",build),("CI",workflow),("terrain",terrain)):
            with self.subTest(entry=name):
                self.assertIn("python3 tools/eryon_gym_interiors.py",source)

if __name__=="__main__":
    unittest.main()
