import sys
import re

lines = sys.stdin.readlines()

fabric = {}
ids = set()
overlap = set()

for line in lines:
    _, id, x, y, w, h, _ = re.split(
        '#([0-9]+) @ ([0-9]+),([0-9]+): ([0-9]+)x([0-9]+)', line.strip())

    id = int(id)
    x = int(x)
    y = int(y)
    w = int(w)
    h = int(h)

    ids.add(id)

    for i in range(x, x + w):
        for j in range(y, y + h):
            if not (i, j) in fabric:
                fabric[(i, j)] = [id]
            else:
                fabric[(i, j)].append(id)

                for idd in fabric[(i,j)]:
                    overlap.add(idd)


#print(overlap)
#print(ids)
print(ids.difference(overlap))