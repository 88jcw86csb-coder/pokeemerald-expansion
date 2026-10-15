#!/usr/bin/env bash
# Build and statically validate the Eryon GBA ROM from the repository root.
# Usage: bash tools/build_eryon.sh
# Requires: Python 3, make, arm-none-eabi toolchain and dependencies in INSTALL.md.
set -Eeuo pipefail
cd "$(dirname "$0")/.."

if [[ ! -f Makefile || ! -f tools/eryon_rom_smoke.py ]]; then
  echo "ERROR: run this script from an Eryon source checkout" >&2
  exit 2
fi

echo "== Eryon: checking Python validator/test syntax =="
python3 -m py_compile tools/eryon_layout_audit.py tools/eryon_validate.py tools/test_eryon_event_flow.py tools/test_eryon_opening_terrain.py tools/test_eryon_layout_audit.py tools/test_eryon_species.py tools/test_eryon_wild_and_river.py tools/test_eryon_echo_study.py tools/test_eryon_rom_smoke.py tools/eryon_rom_smoke.py

echo "== Eryon: regenerate registered map binaries from authoritative terrain plans =="
python3 tools/build_eryon_map_bins.py --wall 0x3c01 --path 0x3001 --meadow 0x3002 --stone 0x3003 --preview-unregistered

echo "== Eryon: check Kalos wildlife encounters and new oasis passages =="
python3 -m unittest discover -s tests -p 'test_eryon_kalos_encounters.py' -v

echo "== Eryon: opening data validation =="
python3 tools/eryon_validate.py
echo "== Eryon: binary terrain and warp tile audit == "
python3 tools/eryon_layout_audit.py
echo "== Eryon: terrain collision audit tests =="
python3 -m unittest discover -s tools -p 'test_eryon_layout_audit.py' -v

echo "== Eryon: opening terrain and exits == "
python3 -m unittest discover -s tools -p 'test_eryon_opening_terrain.py' -v
echo "== Eryon: species tests =="
python3 -m unittest discover -s tools -p 'test_eryon_species.py' -v
echo "== Eryon: wild route habitats and Eclipse river quest =="
python3 -m unittest discover -s tools -p 'test_eryon_wild_and_river.py' -v
echo "== Eryon: Echo Valley archive and Lunaris investigation =="
python3 -m unittest discover -s tools -p 'test_eryon_echo_study.py' -v
echo "== Eryon: event flow tests =="
python3 -m unittest discover -s tools -p 'test_eryon_event_flow.py' -v
echo "== Eryon: Elite Four tournament integrity =="
python3 -m unittest discover -s tests -p 'test_eryon_elite_four.py' -v

echo "== Eryon: Riolu level 35 and no trade/friendship evolution through Kalos =="
python3 -m unittest discover -s tests -p 'test_eryon_level_evolutions.py' -v

echo "== Eryon: Eight Gym level and EXP balance integrity =="
python3 -m unittest discover -s tests -p 'test_eryon_gym_balance.py' -v

echo "== Eryon: Mist lookout and Glacial route progression =="
python3 -m unittest discover -s tests -p 'test_eryon_mist_watch.py' -v

echo "== Eryon: Balanced Glacial Eclipse battle and Frostheim consequence =="
python3 -m unittest discover -s tests -p 'test_eryon_glacial_eclipse.py' -v

echo "== Eryon: Sierra rocky terrain and Eclipse crystal puzzle =="
python3 -m unittest discover -s tests -p 'test_eryon_serra_resonance.py' -v

echo "== Eryon: Crystal Serra sentry and multi-stage Eclipse investigation =="
python3 -m unittest discover -s tests -p 'test_eryon_serra_sentry.py' -v

echo "== Eryon: ROM smoke validator unit tests =="
python3 -m unittest discover -s tools -p 'test_eryon_rom_smoke.py' -v

echo "== Eryon: compiling GBA ROM =="
jobs=2
if command -v nproc >/dev/null 2>&1; then
  jobs="$(nproc)"
fi
mkdir -p build
# Never accept a leftover ROM from an earlier build as evidence of this run.
rm -f pokeeryon.gba
set -o pipefail
make -j"$jobs" -O all 2>&1 | tee build/eryon-build.log

echo "== Eryon: validating ROM header and payload =="
python3 tools/eryon_rom_smoke.py pokeeryon.gba
sha256sum pokeeryon.gba | tee build/eryon-rom.sha256
echo "PASS: build and static checks complete."
echo "NOTE: this is NOT a gameplay/emulator test; test save/load, map traversal and battles separately."
