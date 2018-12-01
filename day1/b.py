from itertools import cycle

import sys

lines = sys.stdin.readlines()
shift = cycle(map(int, lines))

f = 0
freq = set()

while f not in freq:
    freq.add(f)
    f += next(shift)

print(f)
