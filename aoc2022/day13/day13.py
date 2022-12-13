import functools

import aoc

tester = aoc.Tester("Distress Signal")


def run_tests(t: aoc.Tester):
    t.test_section("Tests")
    pairs = yield_pairs("test_input")
    a, b = next(pairs)
    t.test_value(a, [1, 1, 3, 1, 1])
    t.test_value(b, [1, 1, 5, 1, 1])
    t.test_value(compare(a, b), 1)

    a, b = next(pairs)
    t.test_value(a, [[1], [2, 3, 4]])
    t.test_value(b, [[1], 4])
    t.test_value(compare(a, b), 1)

    a, b = next(pairs)
    t.test_value(a, [9])
    t.test_value(b, [[8, 7, 6]])
    t.test_value(compare(a, b), -1)

    a, b = next(pairs)
    t.test_value(a, [[4, 4], 4, 4])
    t.test_value(b, [[4, 4], 4, 4, 4])
    t.test_value(compare(a, b), 1)

    a, b = next(pairs)
    t.test_value(a, [7, 7, 7, 7])
    t.test_value(b, [7, 7, 7])
    t.test_value(compare(a, b), -1)

    a, b = next(pairs)
    t.test_value(a, [])
    t.test_value(b, [3])
    t.test_value(compare(a, b), 1)

    a, b = next(pairs)
    t.test_value(a, [[[]]])
    t.test_value(b, [[]])
    t.test_value(compare(a, b), -1)

    a, b = next(pairs)
    t.test_value(a, [1, [2, [3, [4, [5, 6, 7]]]], 8, 9])
    t.test_value(b, [1, [2, [3, [4, [5, 6, 0]]]], 8, 9])
    t.test_value(compare(a, b), -1)

    a = [[1], [2, 3, 4]]
    b = [[1], 2, 3, 4]
    t.test_value(compare(a, b), -1)

    a = [7, 6, 8, 9, 6]
    b = [7, 6, 8, 9]
    t.test_value(compare(a, b), -1)

    a = [[1, 2], 4]
    b = [[1, 2], 3]
    t.test_value(compare(a, b), -1)

    a = [[1, 2], 3]
    b = [[1, 2], 3]
    t.test_value(compare(a, b), 0)

    t.test_value(calculate_pair_sum("test_input"), 13)
    t.test_value(find_decoder_key("test_input"), 140)


def parse_line(line: str):
    item_stack = [[]]
    number = ""
    for c in line:
        match c:
            case "[":
                new_list = []
                item_stack[-1].append(new_list)
                item_stack.append(new_list)
            case "]":
                if number:
                    item_stack[-1].append(int(number))
                number = ""
                item_stack.pop()
            # case "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9":
            case str(num) if "0" <= num <= "9":
                number += c
            case ",":
                if number:
                    item_stack[-1].append(int(number))
                number = ""
            case _:
                print(f"what?")

    return item_stack[0][0]


def yield_pairs(filename: str):
    data = aoc.read_input(filename)
    lines = [line for line in data.splitlines() if line.strip()]
    for a, b in aoc.grouper(2, lines):
        yield parse_line(a), parse_line(b)


def compare(left, right) -> int:
    for index in range(max(len(left), len(right))):
        if index >= len(left):
            return 1
        if index >= len(right):
            return -1

        match left[index], right[index]:
            case list(l), list(r):
                cmp = compare(l, r)
                if cmp != 0:
                    return cmp
            case list(l), int(r):
                cmp = compare(l, [r])
                if cmp != 0:
                    return cmp
            case int(l), list(r):
                cmp = compare([l], r)
                if cmp != 0:
                    return cmp
            case int(l), int(r):
                if l < r:
                    return 1
                elif l > r:
                    return -1
    return 0


def calculate_pair_sum(filename):
    pair_sum = 0
    for index, (a, b) in enumerate(yield_pairs(filename), start=1):
        if compare(a, b) >= 0:
            pair_sum += index
    return pair_sum


def find_decoder_key(filename):
    data = aoc.read_input(filename)
    messages = [parse_line(msg) for msg in data.splitlines() if msg.strip()]
    # insert divider packets
    messages.append([[2]])
    messages.append([[6]])

    messages = list(sorted(messages, key=functools.cmp_to_key(compare), reverse=True))
    return (messages.index([[2]]) + 1) * (messages.index([[6]]) + 1)


run_tests(tester)

tester.test_section("Part 1")
tester.test_value(calculate_pair_sum("input"), 6086, "solution to part 1=%s")

tester.test_section("Part 2")
tester.test_value(find_decoder_key("input"), 27930, "solution to part 2=%s")
