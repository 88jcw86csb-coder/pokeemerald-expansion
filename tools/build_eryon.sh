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

echo "== Eryon: checking all Python tool and gameplay test syntax =="
python3 -m compileall -q tools tests

echo "== Eryon: generate six original regional tileset banks without touching collisions =="
python3 tools/eryon_tileset_visuals.py

echo "== Eryon: generate distinct indexed GBA portraits (leaders / Team Eclipse) =="
python3 tools/eryon_visual_assets.py

python3 tools/eryon_release_qa.py

echo "== Eryon: generate independent title graphic =="
python3 tools/eryon_boot_assets.py

echo "== Eryon: rebuild designed first-act overworld maps == "
python3 tools/eryon_opening_visual_layouts.py

echo "== Eryon: regenerate registered map binaries from authoritative terrain plans =="
python3 tools/build_eryon_map_bins.py --wall 0x3c01 --path 0x3001 --meadow 0x3002 --stone 0x3003 --preview-unregistered
python3 tools/eryon_gym_interiors.py

# Collect the whole regression suite, including League, Eclipse and late
# routes. Keep test discovery dynamic so future tests cannot be silently
# omitted by forgetting another explicit entry here.
echo "== Eryon: Python tool regression suite (complete discovery) =="
python3 -m unittest discover -s tools -p 'test_eryon_*.py' -v

echo "== Eryon: adventure, battle, League and map regressions (complete discovery) =="
python3 -m unittest discover -s tests -p 'test_eryon_*.py' -v

echo "== Eryon: global gameplay/data and map collision audits =="
python3 tools/eryon_validate.py
python3 tools/eryon_layout_audit.py
python3 tools/eryon_physical_route_audit.py --json-output build/eryon-physical-routes.json
python3 tools/eryon_script_warp_audit.py
python3 tools/eryon_world_audit.py
python3 tools/eryon_map_traversal_audit.py

echo "== Eryon: post-validation graphical repair =="
python3 tools/eryon_terrain_visual_repair.py
python3 tools/eryon_overworld_preview.py
# Repeat structural checks against the EXACT rendered blockdata compiled in ROM.
python3 tools/eryon_layout_audit.py
python3 tools/eryon_map_traversal_audit.py

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
