import aoc

tester = aoc.Tester("Lavaduct Lagoon")


def parse(data: str) -> tuple[aoc.Grid2D, aoc.Grid2D]:
    grid: aoc.Grid2D = {}
    colors: aoc.Grid2D = {}

    x, y = 0, 0
    for line in data.splitlines():
        direction, steps, color = line.split()
        for i in range(int(steps)):
            grid[x, y] = "#"
            colors[x, y] = color
            match direction:
                case "R":
                    x += 1
                case "L":
                    x -= 1
                case "U":
                    y -= 1
                case "D":
                    y += 1
                case _:
                    raise ValueError(f"Invalid direction: {direction}")
    aoc.print_map(grid)
    return grid, colors


def fill(grid: aoc.Grid2D) -> int:
    filled: aoc.Grid2D = {}

    inside = None
    for x, y, c in aoc.iterate_grid(grid):
        if (x, y) in grid and (x, y + 1) in grid and (x + 1, y + 1) not in grid:
            inside = x + 1, y + 1
            break

    queue = [inside]
    while queue:
        x, y = queue.pop()
        if (x, y) in filled:
            continue

        if (x, y) in grid and grid[x, y] == "#":
            filled[x, y] = "*"
            continue  # edge

        filled[x, y] = "#"

        for dx, dy in aoc.DIRECTIONS2D_4:
            queue.append((x + dx, y + dy))
    aoc.print_map(filled)
    return len(filled)


def run_tests(t: aoc.Tester):
    t.test_section("Tests")
    grid, colors = parse(aoc.read_input("input_test"))
    t.test(fill(grid), 62)


run_tests(tester)

grid, colors = parse(aoc.read_input())
fill_count = fill(grid)

tester.test_section("Part 1")
solution_1 = fill(grid)
tester.test_value_neq(solution_1, 50266)
tester.test_solution(fill_count, 71502)

tester.test_section("Part 2")
tester.test_solution(2, 208191)
