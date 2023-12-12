import aoc

tester = aoc.Tester("Cosmic Expansion")


def parse(data: str, expansion: int) -> aoc.Grid2D:
    lines = data.splitlines()
    skip_rows = []
    for row, line in enumerate(lines):
        if all(c == "." for c in line):
            skip_rows.append(row)

    skip_columns = []
    for column in range(len(lines[0])):
        if all(lines[row][column] == "." for row in range(len(lines))):
            skip_columns.append(column)

    grid: aoc.Grid2D = {}
    y = 0
    for row, line in enumerate(lines):
        if row in skip_rows:
            y += expansion
            continue

        x = 0
        for column, char in enumerate(line):
            if column in skip_columns:
                x += expansion
                continue

            if char != ".":
                grid[(x, y)] = char
            x += 1
        y += 1

    return grid


def manhattan_distances(galaxies: aoc.Grid2D) -> dict[tuple[int, int], int]:
    indexes = {key: index + 1 for index, key in enumerate(galaxies.keys())}
    dist = {}
    for (x1, y1), index in indexes.items():
        for (x2, y2), other_index in indexes.items():
            dist[(index, other_index)] = abs(x1 - x2) + abs(y1 - y2)
    return dist


def sum_galaxy_distances(data: str, expansion: int = 2) -> int:
    galaxies = parse(data, expansion)
    dist = manhattan_distances(galaxies)
    return sum(dist.values()) // 2


def run_tests(t: aoc.Tester):
    t.test_section("Tests")
    data = aoc.read_input("input_test")
    galaxies = parse(data, expansion=2)
    dist = manhattan_distances(galaxies)
    t.test_value(dist[(5, 9)], 9)
    t.test_value(dist[(1, 7)], 15)
    t.test_value(dist[(3, 6)], 17)
    t.test_value(dist[(8, 9)], 5)

    t.test_value(sum_galaxy_distances(data), 374)
    t.test_value(sum_galaxy_distances(data, expansion=10), 1030)
    t.test_value(sum_galaxy_distances(data, expansion=100), 8410)


run_tests(tester)

data = aoc.read_input()

tester.test_section("Part 1")
solution_1 = sum_galaxy_distances(data, expansion=2)
tester.test_solution(solution_1, 9556896)

tester.test_section("Part 2")
solution_2 = sum_galaxy_distances(data, expansion=1000000)
tester.test_solution(solution_2, 685038186836)
