import itertools
from typing import List

import intcode as ic


def parse_seating(lines: List[str]):
    seating = {}
    names = set()
    for line in lines:
        line = line.replace(" happiness units by sitting next to ", ' ')
        line = line.replace(" would lose ", ' -')
        line = line.replace(" would gain ", ' ')
        line = line.replace(".", '')
        src, units, dst = line.split()
        names.add(src)
        seating[(src, dst)] = int(units)
    return seating, list(names)


def happiness(names, happiness_units):
    happiness_sum = 0
    for i, src in enumerate(names):
        happiness_sum += happiness_units[(src, names[i - 1])]
        happiness_sum += happiness_units[(src, names[(i + 1) % len(names)])]

    return happiness_sum


def find_best_seating(names, happiness_units):
    best_score = -999999999
    best_seating = None
    for perm in itertools.permutations(names):
        score = happiness(perm, happiness_units)
        if score > best_score:
            best_score = score
            best_seating = perm
    return best_score, best_seating


tester = ic.Tester('Knights of the Dinner Table')

units = """Alice would gain 54 happiness units by sitting next to Bob.
Alice would lose 79 happiness units by sitting next to Carol.
Alice would lose 2 happiness units by sitting next to David.
Bob would gain 83 happiness units by sitting next to Alice.
Bob would lose 7 happiness units by sitting next to Carol.
Bob would lose 63 happiness units by sitting next to David.
Carol would lose 62 happiness units by sitting next to Alice.
Carol would gain 60 happiness units by sitting next to Bob.
Carol would gain 55 happiness units by sitting next to David.
David would gain 46 happiness units by sitting next to Alice.
David would lose 7 happiness units by sitting next to Bob.
David would gain 41 happiness units by sitting next to Carol.
"""

happiness_units, _ = parse_seating(units.splitlines())
optimal_order = ['Alice', 'Bob', 'Carol', 'David']
tester.test_value(happiness(optimal_order, happiness_units), 330)

with open('input') as f:
    lines = f.readlines()

happiness_units, names = parse_seating(lines)
_, best_seating = find_best_seating(names, happiness_units)
happiness_1 = happiness(best_seating, happiness_units)
tester.test_value(happiness_1, 618, 'solution to exercise 1 = %s')

for name in names:
    happiness_units[(name, 'Jean-Paul')] = 0
    happiness_units[('Jean-Paul', name)] = 0
names.append('Jean-Paul')

_, best_seating = find_best_seating(names, happiness_units)
happiness_1 = happiness(best_seating, happiness_units)
tester.test_value(happiness_1, 601, 'solution to exercise 2 = %s')
