import aoc

tester = aoc.Tester("Hot Springs")


def parse(data: str) -> list[tuple[str, tuple[int, ...]]]:
    spring_list = []
    for line in data.splitlines():
        springs, groups = line.split(" ")
        groups = tuple(map(int, groups.split(",")))
        spring_list.append((springs, groups))

    return spring_list


def find_combos(memo: dict, springs: str, groups: tuple[int, ...], current: int) -> int:
    if (springs, groups, current) in memo:
        return memo[(springs, groups, current)]

    if springs == "" and len(groups) > 0:  # springs is empty but groups is not
        return 0

    if "#" in springs and groups == ():  # at least one spring remains but groups is empty
        return 0

    if groups == ():  # springs is either empty or only contains dots and question marks
        return 1

    if springs[0] == ".":
        if current == groups[0]:  # finish last group
            return find_combos(memo, springs[1:], groups[1:], 0)
        elif 0 < current < groups[0]:  # group does not match current size
            return 0
        else:
            return find_combos(memo, springs[1:], groups, 0)  # skip dot

    if springs[0] == "#":
        if current == groups[0]:  # current group will be too large
            return 0
        elif current < groups[0]:  # extend group
            return find_combos(memo, springs[1:], groups, current + 1)
        else:
            raise Exception("This should not happen")

    if springs[0] == "?":
        # we will see what happens if we extend the group and if we skip the dot
        extend = find_combos(memo, "#" + springs[1:], groups, current)
        end = find_combos(memo, "." + springs[1:], groups, current)
        memo[(springs, groups, current)] = extend + end
        return extend + end


def find_combos_unfolded(springs: str, groups: tuple[int, ...]) -> int:
    springs = "?".join([springs for _ in range(5)]) + "."
    return find_combos({}, springs, groups * 5, 0)


def find_all_combos(spring_list: list[tuple[str, tuple[int, ...]]]) -> int:
    total = 0
    for springs, groups in spring_list:
        total += find_combos({}, springs + ".", groups, 0)
    return total


def find_all_combos_unfolded(spring_list: list[tuple[str, tuple[int, ...]]]) -> int:
    total = 0
    for springs, groups in spring_list:
        total += find_combos_unfolded(springs, groups)
    return total


def run_tests(t: aoc.Tester):
    t.test_section("Tests")
    data = aoc.read_input("input_test")
    springs = parse(data)

    t.test_value(find_combos({}, springs[0][0] + ".", springs[0][1], 0), 1)
    t.test_value(find_combos({}, springs[1][0] + ".", springs[1][1], 0), 4)
    t.test_value(find_combos({}, springs[2][0] + ".", springs[2][1], 0), 1)
    t.test_value(find_combos({}, springs[3][0] + ".", springs[3][1], 0), 1)
    t.test_value(find_combos({}, springs[4][0] + ".", springs[4][1], 0), 4)
    t.test_value(find_combos({}, springs[5][0] + ".", springs[5][1], 0), 10)

    t.test_value(find_all_combos(springs), 21)

    t.test_value(find_combos_unfolded(springs[0][0], springs[0][1]), 1)
    t.test_value(find_combos_unfolded(springs[1][0], springs[1][1]), 16384)
    t.test_value(find_combos_unfolded(springs[2][0], springs[2][1]), 1)
    t.test_value(find_combos_unfolded(springs[3][0], springs[3][1]), 16)
    t.test_value(find_combos_unfolded(springs[4][0], springs[4][1]), 2500)
    t.test_value(find_combos_unfolded(springs[5][0], springs[5][1]), 506250)

    t.test_value(find_all_combos_unfolded(springs), 525152)


run_tests(tester)

spring_records = parse(aoc.read_input())

tester.test_section("Part 1")
solution_1 = find_all_combos(spring_records)
tester.test_solution(solution_1, 6949)

tester.test_section("Part 2")
solution_2 = find_all_combos_unfolded(spring_records)
tester.test_solution(solution_2, 51456609952403)
