import collections
import math

import aoc

tester = aoc.Tester("Scrambled Letters and Hash")


def read_operations(filename: str = "input") -> list[str]:
    return aoc.read_input(filename).splitlines()


def swap(items: collections.deque, p1: int, p2: int):
    temp = items[p1]
    items[p1] = items[p2]
    items[p2] = temp


def scramble(password: str, ops: list[str]) -> str:
    items = collections.deque(password)
    for op in ops:
        match op.split(sep=" "):
            case ["swap", "position", p1, "with", "position", p2]:
                p1 = int(p1)
                p2 = int(p2)
                swap(items, p1, p2)
            case ["swap", "letter", p1, "with", "letter", p2]:
                p1 = items.index(p1)
                p2 = items.index(p2)
                swap(items, p1, p2)
            case ["reverse", "positions", p1, "through", p2]:
                p1 = int(p1)
                p2 = int(p2)
                half = math.ceil((p2 - p1) / 2)
                for f, t in zip(range(p1, p1 + half + 1), range(p2, p1 + half - 1, -1)):
                    swap(items, f, t)
            case ["rotate", "left", p1, *_]:
                items.rotate(-int(p1))
            case ["rotate", "right", p1, *_]:
                items.rotate(int(p1))
            case ["move", "position", p1, "to", "position", p2]:
                p1 = int(p1)
                p2 = int(p2)
                item = items[p1]
                del items[p1]
                items.insert(p2, item)
            case ["rotate", "based", "on", "position", "of", "letter", letter]:
                index = items.index(letter)
                items.rotate(1)
                items.rotate(index)
                if index >= 4:
                    items.rotate(1)
            case rest:
                print(rest)
                assert False, f"Unhandled case {rest}"
        # print("".join(items))
    return "".join(items)


def unscramble(password: str, ops: list[str]) -> str:
    reverse_map = {
        0: -1,
        1: -1,
        2: 2,
        3: -2,
        4: 1,
        5: -3,
        6: 0,
        7: -4,
    }
    items = collections.deque(password)
    for op in reversed(ops):
        match op.split(sep=" "):
            case ["swap", "position", p1, "with", "position", p2]:
                p1 = int(p1)
                p2 = int(p2)
                swap(items, p1, p2)
            case ["swap", "letter", p1, "with", "letter", p2]:
                p1 = items.index(p1)
                p2 = items.index(p2)
                swap(items, p1, p2)
            case ["reverse", "positions", p1, "through", p2]:
                p1 = int(p1)
                p2 = int(p2)
                half = math.ceil((p2 - p1) / 2)
                for f, t in zip(range(p1, p1 + half + 1), range(p2, p1 + half - 1, -1)):
                    swap(items, f, t)
            case ["rotate", "left", p1, *_]:
                items.rotate(int(p1))
            case ["rotate", "right", p1, *_]:
                items.rotate(-int(p1))
            case ["move", "position", p1, "to", "position", p2]:
                p1 = int(p1)
                p2 = int(p2)
                item = items[p2]
                del items[p2]
                items.insert(p1, item)
            case ["rotate", "based", "on", "position", "of", "letter", letter]:
                index = items.index(letter)
                items.rotate(reverse_map[index])
            case rest:
                print(rest)
                assert False, f"Unhandled case {rest}"
        # print("".join(items))
    return "".join(items)


def run_tests(t: aoc.Tester):
    t.test_section("Tests")

    t.test_value(scramble("abcde", read_operations("test_input")), "decab")
    t.test_value(unscramble("decab", read_operations("test_input")), "abcde")
    t.test_value(unscramble("gbhcefad", read_operations("input")), "abcdefgh")


run_tests(tester)

tester.test_section("Part 1")
tester.test_solution(scramble("abcdefgh", read_operations()), "gbhcefad")

tester.test_section("Part 2")
tester.test_solution(unscramble("fbgdceah", read_operations("input")), "gahedfcb")
