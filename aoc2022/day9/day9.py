import aoc

DIRECTIONS = {
    "U": (0, -1),
    "D": (0, 1),
    "L": (-1, 0),
    "R": (1, 0),
}

tester = aoc.Tester("Rope Bridge")

test_data = """R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2"""

test_data_2 = """R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20"""

tester.test_section("Tests")

Grid = dict[tuple[int, int], str]


def parse_input(data: str) -> list[tuple[str, int]]:
    movement = []
    for line in data.splitlines():
        direction, steps = line.split(sep=" ")
        movement.append((direction, int(steps)))

    return movement


def simulate_rope(movement: list[tuple[str, int]], length: int) -> Grid:
    grid = {}
    rope = [(0, 0)] * (length + 1)

    for direction, steps in movement:
        for _ in range(steps):
            dir_vec = DIRECTIONS[direction]
            rope[0] = aoc.add_tuple(rope[0], dir_vec)
            for segment in range(0, length):
                front = rope[segment]
                back = rope[segment + 1]
                delta = aoc.diff_tuple(front, back)
                match (aoc.abs_tuple(delta)):
                    case (2, 1):
                        back = aoc.add_tuple(back, (delta[0] // 2, delta[1]))
                    case (1, 2):
                        back = aoc.add_tuple(back, (delta[0], delta[1] // 2))
                    case (2, 2):
                        back = aoc.add_tuple(back, (delta[0] // 2, delta[1] // 2))
                    case (2, 0):
                        back = aoc.add_tuple(back, (delta[0] // 2, 0))
                    case (0, 2):
                        back = aoc.add_tuple(back, (0, delta[1] // 2))
                    case _:
                        pass

                rope[segment] = front
                rope[segment + 1] = back
                grid[rope[-1]] = "#"

            # state = {}
            # print(f"== {direction} {steps}.{_} ==")
            # for index, seg in enumerate(rope):
            #     state[seg] = str(index)
            # aoc.print_map(state)
    # aoc.print_map(grid)
    return grid


test_grid = parse_input(test_data)
test_rope = simulate_rope(test_grid, 1)
tester.test_value(len(test_rope.values()), 13)

test_rope = simulate_rope(test_grid, 9)
tester.test_value(len(test_rope.values()), 1)

test_grid = parse_input(test_data_2)
test_rope = simulate_rope(test_grid, 9)
tester.test_value(len(test_rope.values()), 36)

tester.test_section("Part 1")
grid = simulate_rope(parse_input(aoc.read_input()), 1)
tester.test_value(len(grid.values()), 6098, "solution to part 1=%s")

tester.test_section("Part 2")
grid = simulate_rope(parse_input(aoc.read_input()), 9)
tester.test_value(len(grid.values()), 2597, "solution to part 2=%s")
