import typing

Extents = tuple[int, int, int, int]
"""Extents of a grid, minx, maxx, miny, maxy"""

Coord = tuple[int, int]
"""A coordinate in 2D space."""

Grid2D = dict[Coord, typing.Any]
"""A dictionary representing a grid of values. The grid can be sparse. 
The key is a tuple of x and y coordinates.
"""

DIRECTIONS2D_4 = ((0, -1), (1, 0), (0, 1), (-1, 0))
"""Directions in 2D excluding diagonals"""

DIRECTIONS2D_8 = ((0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1))
"""Directions in 2D including diagonals"""


def find_extents(grid: Grid2D) -> Extents:
    """Find the extents of a grid, minx, maxx, miny, maxy."""
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


def iterate_grid(grid: Grid2D) -> tuple[int, int, typing.Any]:
    """Iterates over a grid, yielding x, y and grid value at coordinate (None if missing)."""
    minx, maxx, miny, maxy = find_extents(grid)
    for y in range(miny, maxy + 1):
        for x in range(minx, maxx + 1):
            if (x, y) in grid:
                yield x, y, grid[(x, y)]
            else:
                yield x, y, None


def print_map(
        grid: Grid2D,
        look_up: dict[typing.Any, str] = None,
        missing: str = None,
        func: typing.Callable[[Grid2D, Coord], str] = None,
        missing_func: typing.Callable[[Grid2D, Coord], str] = None):
    """Prints a grid of values.

    If look_up is provided, non-missing values are looked up in the dictionary.
    if missing is provided, missing coordinates are printed with this value.
    If func is provided, non-missing values are passed to the function.
    If missing_func is provided, missing coordinates are passed to the function.
    """
    minx, maxx, miny, maxy = find_extents(grid)

    for y in range(miny, maxy + 1):
        row = []
        for x in range(minx, maxx + 1):
            if (x, y) not in grid:
                if missing_func:
                    row.append(missing_func(grid, (x, y)))
                elif missing:
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


def print_set(grid: set, marker="#", missing=".", border=0):
    """Prints a set of coordinates as a grid."""
    minx, maxx, miny, maxy = find_extents(grid)
    minx -= border
    miny -= border
    maxx += border
    maxy += border
    for y in range(miny, maxy + 1):
        row = []
        for x in range(minx, maxx + 1):
            if (x, y) not in grid:
                row.append(missing)
            else:
                row.append(marker)
        print(''.join(row))
