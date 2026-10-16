"""Eryon-themed tilesets: graphical-only replacements, no geometry changes."""
import json
from pathlib import Path
import struct
import unittest

ROOT=Path(__file__).resolve().parents[1]
LAYOUTS=ROOT/"data/layouts/layouts.json"
GRAPHICS=(ROOT/"src/data/tilesets/graphics.h").read_text()
HEADERS=(ROOT/"src/data/tilesets/headers.h").read_text()

BIOMES={
    "Aurora":("petalburg",128,80),
    "Urban":("rustboro",128,256),
    "Forest":("rustboro",128,256),
    "Crystal":("rustboro",128,256),
    "Desert":("rustboro",128,256),
    "Lunar":("rustboro",128,256),
}

class EryonBiomeArtTests(unittest.TestCase):
    def test_all_42_maps_use_registered_eryon_graphics_without_moving_warps(self):
        layouts=json.loads(LAYOUTS.read_text())["layouts"]
        regional=[l for l in layouts if l["id"].startswith("LAYOUT_ERYON_")]
        self.assertEqual(len(regional),42)
        by_biome={}
        for layout in regional:
            with self.subTest(map=layout["id"]):
                self.assertEqual(layout["primary_tileset"],"gTileset_General")
                self.assertTrue(layout["secondary_tileset"].startswith("gTileset_Eryon"))
                biome=layout["secondary_tileset"].removeprefix("gTileset_Eryon")
                self.assertIn(biome,BIOMES)
                by_biome[biome]=by_biome.get(biome,0)+1
                self.assertIn("const struct Tileset "+layout["secondary_tileset"],HEADERS)
                self.assertTrue((ROOT/layout["blockdata_filepath"]).is_file())
        self.assertEqual(set(by_biome),set(BIOMES))

    def test_gba_banks_preserve_base_metatiles_and_attributes(self):
        for biome,(base,width,height) in BIOMES.items():
            with self.subTest(biome=biome):
                p=ROOT/"data/tilesets/secondary"/("eryon_"+biome.lower())
                png=(p/"tiles.png").read_bytes()
                self.assertEqual(png[:8],b"\x89PNG\r\n\x1a\n")
                self.assertEqual(struct.unpack(">IIBBBBB",png[16:29])[:4],
                                 (width,height,4,3))
                for i in range(16):
                    pal=(p/"palettes"/f"{i:02d}.pal").read_text().splitlines()
                    self.assertEqual(pal[:3],["JASC-PAL","0100","16"])
                    self.assertEqual(len(pal),19)
                self.assertIn(".metatiles = gMetatiles_"+base.title()+",",HEADERS)
                self.assertIn(".metatileAttributes = gMetatileAttributes_"+
                              base.title()+",",HEADERS)
                self.assertIn("gTilesetTiles_Eryon"+biome+"[]",GRAPHICS)
                self.assertIn("gTilesetPalettes_Eryon"+biome+"[][16]",GRAPHICS)

    def test_build_generates_tiles_before_compilation(self):
        build=(ROOT/"tools/build_eryon.sh").read_text()
        self.assertIn("python3 tools/eryon_tileset_visuals.py",build)
        self.assertLess(build.index("python3 tools/eryon_tileset_visuals.py"),
                        build.index("python3 tools/eryon_visual_assets.py"))

if __name__=="__main__":
    unittest.main()
