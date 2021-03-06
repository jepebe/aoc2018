from functools import reduce
from math import gcd
from .state_machine import load_state_machine, create_state_machine, add_input, run_state_machine, reset_state_machine
from .state_machine import get_output, is_running, has_output, print_output, get_last_output, flush_output
from .tester import red, green, Tester, color, blue
from .bfs import bfs, bfsf


def find_extents(grid):
    minx = min(x[0] for x in grid)
    miny = min(x[1] for x in grid)
    maxx = max(x[0] for x in grid)
    maxy = max(x[1] for x in grid)
    return minx, maxx, miny, maxy


def find_extents_nd(grid, d=4):
    # Returns min, max pairs for each dimension
    minv = tuple((min(v[i] for v in grid) for i in range(d)))
    maxv = tuple((max(v[i] for v in grid) for i in range(d)))
    return tuple(zip(minv, maxv))


def transpose(tile):
    new_tile = {}
    for (x, y), c in tile.items():
        new_tile[y, x] = tile[x, y]
    return new_tile


def flip_horizontal(tile, ext=None):
    new_tile = {}
    if ext is None:
        ext = find_extents_nd(tile, 2)
    # new_tile = {(ext[0][1] - x, y): c for (x, y), c in tile.items()}
    for (x, y), c in tile.items():
        new_tile[ext[0][1] - x, y] = c
    return new_tile


def flip_vertical(tile, ext=None):
    new_tile = {}
    if ext is None:
        ext = find_extents_nd(tile, 2)
    for (x, y), c in tile.items():
        new_tile[x, ext[1][1] - y] = c
    return new_tile


def rotate90(tile, ext=None):
    new_tile = {}
    if ext is None:
        ext = find_extents_nd(tile, 2)
    for (x, y), c in tile.items():
        new_tile[ext[1][1] - y, x] = c  # combined transpose + flip horizontal
    return new_tile


def print_map(grid, look_up=None, missing=None, func=None):
    minx, maxx, miny, maxy = find_extents(grid)

    for y in range(miny, maxy + 1):
        row = []
        for x in range(minx, maxx + 1):
            if (x, y) not in grid:
                if missing:
                    row.append(missing)
                else:
                    row.append(' ')
            else:
                value = grid[(x, y)]
                if look_up:
                    row.append(look_up[value])
                elif func:
                    row.append(func(grid, (x, y)))
                else:
                    if isinstance(value, bool):
                        row.append('T' if value else 'F')
                    else:
                        row.append(value)

        print(''.join(row))


def lcm(a, b):
    return a * b // gcd(a, b)


def lcms(*numbers):
    return reduce(lcm, numbers)


def add_tuple(p1, p2):
    return p1[0] + p2[0], p1[1] + p2[1]


def scale_tuple(p, s):
    return p[0] * s, p[1] * s


def terminal(state_machine):
    while is_running(state_machine):
        run_state_machine(state_machine)
        print_output(state_machine)
        if is_running(state_machine):
            inpt = input()
            for c in inpt:
                add_input(state_machine, ord(c))
            add_input(state_machine, ord('\n'))
