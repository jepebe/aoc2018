import collections

import aoc

tester = aoc.Tester("An Elephant Named Joseph")


def find_winner(elf_count: int) -> int:
    start = 1
    skip = 2
    n = elf_count
    while n > 2:
        if n % 2 > 0:
            start += skip
        skip *= 2
        n //= 2

    return start


def find_winner_across(elf_count: int) -> int:
    # Naive implementation used to find pattern of tripling
    circle = collections.deque()
    for i in range(elf_count):
        circle.append(i + 1)

    while len(circle) > 1:
        across = len(circle) // 2
        circle.rotate(-across)
        circle.popleft()
        circle.rotate(across - 1)

        if len(circle) % 100000 == 0:
            tester.peek_delta_time(f"{len(circle)}")
    return circle[0]


def find_winner_across_numerically(elf_count: int) -> int:
    multiple = 1
    while multiple < elf_count:
        multiple *= 3
    multiple //= 3
    if elf_count > multiple + multiple:
        return (elf_count - multiple - multiple) * 2 + multiple
    else:
        return elf_count - multiple


def run_tests(t: aoc.Tester):
    t.test_section("Tests")

    t.test_value(find_winner(4), 1)
    t.test_value(find_winner(5), 3)
    t.test_value(find_winner(10), 5)
    t.test_value(find_winner(8), 1)
    t.test_value(find_winner(16), 1)

    t.test_value(find_winner_across(5), 2)
    t.test_value(find_winner_across(6), 3)
    t.test_value(find_winner_across(10), 1)

    t.test_value(find_winner_across_numerically(5), 2)
    t.test_value(find_winner_across_numerically(6), 3)
    t.test_value(find_winner_across_numerically(10), 1)
    t.test_value(find_winner_across_numerically(27), 27)
    t.test_value(find_winner_across_numerically(28), 1)
    t.test_value(find_winner_across_numerically(81), 81)
    t.test_value(find_winner_across_numerically(82), 1)
    t.test_value(find_winner_across_numerically(161), 80)
    t.test_value(find_winner_across_numerically(162), 81)
    t.test_value(find_winner_across_numerically(163), 83)
    t.test_value(find_winner_across_numerically(243), 243)
    t.test_value(find_winner_across_numerically(244), 1)


run_tests(tester)

tester.test_section("Part 1")
tester.test_less_than(find_winner(3001330), 4194301)
tester.test_solution(find_winner(3001330), 1808357)

tester.test_section("Part 2")
tester.test_solution(find_winner_across_numerically(3001330), 1407007)
