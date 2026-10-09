# Eryon terrain implementation status

The route sketches produced by `python3 tools/eryon_terrain_plan.py` are **design-only**. They are not `map.bin` files and do not change the terrain shown in-game.

## Current work

- Estrada Oriental: west/east exits at (0,22) and (47,22); surveyor (16,21), medic (33,26), clue marker (8,18).
- Vale dos Ventos: west exit at (0,22); ranger (14,21), researcher (32,25), lookout (39,16), markers (23,18) and (37,10).
- The generator checks that each point is connected to the west entrance in its **abstract** walkability plan.

## Required for playable terrain

1. Choose actual metatile IDs from the configured primary and secondary tilesets in Porymap.
2. Author distinct 48×44 `map.bin` layouts for each route; update `data/layouts/layouts.json` to reference them.
3. Confirm elevation, impassable metatiles, wild grass and warp arrival tiles in the engine.
4. Configure wild encounters for the new map IDs and compile/test on a GBA emulator.

Do not mark these tasks complete based solely on the ASCII plans.
