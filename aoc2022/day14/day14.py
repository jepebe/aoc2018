import aoc

tester = aoc.Tester("Regolith Reservoir")


def parse_grid(data: str):
    grid = {}
    for line in data.splitlines():
        px = None
        py = None
        for point in line.split(sep=" -> "):
            sx, sy = map(int, point.split(sep=","))
            if px is not None:
                if px != sx:
                    start = min(px, sx)
                    end = max(px, sx)
                    delta = (1, 0)
                    pos = start, sy
                else:
                    start = min(py, sy)
                    end = max(py, sy)
                    delta = (0, 1)
                    pos = sx, start

                for _ in range(end - start + 1):
                    grid[pos] = "#"
                    pos = aoc.add_tuple(pos, delta)
            px = sx
            py = sy

    return grid


def find_stop(grid, pos, max_y) -> tuple[int, int] | None:
    if pos in grid:
        return None

    while True:
        if pos[1] > max_y:
            # off the grid
            return None

        next_pos = aoc.add_tuple(pos, (0, 1))

        if next_pos not in grid:
            pos = next_pos
            continue

        left_pos = aoc.add_tuple(pos, (-1, 1))
        if left_pos not in grid:
            pos = left_pos
            continue

        right_pos = aoc.add_tuple(pos, (1, 1))
        if right_pos not in grid:
            pos = right_pos
            continue

        break

    return pos[0], pos[1]


def simulate_sand(grid: dict[tuple[int, int], str]) -> int:
    ext = aoc.find_extents(grid)
    iterations = 0
    while True:
        sand = (500, 0)
        sand = find_stop(grid, sand, max_y=ext[3])
        if sand:
            grid[sand] = "o"
            iterations += 1
        else:
            return iterations


def add_floor(grid: dict[tuple[int, int], str]):
    ext = aoc.find_extents(grid)
    max_y = ext[3] + 2

    for x in range(ext[0] - max_y, ext[1] + max_y):
        grid[(x, max_y)] = "#"


def run_tests(t: aoc.Tester):
    t.test_section("Tests")

    test_map = """498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9"""

    test_grid = parse_grid(test_map)
    t.test_value(simulate_sand(test_grid), 24)
    # aoc.print_map(test_grid)

    test_grid = parse_grid(test_map)
    add_floor(test_grid)
    t.test_value(simulate_sand(test_grid), 93)
    # aoc.print_map(test_grid)


run_tests(tester)

tester.test_section("Part 1")
sand_grid = parse_grid(aoc.read_input())
tester.test_value(simulate_sand(sand_grid), 696, "solution to part 1=%s")

tester.test_section("Part 2")
sand_grid = parse_grid(aoc.read_input())
add_floor(sand_grid)
tester.test_value(simulate_sand(sand_grid), 23610, "solution to part 2=%s")
