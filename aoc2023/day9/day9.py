import aoc

tester = aoc.Tester("Mirage Maintenance")


def parse(data: str) -> list[list[int]]:
    lines = []
    for line in data.splitlines():
        lines.append([int(x) for x in line.split(" ")])
    return lines


def extrapolate(line: list[int]) -> tuple[int, int]:
    xmat = [line[:]]
    while not all(v == 0 for v in xmat[-1]):
        current_line = xmat[-1]
        xmat.append([])
        for i, value in enumerate(current_line[:-1]):
            difference = current_line[i + 1] - current_line[i]
            xmat[-1].append(difference)

    for n in range(len(xmat) - 1, 0, -1):
        value = xmat[n - 1][-1] + xmat[n][-1]
        xmat[n - 1].append(value)

    for n in range(len(xmat) - 1, 0, -1):
        value = xmat[n - 1][0] - xmat[n][0]
        xmat[n - 1].insert(0, value)

    return xmat[0][0], xmat[0][-1]


def sum_all(lines: list[list[int]]) -> int:
    return sum([extrapolate(line)[1] for line in lines])


def sum_all_beginnings(lines: list[list[int]]) -> int:
    return sum([extrapolate(line)[0] for line in lines])


def run_tests(t: aoc.Tester):
    t.test_section("Tests")
    data = aoc.read_input("input_test")
    lines = parse(data)
    t.test_value(extrapolate(lines[0]), (-3, 18))
    t.test_value(extrapolate(lines[1]), (0, 28))
    t.test_value(extrapolate(lines[2]), (5, 68))

    t.test_value(sum_all(lines), 114)
    t.test_value(sum_all_beginnings(lines), 2)

    t.test_value(extrapolate([-6, -8, -10, -12]), (-4, -14))


run_tests(tester)

data = aoc.read_input()
lines = parse(data)

tester.test_section("Part 1")
solution_1 = sum_all(lines)
tester.test_greater_than(solution_1, 1641934227)
tester.test_solution(solution_1, 1641934234)

tester.test_section("Part 2")
solution_2 = sum_all_beginnings(lines)
tester.test_solution(solution_2, 975)
