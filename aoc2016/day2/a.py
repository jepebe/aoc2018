import sys

lines = sys.stdin.readlines()

DIR = {'U': -3,
       'R': 1,
       'D': 3,
       'L': -1}

key = 5
for line in lines:
    for c in line.strip():
        step = DIR[c]

        if (key + step) < 1 or (key + step) > 9:
            pass
        elif key in (1, 4, 7) and step == -1:
            pass
        elif key in (3, 6, 9) and step == 1:
            pass
        else:
            key += step
    print(key)
