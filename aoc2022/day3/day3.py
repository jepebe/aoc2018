import aoc

tester = aoc.Tester("Rucksack Reorganization")

test_data = """vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw"""

tester.test_section("Tests")


def split_sack(sack):
    half = len(sack) // 2
    return sack[:half], sack[half:]


tester.test_value(split_sack("vJrwpWtwJgWrhcsFMMfFFhFp")[0], "vJrwpWtwJgWr")


def find_repeat_item(left, right):
    return set(left).intersection(set(right)).pop()


tester.test_value(find_repeat_item("vJrwpWtwJgWr", "hcsFMMfFFhFp"), "p")


def find_incorrect_item_score(data):
    priorities = " abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    score = 0
    for sack in data.split(sep="\n"):
        l, r = split_sack(sack)
        item = find_repeat_item(l, r)
        score += priorities.index(item)
    return score


tester.test_value(find_incorrect_item_score(test_data), 157)


def find_triple_badge_score(data):
    priorities = " abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    sacks = [sack for sack in data.split(sep="\n")]
    score = 0
    for a, b, c in aoc.grouper(3, sacks):
        badge = set.intersection(set(a), set(b), set(c)).pop()
        score += priorities.index(badge)
    return score


tester.test_value(find_triple_badge_score(test_data), 70)

with open("input") as f:
    data = f.read()

tester.test_section("Part 1")
tester.test_value(find_incorrect_item_score(data), 7889, "solution to part 1=%s")

tester.test_section("Part 2")
tester.test_value(find_triple_badge_score(data), 2825, "solution to part 2=%s")
