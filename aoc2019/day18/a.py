from collections import deque

import intcode as ic


def read_map(filename):
    grid ={}
    keys = {}
    doors = {}
    entrance = None
    with open(filename) as f:
        y = 0
        for line in f.readlines():
            x = 0
            for c in line.strip():
                grid[(x, y)] = c
                if c.isalpha():
                    if c.islower():
                        keys[(x, y)] = c
                    else:
                        doors[(x, y)] = c
                elif c == '@':
                    entrance = (x, y)

                x += 1
            y += 1
    return grid, keys, doors, entrance


def shortest_path(topo, keys, start):
    full_key_set = ''.join(sorted(keys.values()))
    start_k = ' ' * len(full_key_set)
    dist = {}
    queue = deque([[(start[0], start[1], start_k)]])
    seen = {(start[0], start[1], start_k)}
    while queue:
        path = queue.popleft()
        x, y, k = path[-1]
        dist[(x, y, k)] = len(path) - 1

        if k == full_key_set:
            min_dist = min([dist[d] for d in dist if d[2] == full_key_set])
            return dist, min_dist

        open_doors = [key.upper() for key in k]
        walkable = ['.', '@'] + open_doors + list(full_key_set)

        for d in ((0, -1), (-1, 0), (1, 0), (0, 1)):
            pos = (x + d[0], y + d[1])

            if pos not in topo or topo[pos] not in walkable:
                continue

            nk = k
            cell = topo[pos]
            if cell in full_key_set:
                index = full_key_set.index(cell)
                nk = k[:index] + cell + k[index + 1:]

            posk = (pos[0], pos[1], nk)
            if posk in seen:
                continue

            queue.append(path + [posk])
            seen.add(posk)

    min_dist = min([dist[d] for d in dist if d[2] == full_key_set])
    return dist, min_dist


tester = ic.Tester('vault')

grid, keys, doors, entrance = read_map('test1')

dist, min_dist = shortest_path(grid, keys, entrance)
tester.test_value(min_dist, 8)

grid, keys, doors, entrance = read_map('test2')
dist, min_dist = shortest_path(grid, keys, entrance)
tester.test_value(min_dist, 86)

grid, keys, doors, entrance = read_map('test3')
dist, min_dist = shortest_path(grid, keys, entrance)
tester.test_value(min_dist, 132)

grid, keys, doors, entrance = read_map('test4')
dist, min_dist = shortest_path(grid, keys, entrance)
tester.test_value(min_dist, 136)

grid, keys, doors, entrance = read_map('test5')
dist, min_dist = shortest_path(grid, keys, entrance)
tester.test_value(min_dist, 81)

grid, keys, doors, entrance = read_map('input')
dist, min_dist = shortest_path(grid, keys, entrance)
tester.test_value(min_dist, 0, 'Solution to part 1 %s')

tester.summary()
