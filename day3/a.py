import sys
import re

lines = sys.stdin.readlines()

fabric = {}

for line in lines:
    _, id, x, y, w, h, _ = re.split(
        '#([0-9]+) @ ([0-9]+),([0-9]+): ([0-9]+)x([0-9]+)', line.strip())

    id = int(id)
    x = int(x)
    y = int(y)
    w = int(w)
    h = int(h)

    for i in range(x, x + w):
        for j in range(y, y + h):
            if not (i, j) in fabric:
                fabric[(i, j)] = [id]
            else:
                fabric[(i, j)].append(id)

# for i in range(8):
#     s = ''
#     for j in range(8):
#         if (i, j) in fabric:
#             l = len(fabric[(i,j)])
#             s += 'x' if l == 1 else 'X'
#         else:
#             s+= '.'
#     print(s)

#print(fabric)
count = 0
for key, value in fabric.items():
    count += 1 if len(value) >= 2 else 0


print(count)
