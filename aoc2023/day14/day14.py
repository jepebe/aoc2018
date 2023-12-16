import aoc

tester = aoc.Tester("Parabolic Reflector Dish")

Rocks = list[tuple[int, int]]


def parse_input(data: str) -> tuple[aoc.Grid2D, Rocks]:
    grid: aoc.Grid2D = {}
    rocks: list[tuple[int, int]] = []
    for y, line in enumerate(data.splitlines()):
        for x, c in enumerate(line):
            grid[(x, y)] = c
            if c == "O":
                rocks.append((x, y))

    return grid, rocks


def slide_rock(grid: aoc.Grid2D, pos: tuple[int, int], direction: tuple[int, int]):
    slide_pos = pos
    next_pos = (pos[0] + direction[0], pos[1] + direction[1])
    while next_pos in grid and grid[next_pos] == ".":
        slide_pos = next_pos
        next_pos = (next_pos[0] + direction[0], next_pos[1] + direction[1])

    if pos != slide_pos:
        grid[pos] = "."
        grid[slide_pos] = "O"
    return slide_pos


def slide(grid: aoc.Grid2D, rocks: Rocks, direction: tuple[int, int]) -> tuple[aoc.Grid2D, Rocks]:
    if direction == (0, 1) or direction == (1, 0):
        # if we are moving south or east, we need to reverse the rocks since we are going backwards
        rocks = reversed(rocks)

    new_rocks = []
    for x, y in rocks:
        new_pos = slide_rock(grid, (x, y), direction)
        new_rocks.append(new_pos)

    return grid, sorted(new_rocks)


def cycle(grid: aoc.Grid2D, rocks: Rocks) -> tuple[aoc.Grid2D, Rocks]:
    grid, rocks = slide(grid, rocks, (0, -1))
    grid, rocks = slide(grid, rocks, (-1, 0))
    grid, rocks = slide(grid, rocks, (0, 1))
    grid, rocks = slide(grid, rocks, (1, 0))
    return grid, rocks


def total_load(rocks: Rocks, maxy_y: int) -> int:
    total = 0

    for x, y in rocks:
        total += maxy_y - y + 1

    return total


def total_load_after(grid: aoc.Grid2D, rocks: Rocks, cycles: int) -> int:
    max_y = max(grid, key=lambda pos: pos[1])[1]  # max y value in grid
    cycle_hashes = {}
    cycle_loads = {}
    cycle_count = 0
    for _ in range(cycles):
        grid, rocks = cycle(grid, rocks)
        cycle_count += 1
        grid_hash = hash(frozenset(rocks))

        if grid_hash in cycle_hashes:
            cycle_start = cycle_hashes[grid_hash]
            cycle_size = cycle_count - cycle_start
            extra_cycles = (cycles - cycle_start) % cycle_size
            return cycle_loads[cycle_start + extra_cycles]
        else:
            cycle_hashes[grid_hash] = cycle_count
            cycle_loads[cycle_count] = total_load(rocks, max_y)

    # for small cycle sizes the result is found before any repeats
    return cycle_loads[cycles - 1]


def run_tests(t: aoc.Tester):
    t.test_section("Tests")
    data = aoc.read_input("input_test")
    grid, rocks = parse_input(data)
    max_y = max(grid, key=lambda pos: pos[1])[1]
    grid, rocks = slide(grid, rocks, (0, -1))
    t.test_value(total_load(rocks, max_y), 136)

    grid, rocks = parse_input(data)
    grid_c1, rocks_c1 = parse_input(aoc.read_input("input_test_cycle_1"))
    grid_c2, rocks_c2 = parse_input(aoc.read_input("input_test_cycle_2"))
    grid_c3, rocks_c3 = parse_input(aoc.read_input("input_test_cycle_3"))

    grid, rocks = cycle(grid, rocks)
    t.test_value(set(rocks), set(rocks_c1))

    grid, rocks = cycle(grid, rocks)
    t.test_value(set(rocks), set(rocks_c2))

    grid, rocks = cycle(grid, rocks)
    t.test_value(set(grid), set(grid_c3))

    grid, rocks = parse_input(data)
    load = total_load_after(grid, rocks, 3)
    max_y_c3 = max(grid_c3, key=lambda pos: pos[1])[1]
    t.test_value(load, total_load(rocks_c3, max_y_c3))

    grid, rocks = parse_input(data)
    load = total_load_after(grid, rocks, 1000000000)
    t.test_value(load, 64)


run_tests(tester)

data = aoc.read_input()

tester.test_section("Part 1")
grid, rocks = parse_input(data)
max_y = max(grid, key=lambda pos: pos[1])[1]
grid, rocks = slide(grid, rocks, (0, -1))
solution_1 = total_load(rocks, max_y)
tester.test_solution(solution_1, 109654)

tester.test_section("Part 2")
grid, rocks = parse_input(data)
solution_2 = total_load_after(grid, rocks, 1000000000)
tester.test_solution(solution_2, 94876)
