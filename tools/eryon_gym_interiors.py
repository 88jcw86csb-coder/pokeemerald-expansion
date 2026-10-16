#!/usr/bin/env python3
"""Generate eight distinct Eryon gym interiors without altering campaign data.

The 24x18 arenas retain existing object/trigger coordinates, elevation,
scripted return travel, badge flags, trainer teams and metatile attributes.
Decorative obstacle silhouettes are specific to each city; scripted puzzles
remain the existing two-panel sequence until their mechanics are redesigned.
This generates collision layouts, not final hand-painted GBA gym artwork.
"""
from collections import deque
from pathlib import Path
import struct

ROOT = Path(__file__).resolve().parents[1]
CITIES = ("Verdelume", "Neonara", "Frostheim", "Arkhara",
          "Umbra", "Ignivar", "Lunaris", "Drakonia")
WIDTH, HEIGHT = 24, 18
FLOOR = 0x3001
WALL = 0x3C0D
DETAIL = 0x3005

# Each motif consists of straight, blocked metatile runs (x1,y1,x2,y2).
# Separate obstacle islands keep every accessible floor tile connected.
MOTIFS = (
    # Verdelume: staggered root terraces and greenhouse divisions.
    ((3,4,9,4),(14,4,20,4),(4,12,7,12),(16,12,19,12),(6,6,6,8),(17,6,17,8)),
    # Neonara: two conductor stacks with staggered branching contacts.
    ((6,3,6,7),(17,3,17,7),(6,12,6,14),(17,12,17,14),(7,5,9,5),(14,5,16,5)),
    # Frostheim: fractured ice shelves, split at the central stair.
    ((4,5,7,5),(7,5,7,8),(16,5,19,5),(16,5,16,8),(4,13,8,13),(15,13,19,13)),
    # Arkhara: archaeological gallery corners and recessed alcoves.
    ((4,4,8,4),(4,5,4,8),(15,4,19,4),(19,5,19,8),(5,12,8,12),(15,12,18,12)),
    # Umbra: offset dark-garden banks, suggesting two lantern pools.
    ((5,4,8,4),(4,5,4,8),(15,4,18,4),(19,5,19,8),(5,13,8,13),(15,13,18,13)),
    # Ignivar: paired heat exchangers and two short pressure manifolds.
    ((5,4,5,7),(18,4,18,7),(5,12,8,12),(15,12,18,12),(8,5,9,5),(14,5,15,5)),
    # Lunaris: four separated arcs around a clear observatory axis.
    ((5,5,5,7),(6,4,8,4),(15,4,17,4),(18,5,18,7),(5,12,5,14),(18,12,18,14)),
    # Drakonia: interlocking dragon-wing steps, leaving both panel paths.
    ((4,5,7,5),(7,6,7,8),(16,5,19,5),(16,6,16,8),(5,12,8,12),(15,12,18,12)),
)

# Registered NPCs / scripts in GymEryon_*/map.json.
LEADER = (12, 6)
GUIDE = (9, 8)
FIRST_PANEL = (8, 10)
SECOND_PANEL = (16, 10)
EXIT = (12, 16)
ARRIVAL = (12, 15)
EVENTS = frozenset((LEADER, GUIDE, FIRST_PANEL, SECOND_PANEL, EXIT, ARRIVAL))


def layout(index):
    if not 0 <= index < len(CITIES):
        raise ValueError("gym index out of range")
    cells = [[FLOOR] * WIDTH for _ in range(HEIGHT)]
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if x in (0, WIDTH - 1) or y in (0, HEIGHT - 1):
                cells[y][x] = WALL
    for x1, y1, x2, y2 in MOTIFS[index]:
        if x1 != x2 and y1 != y2:
            raise ValueError("motif run must be horizontal or vertical")
        for y in range(min(y1, y2), max(y1, y2) + 1):
            for x in range(min(x1, x2), max(x1, x2) + 1):
                if not (1 <= x < WIDTH-1 and 1 <= y < HEIGHT-1):
                    raise ValueError("motif overlaps border")
                if (x, y) in EVENTS:
                    raise ValueError(f"motif blocks registered event {(x,y)}")
                cells[y][x] = WALL
    # Walkable etched tiles are accents, never walls or event replacements.
    for x, y in ((3,10),(20,10),(10,13),(13,13)):
        if cells[y][x] == FLOOR:
            cells[y][x] = DETAIL
    return cells


def reachable(cells, origin, occupied=frozenset()):
    if cells[origin[1]][origin[0]] & 0x0C00 or origin in occupied:
        return set()
    q = deque([origin])
    seen = {origin}
    while q:
        x, y = q.popleft()
        for nx, ny in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
            if (0 <= nx < WIDTH and 0 <= ny < HEIGHT and
                not cells[ny][nx] & 0x0C00 and
                (nx, ny) not in occupied and (nx, ny) not in seen):
                seen.add((nx, ny))
                q.append((nx, ny))
    return seen


def validate(cells):
    if len(cells) != HEIGHT or any(len(row) != WIDTH for row in cells):
        raise ValueError("wrong gym dimensions")
    for x, y in EVENTS:
        if cells[y][x] & 0x0C00:
            raise ValueError(f"registered gym event blocked at {(x,y)}")
    walkable = {(x, y) for y in range(HEIGHT) for x in range(WIDTH)
                if not cells[y][x] & 0x0C00}
    if reachable(cells, ARRIVAL) != walkable:
        raise ValueError("gym floor has inaccessible islands")
    # NPCs are physically occupied during gameplay; do not route through them.
    access = reachable(cells, ARRIVAL, frozenset((LEADER, GUIDE)))
    if not {FIRST_PANEL, SECOND_PANEL, EXIT} <= access:
        raise ValueError("one of the gym puzzle signs or exit is unreachable")
    if not any((LEADER[0]+dx, LEADER[1]+dy) in access
               for dx, dy in ((1,0),(-1,0),(0,1),(0,-1))):
        raise ValueError("gym leader cannot be spoken to")
    if not any((GUIDE[0]+dx, GUIDE[1]+dy) in access
               for dx, dy in ((1,0),(-1,0),(0,1),(0,-1))):
        raise ValueError("gym guide cannot be spoken to")
    return len(walkable)


def generate():
    result = []
    signatures = set()
    for i, city in enumerate(CITIES):
        cells = layout(i)
        walk = validate(cells)
        payload = struct.pack(f"<{WIDTH * HEIGHT}H",
                              *(v for row in cells for v in row))
        if payload in signatures:
            raise ValueError(f"duplicate gym geometry for {city}")
        signatures.add(payload)
        path = ROOT / "data/layouts" / ("GymEryon_" + city) / "map.bin"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(payload)
        print("ERYON_GYM_ARENA", city, WIDTH, HEIGHT, "floor", walk)
        result.append(path)
    return result


if __name__ == "__main__":
    generate()
