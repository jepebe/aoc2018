import sys

lines = sys.stdin.readlines()


def counter(line):
    cnts = {}
    for c in line:
        if not c in cnts:
            cnts[c] = 1
        else:
            cnts[c] += 1

    twos = 1 if any([c for c in cnts.values() if c == 2]) else 0
    threes = 1 if any([c for c in cnts.values() if c == 3]) else 0
    return twos, threes


a, b = 0, 0

for line in lines:
    x, y = counter(line)
    a += x
    b += y

print(a * b)
