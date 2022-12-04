import aoc

tester = aoc.Tester("")

tester.test_section("Tests")

data = aoc.read_input()

tester.test_section("Part 1")
tester.test_value(1, 71502, "solution to part 1=%s")

tester.test_section("Part 2")
tester.test_value(2, 208191, "solution to part 2=%s")
