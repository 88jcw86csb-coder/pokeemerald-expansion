"""Inspect the generated, GBA-compatible Eryon PNG data, not just names.

These byte-level checks catch damaged PNG chunks, wrong bit depth/size, missing
palette indices, blank character portraits and missing field frames. A pass
does NOT prove sprites look correct on a GBA screen or Delta emulator.
"""
from pathlib import Path
import hashlib
import struct
import unittest
import zlib

ROOT = Path(__file__).resolve().parents[1]
SIGNATURE = b"\x89PNG\r\n\x1a\n"
LEADERS = ("kael", "volt", "bjorn", "tessa", "nyx", "kaio", "lyra", "ryu")
PORTRAITS = tuple("eryon_" + p for p in LEADERS) + (
    "eryon_eclipse", "eryon_eclipse_f", "eryon_commander",
    "eryon_aria", "eryon_bastian", "eryon_selene", "eryon_darius",
    "eryon_aurelio", "eryon_elya")
BIOMES = ("aurora", "urban", "forest", "crystal", "desert", "lunar")


def decode_indexed_png(path):
    raw = path.read_bytes()
    if not raw.startswith(SIGNATURE):
        raise ValueError(f"{path}: invalid PNG signature")
    offset = 8
    chunks, compressed = [], []
    width = height = None
    palette = None
    while offset < len(raw):
        if offset + 12 > len(raw):
            raise ValueError(f"{path}: truncated PNG chunk")
        length = int.from_bytes(raw[offset:offset+4], "big")
        end = offset + 12 + length
        if end > len(raw):
            raise ValueError(f"{path}: PNG chunk overflows file")
        tag = raw[offset+4:offset+8]
        data = raw[offset+8:offset+8+length]
        actual = int.from_bytes(raw[end-4:end], "big")
        expected = zlib.crc32(tag+data) & 0xFFFFFFFF
        if actual != expected:
            raise ValueError(f"{path}: {tag!r} CRC mismatch")
        chunks.append(tag)
        if tag == b"IHDR":
            if len(data) != 13:
                raise ValueError("invalid IHDR length")
            width, height, bit, kind, compression, filter_mode, interlace = (
                struct.unpack(">IIBBBBB", data))
            if (bit, kind, compression, filter_mode, interlace) != (4,3,0,0,0):
                raise ValueError(f"{path}: not noninterlaced indexed 4bpp")
            if not width or not height or width % 8 or height % 8:
                raise ValueError(f"{path}: invalid 8px GBA tile alignment")
        elif tag == b"PLTE":
            palette = data
        elif tag == b"IDAT":
            compressed.append(data)
        elif tag == b"IEND":
            if end != len(raw):
                raise ValueError(f"{path}: garbage after IEND")
            break
        offset = end
    if chunks[0] != b"IHDR" or chunks[-1] != b"IEND" or not compressed:
        raise ValueError(f"{path}: incomplete PNG structure")
    if palette is None or len(palette) != 48:
        raise ValueError(f"{path}: 16-entry GBA palette required")
    pixels = zlib.decompress(b"".join(compressed))
    stride = width // 2
    if len(pixels) != (stride + 1)*height:
        raise ValueError(f"{path}: invalid inflated row length")
    decoded = []
    for y in range(height):
        row = pixels[y*(stride+1):(y+1)*(stride+1)]
        if row[0] != 0:
            raise ValueError(f"{path}: unexpected PNG filter (expected zero)")
        for octet in row[1:]:
            decoded.extend((octet >> 4, octet & 0x0F))
    if len(decoded) != width*height or max(decoded) >= 16:
        raise ValueError(f"{path}: invalid palette index")
    return width, height, decoded


