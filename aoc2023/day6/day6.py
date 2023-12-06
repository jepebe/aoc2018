import aoc

tester = aoc.Tester("Wait For It")


def win_all_races(races: tuple[tuple[int, int], ...]) -> int:
    ways = 1
    for length, record in races:
        winning_edge = find_winning_edge(0, length, length, record)
        losing_edges = find_losing_edge(0, length, length, record)
        ways *= losing_edges - winning_edge
    return ways


def find_winning_edge(start: int, end: int, length: int, record: int) -> int:
    """The edge where we start winning."""
    if start == end:
        return start

    pos = (start + end) // 2
    if pos * (length - pos) > record:
        return find_winning_edge(start, pos, length, record)
    else:
        return find_winning_edge(pos + 1, end, length, record)


def find_losing_edge(start: int, end: int, length: int, record: int) -> int:
    """The edge where we start losing again."""
    if start == end:
        return start

    pos = (start + end) // 2
    if pos * (length - pos) > record:
        return find_losing_edge(pos + 1, end, length, record)
    else:
        return find_losing_edge(start, pos, length, record)


def run_tests(t: aoc.Tester):
    t.test_section("Tests")
    t.test_value(find_winning_edge(0, 7, 7, 9), 2)
    t.test_value(find_losing_edge(0, 7, 7, 9), 6)

    t.test_value(find_winning_edge(0, 15, 15, 40), 4)
    t.test_value(find_losing_edge(0, 15, 15, 40), 12)

    t.test_value(find_winning_edge(0, 30, 30, 200), 11)
    t.test_value(find_losing_edge(0, 30, 30, 200), 20)

    t.test_value(win_all_races(((7, 9), (15, 40), (30, 200))), 288)
    t.test_value(win_all_races(((71530, 940200),)), 71503)


run_tests(tester)

tester.test_section("Part 1")
races = ((60, 601), (80, 1163), (86, 1559), (76, 1300))
tester.test_solution(win_all_races(races), 1155175)

tester.test_section("Part 2")
tester.test_solution(win_all_races(((60808676, 601116315591300),)), 35961505)
