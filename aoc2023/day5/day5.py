import typing

import aoc

tester = aoc.Tester("If You Give A Seed A Fertilizer")


class Range:
    def __init__(self, start, end):
        self._start = start
        self._end = end

    def __contains__(self, item):
        return self._start <= item < self._end

    def __repr__(self):
        return f"Range({self._start}, {self._end})"

    def overlap(self, other: typing.Self) -> typing.Self:
        if self._start in other:
            return Range(self._start, min(self._end, other._end))
        elif self._end in other:
            return Range(max(self._start, other._start), self._end)
        elif self._start <= other._start and other._end <= self._end:
            return Range(other._start, other._end)
        elif other._start <= self._start and self._end <= other._end:
            return Range(self._start, self._end)
        else:
            return None

    def __lt__(self, other: typing.Self):
        return self._start < other._start

    @property
    def start(self):
        return self._start

    @property
    def end(self):
        return self._end


Alamanac = list[dict[str, str | dict[Range, Range]]]


def parse(data: str) -> tuple[list[int], Alamanac]:
    seeds = []
    alamanac = []
    current = None
    for line in data.split("\n"):
        if line.startswith("seeds:"):
            seeds = list(map(int, line.split(":")[1].strip().split(" ")))
        elif line and line[0].isalpha():
            current = {"map": line, "ranges": {}}
            alamanac.append(current)
        elif line:
            destination_value, source_value, size = list(map(int, line.split(" ")))
            destination_range = Range(destination_value, destination_value + size)
            source_range = Range(source_value, source_value + size)
            current["ranges"][source_range] = destination_range

    return seeds, alamanac


def find_seed_location(seed: int, almanac: Alamanac) -> int:
    seed_map = {}
    seed_map["seed"] = seed
    for entry in almanac:
        current = entry["map"]
        seed_map[current] = None
        for source_range, destination_range in entry["ranges"].items():
            if seed in source_range:
                seed = seed - source_range.start + destination_range.start
                break

        seed_map[current] = seed

    return seed_map[current]


def find_min_seed_location(seeds: list[int], almanac: Alamanac) -> int:
    min_location = None
    for seed in seeds:
        location = find_seed_location(seed, almanac)
        if min_location is None or location < min_location:
            min_location = location
    return min_location


def find_minimum_seed_location_for_range(seed_range: Range, almanac: Alamanac, level: int) -> int:
    if level >= len(almanac):
        return seed_range.start

    mapped_ranges = {}
    for source_range, destination_range in almanac[level]["ranges"].items():
        overlap = seed_range.overlap(source_range)

        if overlap:
            mapped_start = overlap.start - source_range.start + destination_range.start
            mapped_stop = overlap.end - source_range.start + destination_range.start
            mapped_range = Range(mapped_start, mapped_stop)
            mapped_ranges[overlap] = mapped_range

    new_ranges = []
    left = seed_range.start
    for overlap in sorted(mapped_ranges):
        if left < overlap.start <= seed_range.end:
            new_ranges.append(Range(left, overlap.start))
        left = overlap.end

        if left >= seed_range.end:
            break

    if left < seed_range.end:
        new_ranges.append(Range(left, seed_range.end))

    for new_range in new_ranges:
        mapped_ranges[new_range] = new_range

    min_location = None
    for overlap, mapped_range in mapped_ranges.items():
        location = find_minimum_seed_location_for_range(mapped_range, almanac, level + 1)
        if min_location is None or location < min_location:
            min_location = location

    return min_location


def find_seed_range_minimum_location(seeds: list[int], almanac: Alamanac) -> int:
    min_location = None
    for seed, size in aoc.grouper(2, seeds):
        seed_range = Range(seed, seed + size)
        location = find_minimum_seed_location_for_range(seed_range, almanac, 0)
        if min_location is None or location < min_location:
            min_location = location
    return min_location


def run_tests(t: aoc.Tester):
    t.test_section("Tests")
    data = aoc.read_input("input_test")
    seed, almanac = parse(data)

    t.test_value(find_seed_location(79, almanac), 82)
    t.test_value(find_min_seed_location(seed, almanac), 35)
    t.test_value(find_seed_range_minimum_location(seed, almanac), 46)

    r = Range(50, 52)
    t.test(50 in r)
    t.test(51 in r)
    t.test(52 not in r)


run_tests(tester)

data = aoc.read_input()
seeds, almanac = parse(data)

tester.test_section("Part 1")
tester.test_solution(find_min_seed_location(seeds, almanac), 340994526)

tester.test_section("Part 2")
tester.test_greater_than(find_seed_range_minimum_location(seeds, almanac), 30879028)
tester.test_solution(find_seed_range_minimum_location(seeds, almanac), 52210644)
