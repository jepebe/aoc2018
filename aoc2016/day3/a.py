import sys

lines = sys.stdin.readlines()

valid = 0
non_valid = 0
for line in lines:
    a, b, c = sorted(map(int, line.strip().split()))

    # print(a, b, c, (a+b) < c)
    if (a + b) <= c:
        non_valid += 1
    else:
        valid += 1

print(valid, non_valid)
