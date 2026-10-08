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

echo "== Eryon: opening data validation =="
python3 tools/eryon_validate.py

echo "== Eryon: species tests =="
python3 -m unittest discover -s tools -p 'test_eryon_species.py' -v
echo "== Eryon: event flow tests =="
python3 -m unittest discover -s tools -p 'test_eryon_event_flow.py' -v
echo "== Eryon: ROM smoke validator unit tests =="
python3 -m unittest discover -s tools -p 'test_eryon_rom_smoke.py' -v

echo "== Eryon: compiling GBA ROM =="
jobs=2
if command -v nproc >/dev/null 2>&1; then
  jobs="$(nproc)"
fi
mkdir -p build
set -o pipefail
make -j"$jobs" -O all 2>&1 | tee build/eryon-build.log

echo "== Eryon: validating ROM header and payload =="
python3 tools/eryon_rom_smoke.py pokeeryon.gba
echo "PASS: build and static checks complete."
echo "NOTE: this is NOT a gameplay/emulator test; test save/load, map traversal and battles separately."
