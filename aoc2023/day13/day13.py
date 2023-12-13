import aoc

tester = aoc.Tester("Point of Incidence")

Pattern = dict[tuple[int, int], bool]


def parse(data: str) -> list[Pattern]:
    patterns = []
    pattern = {}
    y = 0
    for line in data.splitlines():
        if line == "":
            y = 0
            patterns.append(pattern)
            pattern = {}
            continue

        for x, c in enumerate(line):
            if c == "#":
                pattern[(x, y)] = True
        y += 1

    patterns.append(pattern)
    return patterns


def is_reflected_horizontal(y: int, width: int, cols: int, pattern: Pattern) -> bool:
    for x in range(cols + 1):
        if (x, y - width) in pattern and (x, y + width + 1) in pattern:
            continue
        elif (x, y - width) not in pattern and (x, y + width + 1) not in pattern:
            continue
        else:
            return False
    return True


def is_reflected_vertical(x: int, width: int, rows: int, pattern: Pattern) -> bool:
    for y in range(rows + 1):
        if (x - width, y) in pattern and (x + width + 1, y) in pattern:
            continue
        elif (x - width, y) not in pattern and (x + width + 1, y) not in pattern:
            continue
        else:
            return False
    return True


def find_reflection(pattern: Pattern, exclude: tuple[str, int, int] = None) -> tuple[str, int, int]:
    minx, maxx, miny, maxy = aoc.find_extents(pattern)
    # horizontal check
    horizontal = 0, 0
    for row in range(miny, maxy + 1):
        width = 0
        while is_reflected_horizontal(row, width, maxx - minx, pattern) and width < maxy - miny:
            width += 1

        if (row - width < 0 or row + width >= maxy) and width > 0 and width > horizontal[1]:
            if exclude is not None and exclude[:2] == ("h", row):
                continue
            horizontal = row, width

    # vertical check
    vertical = 0, 0
    for col in range(minx, maxx + 1):
        width = 0
        while is_reflected_vertical(col, width, maxy - miny, pattern) and width < maxx - minx:
            width += 1

        if (col - width < 0 or col + width >= maxx) and width > 0 and width > vertical[1]:
            if exclude is not None and exclude[:2] == ("v", col):
                continue
            vertical = col, width

    if horizontal[1] > vertical[1]:
        return "h", horizontal[0], horizontal[1]
    elif horizontal[1] < vertical[1]:
        return "v", vertical[0], vertical[1]
    else:
        return "n", 0, 0


def smudge(pattern: Pattern) -> tuple[str, int, int]:
    exclude = find_reflection(pattern)
    result = None
    for x, y, value in aoc.iterate_grid(pattern):
        if value is None:
            pattern[(x, y)] = True
        else:
            del pattern[(x, y)]

        direction, index, width = find_reflection(pattern, exclude=exclude)

        if result is not None and direction != "n" and result != (direction, index, width):
            print(exclude, result, direction, index, width)
            aoc.print_map(pattern, func=lambda x, g: "#", missing=".")

        if result is None and direction != "n":
            result = direction, index, width

        if value is None:
            del pattern[(x, y)]
        else:
            pattern[(x, y)] = True
    return result


def summarize(patterns: list[Pattern]) -> int:
    summary = 0
    for pattern in patterns:
        direction, index, width = find_reflection(pattern)

        if direction == "v":
            summary += index + 1
        elif direction == "h":
            summary += (index + 1) * 100
    return summary


def smudge_summarize(patterns: list[Pattern]) -> int:
    summary = 0
    for pattern in patterns:
        direction, index, width = smudge(pattern)

        if direction == "v":
            summary += index + 1
        elif direction == "h":
            summary += (index + 1) * 100
    return summary


def run_tests(t: aoc.Tester):
    t.test_section("Tests")
    data = aoc.read_input("input_test")
    patterns = parse(data)

    t.test_value(find_reflection(patterns[0]), ("v", 4, 4))
    t.test_value(find_reflection(patterns[1]), ("h", 3, 3))
    t.test_value(summarize(patterns), 405)

    t.test_value(smudge(patterns[0]), ("h", 2, 3))
    t.test_value(smudge(patterns[1]), ("h", 0, 1))
    t.test_value(smudge_summarize(patterns), 400)

    data = aoc.read_input("input_test_1")
    patterns = parse(data)
    t.test_value(find_reflection(patterns[0]), ("v", 0, 1))

    t.test_section("Test JIB")
    data = aoc.read_input("input_test_jib")
    patterns = parse(data)
    t.test_value(smudge(patterns[0]), ("v", 7, 8))


run_tests(tester)

data = aoc.read_input()
patterns = parse(data)

tester.test_section("Part 1")
solution_1 = summarize(patterns)
tester.test_greater_than(solution_1, 24043)
tester.test_greater_than(solution_1, 25394)
tester.test_less_than(solution_1, 28165)
tester.test_value_neq(solution_1, 27189)
tester.test_solution(solution_1, 27742)

tester.test_section("Part 2")
solution_2 = smudge_summarize(patterns)
tester.test_greater_than(solution_2, 32337)
tester.test_solution(solution_2, 32728)
