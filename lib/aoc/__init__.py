import typing
from functools import reduce
from math import gcd
from .tester import red, green, Tester, color, blue
from .bfs import bfs, bfsf
from .floyd_warshall import Distances, print_floyd_warshall, floyd_warshall
from itertools import zip_longest

Extents = tuple[int, int, int, int]


def grouper(n, iterable, fill_value=None) -> typing.Iterator:
    # Groups together items in an iterable
    # Example: grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx
    args = [iter(iterable)] * n
    return zip_longest(fillvalue=fill_value, *args)


def read_input(filename: str = "input") -> str:
    with open(filename) as f:
        data = f.read()
    return data


def find_extents(grid) -> Extents:
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
    """Least Common Multiple for two numbers"""
    return a * b // gcd(a, b)


def lcms(*numbers):
    """LCM for multiple numbers"""
    return reduce(lcm, numbers)


def add_tuple(p1, p2):
    return p1[0] + p2[0], p1[1] + p2[1]


def add_tuple3(p1, p2):
    return p1[0] + p2[0], p1[1] + p2[1], p1[2] + p2[2]


def scale_tuple(p, s):
    return p[0] * s, p[1] * s


def diff_tuple(t1, t2):
    return t1[0] - t2[0], t1[1] - t2[1]


def abs_tuple(t):
    return abs(t[0]), abs(t[1])
