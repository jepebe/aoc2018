from functools import reduce
from math import gcd
from .state_machine import load_state_machine, create_state_machine, add_input, run_state_machine, get_output, is_running, has_output
from .tester import red, green, Tester


def print_map(grid, look_up=None, missing=None, func=None):
    minx = min(x[0] for x in grid)
    miny = min(x[1] for x in grid)
    maxx = max(x[0] for x in grid)
    maxy = max(x[1] for x in grid)

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
                    row.append('.')

        print(''.join(row))


def lcm(a, b):
    return a * b // gcd(a, b)


def lcms(*numbers):
    return reduce(lcm, numbers)

