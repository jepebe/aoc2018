import sys

lines = sys.stdin.readlines()

lines = [line.strip() for line in lines]


def is_valid(a, b, c):
    a, b, c = sorted([a, b, c])
    return (a + b) > c


valid = 0
for index in range(0, len(lines), 3):
    l1 = lines[index]
    l2 = lines[index + 1]
    l3 = lines[index + 2]
    a1, a2, a3 = map(int, l1.split())
    b1, b2, b3 = map(int, l2.split())
    c1, c2, c3 = map(int, l3.split())

    valid += 1 if is_valid(a1, b1, c1) else 0
    valid += 1 if is_valid(a2, b2, c2) else 0
    valid += 1 if is_valid(a3, b3, c3) else 0

print(valid)
