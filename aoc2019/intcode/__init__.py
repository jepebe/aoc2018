from functools import reduce
from math import gcd
from .state_machine import load_state_machine, create_state_machine, add_input, run_state_machine
from .state_machine import get_output, is_running, has_output, print_output, get_last_output, flush_output
from .tester import red, green, Tester, color, blue
from .bfs import bfs


def find_extents(grid):
    minx = min(x[0] for x in grid)
    miny = min(x[1] for x in grid)
    maxx = max(x[0] for x in grid)
    maxy = max(x[1] for x in grid)
    return minx, maxx, miny, maxy


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
                if look_up:
                    row.append(look_up[grid[(x, y)]])
                elif func:
                    row.append(func(grid, (x, y)))
                else:
                    row.append('∞')

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
