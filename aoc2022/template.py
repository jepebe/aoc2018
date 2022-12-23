import aoc

tester = aoc.Tester("")


def run_tests(t: aoc.Tester):
    t.test_section("Tests")


run_tests(tester)

data = aoc.read_input()

tester.test_section("Part 1")
tester.test_solution(1, 71502)

tester.test_section("Part 2")
tester.test_solution(2, 208191)
