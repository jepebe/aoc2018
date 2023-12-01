import aoc

tester = aoc.Tester("Trebuchet?!")


numbers = ("one", "two", "three", "four", "five", "six", "seven", "eight", "nine")


def trebuchet(data: str, include_words: bool = False) -> int:
    lines = data.splitlines()
    sum = 0
    for line in lines:
        digits = []
        for i in range(len(line)):
            if line[i].isdigit():
                digits.append(int(line[i]))

            if include_words:
                for index, word in enumerate(numbers):
                    if line.startswith(word, i):
                        digits.append(int(index + 1))
                        break

        sum += digits[0] * 10 + digits[-1]
    return sum


def run_tests(t: aoc.Tester):
    t.test_section("Tests")
    data = aoc.read_input("input_test")
    result = trebuchet(data)
    tester.test_value(result, 142)

    data = aoc.read_input("input_test_2")
    result = trebuchet(data, True)
    tester.test_value(result, 281)

    tester.test_value(trebuchet("12sevenine", True), 19)


run_tests(tester)

data = aoc.read_input()

tester.test_section("Part 1")
tester.test_solution(trebuchet(data), 52974)

tester.test_section("Part 2")
tester.test_less_than(trebuchet(data, True), 53370)
tester.test_less_than(trebuchet(data, True), 53363)
tester.test_solution(trebuchet(data, True), 53340)
