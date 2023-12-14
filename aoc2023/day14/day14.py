import aoc

tester = aoc.Tester("Parabolic Reflector Dish")


def parse_input(data: str) -> aoc.Grid2D:
    grid: aoc.Grid2D = {}
    for y, line in enumerate(data.splitlines()):
        for x, c in enumerate(line):
            grid[(x, y)] = c

    return grid


def slide_rocks(grid: aoc.Grid2D) -> aoc.Grid2D:
    for x, y, c in aoc.iterate_grid(grid):
        if c == ".":
            continue

        if c == "O":
            dy = 0
            while (x, y + dy - 1) in grid and grid[(x, y + dy - 1)] == ".":
                dy -= 1

            if dy < 0 and grid[(x, y + dy)] == ".":
                grid[(x, y)] = "."
                grid[(x, y + dy)] = "O"

    return grid


def total_load(grid: aoc.Grid2D) -> int:
    minx, maxx, miny, maxy = aoc.find_extents(grid)
    total = 0
    for x, y, c in aoc.iterate_grid(grid):
        if c == "O":
            total += maxy - y + 1

    return total


def run_tests(t: aoc.Tester):
    t.test_section("Tests")
    data = aoc.read_input("input_test")
    grid = parse_input(data)
    grid = slide_rocks(grid)
    t.test_value(total_load(grid), 136)


run_tests(tester)

data = aoc.read_input()
grid = parse_input(data)
grid = slide_rocks(grid)

tester.test_section("Part 1")
solution_1 = total_load(grid)
tester.test_solution(solution_1, 109654)

tester.test_section("Part 2")
tester.test_solution(2, 208191)
