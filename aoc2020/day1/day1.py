import itertools

import intcode as ic


def find_pair(elt):
    pairs = itertools.combinations(elt, 2)
    for pair in pairs:
        if sum(pair) == 2020:
            return pair[0] * pair[1]


def find_triplet(elt):
    triplets = itertools.combinations(elt, 3)
    for triplet in triplets:
        if sum(triplet) == 2020:
            return triplet[0] * triplet[1] * triplet[2]


data = [1721, 979, 366, 299, 675, 1456]

tester = ic.Tester('Report Repair')

tester.test_value(find_pair(data), 514579)
tester.test_value(find_triplet(data), 241861950)

with open('input') as f:
    lines = f.readlines()

data = [int(e) for e in lines]

tester.test_value(find_pair(data), 982464, "solution to exercise 1=%s")
tester.test_value(find_triplet(data), 162292410, "solution to exercise 2=%s")
