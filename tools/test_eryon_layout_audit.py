#!/usr/bin/env python3
"""Unit tests for the Eryon terrain audit's conservative collision model."""
import struct
import unittest

from eryon_layout_audit import connected_by_collision_bits, decode_block, zero_collision_edge_positions, reachable_edge_positions


def grid(width, height, walls=()):
    blocked = set(walls)
    return b"".join(
        struct.pack("<H", 1 | ((1 if (x, y) in blocked else 0) << 10))
        for y in range(height) for x in range(width)
    )


class EryonLayoutAuditTests(unittest.TestCase):
    def test_block_decode(self):
        raw = struct.pack("<H", 27 | (2 << 10) | (3 << 12))
        self.assertEqual(decode_block(raw, 1, 0, 0), (27, 2, 3))

    def test_open_path(self):
        raw = grid(4, 3)
        self.assertTrue(connected_by_collision_bits(raw, 4, 3, (0, 1), (3, 1)))

    def test_wall_separates_exits(self):
        raw = grid(4, 3, walls={(1, 0), (1, 1), (1, 2)})
        self.assertFalse(connected_by_collision_bits(raw, 4, 3, (0, 1), (3, 1)))

    def test_blocked_start_or_exit(self):
        raw = grid(3, 2, walls={(0, 0), (2, 1)})
        self.assertFalse(connected_by_collision_bits(raw, 3, 2, (0, 0), (1, 0)))
        self.assertFalse(connected_by_collision_bits(raw, 3, 2, (1, 0), (2, 1)))

    def test_edge_collision_candidates_all_directions(self):
        raw = grid(4, 3, walls={(0, 0), (3, 1), (2, 2)})
        self.assertEqual(zero_collision_edge_positions(raw, 4, 3, "up"),
                         [(1, 0), (2, 0), (3, 0)])
        self.assertEqual(zero_collision_edge_positions(raw, 4, 3, "down"),
                         [(0, 2), (1, 2), (3, 2)])
        self.assertEqual(zero_collision_edge_positions(raw, 4, 3, "left"),
                         [(0, 1), (0, 2)])
        self.assertEqual(zero_collision_edge_positions(raw, 4, 3, "right"),
                         [(3, 0), (3, 2)])

    def test_edge_candidates_invalid_direction(self):
        with self.assertRaises(ValueError):
            zero_collision_edge_positions(grid(2, 2), 2, 2, "diagonal")

    def test_reachable_edge_excludes_isolated_clear_exit(self):
        raw = grid(5, 3, walls={(2, 0), (2, 1), (2, 2)})
        self.assertEqual(reachable_edge_positions(raw, 5, 3, (0, 1), "right"), [])
        self.assertEqual(reachable_edge_positions(raw, 5, 3, (0, 1), "left"),
                         [(0, 0), (0, 1), (0, 2)])

    def test_reachable_edge_from_blocked_spawn(self):
        raw = grid(3, 3, walls={(1, 1)})
        self.assertEqual(reachable_edge_positions(raw, 3, 3, (1, 1), "up"), [])

    def test_out_of_bounds_exit(self):
        raw = grid(3, 2)
        self.assertFalse(connected_by_collision_bits(raw, 3, 2, (-1, 0), (2, 1)))


if __name__ == "__main__":
    unittest.main()
