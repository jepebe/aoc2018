import sys
import itertools

lines = map(str.strip, sys.stdin.readlines())

comb = itertools.combinations(lines, 2)


def diff(a, b):
    count = 0
    common = ''
    x = zip(a, b)
    for a, b in x:
        count += 1 if a != b else 0
        common += a if a == b else ''
    return count, common


for a, b in comb:
    count, common = diff(a, b)

    if count < 2:
        print(count, common)
