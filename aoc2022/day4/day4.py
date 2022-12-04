import typing

import aoc

tester = aoc.Tester("Camp Cleanup")

tester.test_section("Tests")
test_data = """2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8"""


def parse_input(data: str):
    range_pairs = []
    for line in data.splitlines():
        a, b = line.split(sep=",")
        af, at = map(int, a.split(sep="-"))
        bf, bt = map(int, b.split(sep="-"))
        range_pairs.append((af, at, bf, bt))
    return range_pairs


test_pairs = parse_input(test_data)
expected_paris = [(2, 4, 6, 8), (2, 3, 4, 5)]
tester.test_value(test_pairs[:2], [(2, 4, 6, 8), (2, 3, 4, 5)])


def find_complete_overlap_counts(range_pairs: list[typing.Tuple[int, int, int, int]]) -> int:
    overlap_count = 0

    for (af, at, bf, bt) in range_pairs:
        if af <= bf and bt <= at:
            overlap_count += 1
        elif bf <= af and at <= bt:
            overlap_count += 1

    return overlap_count


tester.test_value(find_complete_overlap_counts(test_pairs), 2)


def find_partial_overlap_counts(range_pairs: list[typing.Tuple[int, int, int, int]]) -> int:
    overlap_count = 0

    for (af, at, bf, bt) in range_pairs:
        if af <= bf <= at:
            overlap_count += 1
        elif af <= bt <= at:
            overlap_count += 1
        elif bf <= af <= bt:
            overlap_count += 1
        elif bf <= at <= bt:
            overlap_count += 1

    return overlap_count


tester.test_value(find_partial_overlap_counts(test_pairs), 4)

pairs = parse_input(aoc.read_input())

tester.test_section("Part 1")
tester.test_value(find_complete_overlap_counts(pairs), 602, "solution to part 1=%s")

tester.test_section("Part 2")
tester.test_value(find_partial_overlap_counts(pairs), 891, "solution to part 2=%s")
