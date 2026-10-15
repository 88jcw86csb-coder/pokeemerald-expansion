"""Ensure Eryon's ROM build and CI never silently skip existing regressions.

This is a source contract: it does not launch the ARM compiler or emulator.
"""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / "tools/build_eryon.sh"
CI = ROOT / ".github/workflows/build.yml"


class EryonBuildContract(unittest.TestCase):
    def test_build_covers_all_regressions_by_discovery(self):
        script = BUILD.read_text(encoding="utf-8")
        self.assertIn("python3 -m unittest discover -s tools -p 'test_eryon_*.py' -v", script)
        self.assertIn("python3 -m unittest discover -s tests -p 'test_eryon_*.py' -v", script)
        self.assertGreaterEqual(len(list((ROOT / "tests").glob("test_eryon_*.py"))), 24)
        self.assertGreaterEqual(len(list((ROOT / "tools").glob("test_eryon_*.py"))), 5)

    def test_ci_independently_runs_entire_suite(self):
        content = CI.read_text(encoding="utf-8")
        validation = content.split("  eryon-validation:", 1)[1].split(
            "  build-firered:", 1)[0]
        self.assertIn("python3 -m compileall -q tools tests", validation)
        for folder in ("tools", "tests"):
            self.assertIn(
                f"python3 -m unittest discover -s {folder} -p 'test_eryon_*.py' -v",
                validation,
            )

    def test_static_audits_precede_new_build(self):
        script = BUILD.read_text(encoding="utf-8")
        compile_at = script.index('echo "== Eryon: compiling GBA ROM =="')
        for command in (
            "python3 tools/eryon_validate.py",
            "python3 tools/eryon_layout_audit.py",
            "python3 tools/eryon_world_audit.py",
        ):
            self.assertLess(script.index(command), compile_at)

    def test_build_never_accepts_a_stale_rom_and_checks_new_binary(self):
        source = BUILD.read_text(encoding="utf-8")
        self.assertIn("rm -f pokeeryon.gba", source)
        self.assertLess(source.index("rm -f pokeeryon.gba"),
                        source.index('make -j"$jobs" -O all'))
        self.assertLess(source.index('make -j"$jobs" -O all'),
                        source.index("python3 tools/eryon_rom_smoke.py pokeeryon.gba"))
        self.assertIn("sha256sum pokeeryon.gba", source)


if __name__ == "__main__":
    unittest.main()
