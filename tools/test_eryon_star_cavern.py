#!/usr/bin/env python3
"""Validate the registered HM-free Star Cavern and its generated plan."""
import unittest
from eryon_star_cavern import ROOT, W, H, cavern, reachable, render


class StarCavernTests(unittest.TestCase):
    def test_lower_switchback_prevents_straight_crossing(self):
        """New lower bypass remains reachable while the upper gallery persists."""
        import json
        from collections import deque
        from build_eryon_map_bins import compile_plan

        t = cavern()
        self.assertEqual(t[22][21], "#")
        self.assertIn((23, 28), reachable(t))
        self.assertIn((29, 9), reachable(t))
        self.assertIn((47, 22), reachable(t))
        info = json.loads((ROOT / "data/maps/Eryon_GrutaDasEstrelas/map.json").read_text())
        occupied = {(e["x"], e["y"]) for e in info["object_events"]}
        q = deque([(0, 22)])
        seen = {(0, 22)}
        while q:
            x, y = q.popleft()
            for p in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
                a,b = p
                if 0 <= a < W and 0 <= b < H and t[b][a] != "#" and p not in occupied and p not in seen:
                    seen.add(p)
                    q.append(p)
        self.assertIn((47, 22), seen, "An NPC must not seal the route")
        for group in ("object_events", "bg_events", "warp_events"):
            for e in info[group]:
                with self.subTest(group=group, coordinate=(e["x"],e["y"])):
                    self.assertIn((e["x"], e["y"]), reachable(t))
        source = ROOT / "docs/eryon/gruta_das_estrelas_terrain_plan.txt"
        binary = (ROOT / "data/layouts/Eryon_GrutaDasEstrelas/map.bin").read_bytes()
        self.assertEqual(binary, compile_plan(source, {"#":0x3C01,".":0x3001,":":0x3003}))

    def test_connected_cavern_and_synchronized_plan(self):
        terrain=cavern()
        self.assertEqual(len(terrain),H)
        self.assertTrue(all(len(row)==W for row in terrain))
        walkable={(x,y) for y,row in enumerate(terrain)
                  for x,tile in enumerate(row) if tile!="#"}
        self.assertEqual(reachable(terrain),walkable)
        self.assertIn((47,22),walkable)
        source=ROOT/"docs/eryon/gruta_das_estrelas_terrain_plan.txt"
        self.assertEqual(source.read_text(encoding="utf-8"),render(terrain))


    def test_upper_gallery_detour_and_registered_event(self):
        """The added northern route must be a genuine optional walkable loop."""
        import json
        from collections import deque
        import struct
        from build_eryon_map_bins import compile_plan

        t = cavern()
        accessible = reachable(t)
        chamber = (29, 9)
        self.assertIn(chamber, accessible)
        self.assertIn((18, 12), accessible)
        self.assertIn((40, 20), accessible)

        # The gallery must join the eastern passage ABOVE the main y=21/22 road.
        seen = {(18, 12)}
        q = deque([(18, 12)])
        while q:
            x, y = q.popleft()
            for nx, ny in ((x-1, y), (x+1, y), (x, y-1), (x, y+1)):
                if 0 <= nx < W and 0 <= ny <= 20 and t[ny][nx] != "#" and (nx, ny) not in seen:
                    seen.add((nx, ny))
                    q.append((nx, ny))
        self.assertIn((40, 20), seen, "upper route cannot bypass the central road")
        self.assertIn(chamber, seen)

        info = json.loads((ROOT / "data/maps/Eryon_GrutaDasEstrelas/map.json").read_text(encoding="utf-8"))
        registered = [event for event in info["bg_events"]
                      if event["script"] == "EryonEstrelas_EventScript_ResonanceGallery"]
        self.assertEqual([(e["x"], e["y"]) for e in registered], [chamber])
        scripts = (ROOT / "data/maps/Eryon_GrutaDasEstrelas/scripts.inc").read_text(encoding="utf-8")
        for label in ("ResonanceGallery", "GalleryReported", "GallerySilent", "GalleryManifest"):
            self.assertIn("EryonEstrelas_EventScript_" + label + "::", scripts)

        # Regeneration must preserve the actual committed blockdata; previously
        # 123 manually refined tiles were silently omitted from the generator.
        plan = ROOT / "docs/eryon/gruta_das_estrelas_terrain_plan.txt"
        binary = (ROOT / "data/layouts/Eryon_GrutaDasEstrelas/map.bin").read_bytes()
        expected = compile_plan(plan, {"#": 0x3C01, ".": 0x3001, ":": 0x3003})
        self.assertEqual(binary, expected)
        for x, y in ((0, 22), (47, 22), (29, 9), (31, 30), (42, 29)):
            offset = (y * W + x) * 2
            self.assertEqual(struct.unpack_from("<H", binary, offset)[0] & 0x0C00, 0)



if __name__=="__main__":
    unittest.main()
