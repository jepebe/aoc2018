import aoc

tester = aoc.Tester("Trebuchet?!")


def trebuchet(data: str) -> int:
    lines = data.splitlines()
    sum = 0
    for line in lines:
        digits = [int(char) for char in line if char.isdigit()]
        sum += digits[0] * 10 + digits[-1]
    return sum


numbers = (
    ("one", "1"), ("two", "2"), ("three", "3"),
    ("four", "4"), ("five", "5"), ("six", "6"),
    ("seven", "7"), ("eight", "8"), ("nine", "9"),
)


def trebuchet_with_words(data: str) -> int:
    lines = data.splitlines()
    sum = 0
    for line in lines:
        digits = []
        for i in range(len(line)):
            if line[i].isdigit():
                digits.append(int(line[i]))

            for word, number in numbers:
                if line.startswith(word, i):
                    digits.append(int(number))
                    break

        sum += digits[0] * 10 + digits[-1]
    return sum


def run_tests(t: aoc.Tester):
    t.test_section("Tests")
    data = aoc.read_input("input_test")
    result = trebuchet(data)
    tester.test_value(result, 142)

    data = aoc.read_input("input_test_2")
    result = trebuchet_with_words(data)
    tester.test_value(result, 281)

    tester.test_value(trebuchet_with_words("12sevenine"), 19)


run_tests(tester)

data = aoc.read_input()

tester.test_section("Part 1")
tester.test_solution(trebuchet(data), 52974)

tester.test_section("Part 2")
tester.test_less_than(trebuchet_with_words(data), 53370)
tester.test_less_than(trebuchet_with_words(data), 53363)
tester.test_solution(trebuchet_with_words(data), 53340)
