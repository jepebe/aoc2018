from itertools import cycle

import sys

lines = sys.stdin.readlines()
shift = cycle([int(l) for l in lines])

f = 0
freq = set()

while f not in freq:
    freq.add(f)
    f += next(shift)

print(f)