class EryonGraphicsIntegrityTests(unittest.TestCase):
    def test_all_six_generated_biomes_decode_without_corruption(self):
        sizes = {
            "aurora": (128, 80), "urban": (128,256),
            "forest": (128,256), "crystal": (128,256),
            "desert": (128,256), "lunar": (128,256),
        }
        for name in BIOMES:
            with self.subTest(biome=name):
                path = ROOT / "data/tilesets/secondary" / ("eryon_" + name) / "tiles.png"
                w, h, px = decode_indexed_png(path)
                self.assertEqual((w, h), sizes[name])
                self.assertGreater(len(set(px)), 2, f"{name}: blank/flat atlas")

    def test_leader_and_eclipse_battle_portraits_decode_distinctly(self):
        unique = set()
        for name in PORTRAITS:
            with self.subTest(portrait=name):
                path = ROOT / "graphics/trainers/front_pics" / (name+".png")
                w, h, px = decode_indexed_png(path)
                self.assertEqual((w,h), (64,64))
                self.assertGreater(len(set(px)), 3)
                self.assertGreater(sum(color != 0 for color in px), 100)
                unique.add(hashlib.sha256(bytes(px)).digest())
        self.assertEqual(len(unique), len(PORTRAITS))

    def test_all_eight_leader_field_sprites_have_visible_frames(self):
        for name in LEADERS:
            with self.subTest(leader=name):
                path = (ROOT / "graphics/object_events/pics/people/eryon_leaders" /
                        ("eryon_"+name+".png"))
                width,height,px = decode_indexed_png(path)
                self.assertEqual((width,height), (32,128))
                for frame in range(8):
                    fx,fy=(frame%2)*16,(frame//2)*32
                    region = [px[y*width+x] for y in range(fy,fy+32)
                              for x in range(fx,fx+16)]
                    self.assertGreater(
                        sum(v != 0 for v in region), 35,
                        f"{name}: blank frame {frame}")

    def test_protagonists_and_eclipse_field_graphics_decode(self):
        for folder in ("eryon_hero", "eryon_hero_f"):
            with self.subTest(hero=folder):
                path = ROOT / "graphics/object_events/pics/people" / folder / "walking.png"
                w,h,px = decode_indexed_png(path)
                self.assertEqual((w,h),(144,32))
                self.assertGreater(len(set(px)),3)
                self.assertGreater(sum(v!=0 for v in px),100)
        eclipse = ROOT / "graphics/object_events/pics/people/eryon_eclipse.png"
        w,h,px = decode_indexed_png(eclipse)
        self.assertEqual((w,h),(32,128))
        self.assertGreater(len(set(px)),3)

    def test_hero_graphics_have_no_missing_or_blank_4bpp_frames(self):
        # Check every action, not only the two 9-frame walking strips.
        cases = {
            "eryon_hero": {"walking":(9,16), "running":(9,16),
                           "field_move":(5,32), "surfing":(6,32),
                           "mach_bike":(9,32), "acro_bike":(27,32),
                           "fishing":(12,32), "underwater":(4,32)},
            "eryon_hero_f": {"walking":(9,16), "running":(9,16),
                             "field_move":(5,32), "surfing":(6,32),
                             "mach_bike":(9,32), "acro_bike":(27,32),
                             "fishing":(12,32), "underwater":(4,32),
                             "watering":(6,32), "decorating":(1,16)}
        }
        for actor, sheets in cases.items():
            for action,(count,frame_width) in sheets.items():
                with self.subTest(actor=actor,action=action):
                    file = ROOT / "graphics/object_events/pics/people" / actor / (action+".png")
                    width,height,pixels=decode_indexed_png(file)
                    self.assertEqual((width,height),(count*frame_width,32))
                    unique_frames=set()
                    for i in range(count):
                        frame=bytes(pixels[y*width+i*frame_width:y*width+(i+1)*frame_width]
                                    for y in []) if False else bytes(
                            pix for y in range(32) for pix in
                            pixels[y*width+i*frame_width:y*width+(i+1)*frame_width]
                        )
                        self.assertGreater(sum(value!=0 for value in frame),55)
                        unique_frames.add(hashlib.sha256(frame).digest())
                    if count >= 4:
                        self.assertGreaterEqual(len(unique_frames),3)

    def test_hero_battle_portraits_have_valid_indexed_frame_geometry(self):
        for name in ("eryon_hero","eryon_hero_f"):
            with self.subTest(actor=name):
                w,h,pixels=decode_indexed_png(ROOT / "graphics/trainers/front_pics" / (name+".png"))
                self.assertEqual((w,h),(64,64))
                self.assertGreater(sum(x!=0 for x in pixels),200)
                w,h,pixels=decode_indexed_png(ROOT / "graphics/trainers/back_pics" / (name+".png"))
                self.assertEqual((w,h),(64,256))
                frames=[tuple(pixels[y*64:(y+1)*64] for y in range(i*64,(i+1)*64))
                        for i in range(4)]
                self.assertTrue(all(sum(sum(px!=0 for px in row) for row in f)>150 for f in frames))
                self.assertGreaterEqual(len(set(frames)),3)


if __name__ == "__main__":
    unittest.main()
