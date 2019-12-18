from collections import deque, defaultdict
from itertools import combinations

import intcode as ic


def read_map(filename):
    grid = {}
    keys = {}
    doors = {}
    entrance = []
    with open(filename) as f:
        y = 0
        for line in f.readlines():
            x = 0
            for c in line.strip():
                pos = (x, y)
                grid[pos] = c
                if c.isalpha():
                    if c.islower():
                        keys[pos] = c
                    else:
                        doors[pos] = c
                elif c == '@':
                    entrance.append(pos)

                x += 1
            y += 1
    return grid, keys, doors, entrance


def shortest_path(topo, keys, start):
    full_key_set = ''.join(sorted(keys.values()))
    start_k = ' ' * len(full_key_set)
    dist = {}
    queue = deque([[(start[0], start[1], start_k)]])
    seen = {(start[0], start[1], start_k)}
    skipped = 0
    count = 0
    while queue:
        path = queue.popleft()
        x, y, k = path[-1]
        dist[(x, y, k)] = len(path) - 1

        # if k == full_key_set:
        #     min_dist = min([dist[d] for d in dist if d[2] == full_key_set])
        #     return dist, min_dist
        closed_doors = [key.upper() for key in full_key_set if key not in k]

        for d in ((0, -1), (-1, 0), (1, 0), (0, 1)):
            count += 1
            pos = (x + d[0], y + d[1])

            if pos not in topo:
                continue

            cell = topo[pos]
            if cell == '#':
                continue

            if cell in closed_doors:
                continue

            nk = k

            if cell in full_key_set:
                index = full_key_set.index(cell)
                nk = k[:index] + cell + k[index + 1:]

            posk = (pos[0], pos[1], nk)
            if posk in seen:
                skipped += 1
                continue

            queue.append(path + [posk])
            seen.add(posk)
    print(f'skipped {skipped}/{count} seen {len(seen)}')
    min_dist = min([dist[d] for d in dist if d[2] == full_key_set])
    return dist, min_dist


def reachable_keys(grid, keys, start, pocket):
    open_doors = [p.upper() for p in pocket]
    walkable = ['.', '@'] + list(sorted(keys.values())) + open_doors
    dist = ic.bfs(grid, start, walkable=walkable)

    return [(key, keys[key], dist[key]) for key in keys if key in dist]


def find_path(grid, keys, start, pocket=None, length=0, memo=None):
    available_keys = reachable_keys(grid, keys, start, pocket)
    full_key_set = ''.join(sorted(keys.values()))

    if pocket == full_key_set:
        memo[(start, pocket)] = length
    else:
        for key in [k for k in available_keys if k[1] not in pocket]:
            index = full_key_set.index(key[1])
            np = pocket[:index] + key[1] + pocket[index + 1:]

            kp = (key[0], pocket)
            if kp not in memo or memo[kp] > length + key[2]:
                memo[kp] = length + key[2]
                find_path(grid, keys, key[0], np, length + key[2], memo)


def shortest_path(grid, keys, start):
    full_key_set = ''.join(sorted(keys.values()))
    memo = {}
    find_path(grid, keys, start, ' ' * len(keys), 0, memo)
    min_dist = min([memo[d] for d in memo if d[1] == full_key_set])
    # print(memo)
    return memo, min_dist


def short_path(topo, start, end):
    queue = deque([[(start[0], start[1], '')]])
    seen = {(start[0], start[1], '')}
    while queue:
        path = queue.popleft()
        x, y, doors = path[-1]

        if (x, y) == end:
            return len(path) - 1, doors

        for d in ((0, -1), (-1, 0), (1, 0), (0, 1)):
            pos = (x + d[0], y + d[1])

            if pos not in topo:
                continue

            cell = topo[pos]
            if cell == '#':
                continue

            if pos in seen:
                continue

            is_door = cell.isalpha() and cell.isupper()

            queue.append(path + [(pos[0], pos[1], doors + cell if is_door else doors)])
            seen.add(pos)
    return None, None


def shortest_path(grid, keys, start):
    graph = {keys[key]: {} for key in keys}
    graph['@'] = {}

    for key in keys:
        length, doors = short_path(grid, start, key)
        graph['@'][keys[key]] = {'length': length, 'doors': doors}
        graph[keys[key]]['@'] = {'length': length, 'doors': doors}

    for a, b in combinations(keys.keys(), 2):
        length, doors = short_path(grid, a, b)
        graph[keys[a]][keys[b]] = {'length': length, 'doors': doors}
        graph[keys[b]][keys[a]] = {'length': length, 'doors': doors}
    print(graph)
    return None, None


tester = ic.Tester('vault')

grid, keys, doors, entrance = read_map('test1')

dist, min_dist = shortest_path(grid, keys, entrance[0])
tester.test_value(min_dist, 8)

grid, keys, doors, entrance = read_map('test2')
dist, min_dist = shortest_path(grid, keys, entrance[0])
tester.test_value(min_dist, 86)

grid, keys, doors, entrance = read_map('test3')
dist, min_dist = shortest_path(grid, keys, entrance[0])
tester.test_value(min_dist, 132)

grid, keys, doors, entrance = read_map('test4')
dist, min_dist = shortest_path(grid, keys, entrance[0])
tester.test_value(min_dist, 136)

grid, keys, doors, entrance = read_map('test5')
dist, min_dist = shortest_path(grid, keys, entrance[0])
tester.test_value(min_dist, 81)

# grid, keys, doors, entrance = read_map('input')
# dist, min_dist = shortest_path(grid, keys, entrance[0])
# tester.test_value(min_dist, 5402, 'Solution to part 1 %s')

tester.summary()
