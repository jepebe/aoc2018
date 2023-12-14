from collections import namedtuple

import aoc

tester = aoc.Tester("Parabolic Reflector Dish")

Extents = namedtuple("Extents", ["minx", "maxx", "miny", "maxy"])


def parse_input(data: str) -> aoc.Grid2D:
    grid: aoc.Grid2D = {}
    for y, line in enumerate(data.splitlines()):
        for x, c in enumerate(line):
            grid[(x, y)] = c

    return grid


def slide_rock(grid: aoc.Grid2D, pos: tuple[int, int], dir: tuple[int, int]):
    slide_pos = pos
    next_pos = (pos[0] + dir[0], pos[1] + dir[1])
    while next_pos in grid and grid[next_pos] == ".":
        slide_pos = next_pos
        next_pos = (next_pos[0] + dir[0], next_pos[1] + dir[1])

    if slide_pos in grid and pos != slide_pos and grid[slide_pos] == ".":
        grid[pos] = "."
        grid[slide_pos] = "O"


def slide_north(grid: aoc.Grid2D, extents: Extents) -> aoc.Grid2D:
    for y in range(extents.miny, extents.maxy + 1):
        for x in range(extents.minx, extents.maxx + 1):
            c = grid[(x, y)]

            if c == "O":
                slide_rock(grid, (x, y), (0, -1))
    return grid


def slide_west(grid: aoc.Grid2D, extents: Extents) -> aoc.Grid2D:
    for y in range(extents.miny, extents.maxy + 1):
        for x in range(extents.minx, extents.maxx + 1):
            c = grid[(x, y)]

            if c == "O":
                slide_rock(grid, (x, y), (-1, 0))
    return grid


def slide_south(grid: aoc.Grid2D, extents: Extents) -> aoc.Grid2D:
    for y in range(extents.maxy, extents.miny - 1, -1):
        for x in range(extents.minx, extents.maxx + 1):
            c = grid[(x, y)]

            if c == "O":
                slide_rock(grid, (x, y), (0, 1))

    return grid


def slide_east(grid: aoc.Grid2D, extents: Extents) -> aoc.Grid2D:
    for y in range(extents.miny, extents.maxy + 1):
        for x in range(extents.maxx, extents.minx - 1, -1):
            c = grid[(x, y)]

            if c == "O":
                slide_rock(grid, (x, y), (1, 0))

    return grid


def cycle(grid: aoc.Grid2D, extents: Extents) -> aoc.Grid2D:
    grid = slide_north(grid, extents)
    grid = slide_west(grid, extents)
    grid = slide_south(grid, extents)
    grid = slide_east(grid, extents)
    return grid


def total_load_after(grid: aoc.Grid2D, cycles: int) -> int:
    extents = Extents(*aoc.find_extents(grid))
    cycle_hashes = {}
    cycle_loads = {}
    cycle_count = 0
    for _ in range(cycles):
        grid = cycle(grid, extents)
        cycle_count += 1
        grid_hash = hash(frozenset(grid.items()))

        if grid_hash in cycle_hashes:
            cycle_start = cycle_hashes[grid_hash]
            cycle_size = cycle_count - cycle_start
            extra_cycles = (cycles - cycle_start) % cycle_size
            return cycle_loads[cycle_start + extra_cycles]
        else:
            cycle_hashes[grid_hash] = cycle_count
            cycle_loads[cycle_count] = total_load(grid, extents)

    # for small cycle sizes
    return cycle_loads[cycles - 1]


def total_load(grid: aoc.Grid2D, extents: Extents) -> int:
    total = 0
    for y in range(extents.miny, extents.maxy + 1):
        for x in range(extents.minx, extents.maxx + 1):
            c = grid[(x, y)]
            if c == "O":
                total += extents.maxy - y + 1

    return total


def run_tests(t: aoc.Tester):
    t.test_section("Tests")
    data = aoc.read_input("input_test")
    grid = parse_input(data)
    grid = slide_north(grid, Extents(*aoc.find_extents(grid)))
    t.test_value(total_load(grid, Extents(*aoc.find_extents(grid))), 136)

    grid = parse_input(data)
    grid_c1 = parse_input(aoc.read_input("input_test_cycle_1"))
    grid_c2 = parse_input(aoc.read_input("input_test_cycle_2"))
    grid_c3 = parse_input(aoc.read_input("input_test_cycle_3"))

    grid = cycle(grid, Extents(*aoc.find_extents(grid)))
    t.test_value(grid, grid_c1)

    grid = cycle(grid, Extents(*aoc.find_extents(grid)))
    t.test_value(grid, grid_c2)

    grid = cycle(grid, Extents(*aoc.find_extents(grid)))
    t.test_value(grid, grid_c3)

    grid = parse_input(data)
    load = total_load_after(grid, 3)
    t.test_value(load, total_load(grid_c3, Extents(*aoc.find_extents(grid_c3))))

    grid = parse_input(data)
    load = total_load_after(grid, 1000000000)
    t.test_value(load, 64)


run_tests(tester)

data = aoc.read_input()

tester.test_section("Part 1")
grid = parse_input(data)
grid = slide_north(grid, Extents(*aoc.find_extents(grid)))
solution_1 = total_load(grid, Extents(*aoc.find_extents(grid)))
tester.test_solution(solution_1, 109654)

tester.test_section("Part 2")
grid = parse_input(data)
solution_2 = total_load_after(grid, 1000000000)
tester.test_solution(solution_2, 94876)
