import aoc

tester = aoc.Tester("Firewall Rules")


def parse_input() -> list[tuple[int, int]]:
    data = aoc.read_input()
    intervals = []
    for line in data.splitlines():
        f, t = list(map(int, line.split(sep="-")))
        intervals.append((f, t))
    return intervals


def merge_intervals(intervals: list[tuple[int, int]]) -> list[tuple[int, int]]:
    n = 1
    while n > 0:
        intervals.sort()
        stack = [intervals[0]]
        for interval in intervals[1:]:
            if stack[-1][0] <= interval[0] <= stack[-1][1]:
                stack[-1] = stack[-1][0], max(stack[-1][1], interval[1])
            else:
                stack.append(interval)
        n = len(intervals) - len(stack)
        intervals = stack
    return stack


def find_gap(intervals: list[tuple[int, int]]) -> int:
    intervals = merge_intervals(intervals)
    for index in range(len(intervals) - 1):
        if intervals[index + 1][0] - intervals[index][1] == 2:
            return intervals[index][1] + 1
    assert False, "No gap found!"


def count_ips(intervals: list[tuple[int, int]], max_ip: int = 9) -> int:
    intervals = merge_intervals(intervals)
    count = 0
    for index in range(len(intervals) - 1):
        count += intervals[index + 1][0] - intervals[index][1] - 1

    count += intervals[0][0]
    count += max_ip - intervals[-1][1]
    return count


def run_tests(t: aoc.Tester):
    t.test_section("Tests")
    intervals = [(5, 8), (0, 2), (4, 7)]
    t.test_value(find_gap(intervals), 3)
    t.test_value(count_ips(intervals), 2)


run_tests(tester)

tester.test_section("Part 1")
tester.test_solution(find_gap(parse_input()), 19449262)

tester.test_section("Part 2")
tester.test_solution(count_ips(parse_input(), max_ip=4294967295), 119)
