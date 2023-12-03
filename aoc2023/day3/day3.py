import collections

import aoc

tester = aoc.Tester("Gear Ratios")

SymbolPos = tuple[str, aoc.Coord]
"""A symbol and its position in the grid. The symbol is the first element, 
the x and y coordinates are the second and third element.
"""
GearRatios = dict[SymbolPos, list[int]]
"""A collection of all unique symbols and their ratios. The symbol with position is the key,
the ratios are the values. A symbol may be adjacent to multiple numbers, so the ratios are a list.
"""


def parse(data: str) -> aoc.Grid2D:
    grid = {}
    ops = set()
    for y, line in enumerate(data.splitlines()):
        for x, char in enumerate(line):
            grid[(x, y)] = char
            ops.add(char)
    # print(sorted(ops))
    return grid


def find_adjacent_symbols(grid: aoc.Grid2D, pos: aoc.Coord) -> list[SymbolPos]:
    """Find all adjacent symbols to a position, with their coordinates."""
    x, y = pos
    symbols = []
    for dx, dy in aoc.DIRECTIONS2D_8:
        pos = (x + dx, y + dy)
        if pos in grid and grid[pos] in "#$%&*+-/=@":
            symbols.append((grid[pos], pos))
    return symbols


def identify_gear_parts(grid: aoc.Grid2D) -> tuple[list[int], GearRatios]:
    gear_parts = []
    gear_ratios = collections.defaultdict(list)  # collection of all unique symbols and their ratios
    number = 0
    adjacent_symbols = set()  # a number may have multiple hits for the same adjacent symbol
    for x, y, candidate in aoc.iterate_grid(grid):
        # complete number from previous row, if any
        if x == 0:
            if number > 0 and adjacent_symbols:
                gear_parts.append(number)
                for symbol in adjacent_symbols:
                    gear_ratios[symbol].append(number)
            number = 0
            adjacent_symbols = set()

        # a number may be done
        if not candidate.isdigit():
            if number > 0 and adjacent_symbols:
                gear_parts.append(number)
                for symbol in adjacent_symbols:
                    gear_ratios[symbol].append(number)
            number = 0
            adjacent_symbols = set()
            continue

        if candidate.isdigit():
            number *= 10
            number += int(candidate)

        for symbol in find_adjacent_symbols(grid, (x, y)):
            adjacent_symbols.add(symbol)
    return gear_parts, gear_ratios


def find_all_parts(grid: aoc.Grid2D) -> int:
    gear_parts, _ = identify_gear_parts(grid)
    return sum(gear_parts)


def find_gear_ratios(grid: aoc.Grid2D) -> int:
    _, gear_ratios = identify_gear_parts(grid)

    total = 0
    for symbol, ratio in gear_ratios.items():
        if symbol[0] == "*" and len(ratio) == 2:
            total += ratio[0] * ratio[1]

    return total


def run_tests(t: aoc.Tester):
    t.test_section("Tests")
    data = aoc.read_input("input_test")
    grid = parse(data)

    t.test_value(find_all_parts(grid), 4361)

    grid = parse(".952*308.")
    t.test_value(find_all_parts(grid), 952 + 308)
    grid = parse(".952*308\n...123..")
    t.test_value(find_all_parts(grid), 952 + 308 + 123)

    grid = parse("-952.308.")
    t.test_value(find_all_parts(grid), 952)

    grid = parse(".-952\n308..")
    t.test_value(find_all_parts(grid), 952 + 308)

    grid = parse(".952-952.")
    t.test_value(find_all_parts(grid), 952 * 2)

    grid = parse(data)
    t.test_value(find_gear_ratios(grid), 467835)


run_tests(tester)

data = aoc.read_input()
grid = parse(data)

tester.test_section("Part 1")
solution_1 = find_all_parts(grid)
tester.test_less_than(solution_1, 1837615)
tester.test_less_than(solution_1, 1645975)
tester.test_value_neq(solution_1, 332653)
tester.test_solution(solution_1, 525181)

tester.test_section("Part 2")
tester.test_solution(find_gear_ratios(grid), 84289137)
