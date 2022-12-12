import colorsys
import typing

import aoc


def char_color(pos: tuple[int, int], value: typing.Any):
    r = (ord(value) - ord("a")) * 256 // 26
    g = r
    b = r
    return r, g, b


def rainbow_color(pos: tuple[int, int], value: typing.Any):
    hue = (ord(value) - ord("a")) / 26
    r, g, b = colorsys.hsv_to_rgb(hue, 0.6 + (hue * 0.4), 1)
    return int(r * 255), int(g * 255), int(b * 255)


def print_heightmap(grid: dict[tuple[int, int], typing.Any], color_fn: callable = None):
    minx, maxx, miny, maxy = aoc.find_extents(grid)
    missing = (0, 0, 0)

    if not color_fn:
        color_fn = char_color

    for y in range(miny, maxy + 1):
        for x in range(minx, maxx + 1):
            if (x, y) not in grid:
                r, g, b = missing
            else:
                r, g, b = color_fn((x, y), grid[(x, y)])
            print(f"\x1b[48;2;{r};{g};{b}m ", end="")
            # print(f"\x1b[38;2;{r};{g};{b}m#", end="")
        print("\033[0m")
