from heapq import heappop, heappush
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


def short_path(topo, start, end):
    def neighbours(grid, pos):
        doors = pos[1]
        pos = pos[0]
        for d in ((0, -1), (-1, 0), (1, 0), (0, 1)):
            npos = (pos[0] + d[0], pos[1] + d[1])

            if npos not in grid or grid[npos] == '#':
                continue

            cell = grid[npos]
            is_door = cell.isalpha() and cell.isupper()

            yield npos, doors + cell if is_door else doors

    def cmp(value):
        return value[0]

    def meta(length, node):
        return length, node[1]

    result = ic.bfsf(topo, (start, ''), end, neighbours, cmp=cmp, meta=meta)

    if result is None:
        return 9999, '#'
    return result


def create_graph(grid, keys, entrances):
    graph = {keys[key]: {} for key in keys}

    for index, entrance in enumerate(entrances):
        entrance_node = f'@{index}'
        graph[entrance_node] = {}
        for key in keys:
            length, doors = short_path(grid, entrance, key)
            graph[entrance_node][keys[key]] = {'length': length, 'doors': doors}

    for a, b in combinations(keys.keys(), 2):
        length, doors = short_path(grid, a, b)
        graph[keys[a]][keys[b]] = {'length': length, 'doors': doors}
        graph[keys[b]][keys[a]] = {'length': length, 'doors': doors}

    return graph


def graph_dijkstra(graph, start, full_key_set):
    queue = [(0, ' ' * len(full_key_set), start)]
    dist = {(start, ' ' * len(full_key_set)): 0}
    parent = {}

    while queue:
        length, keys, node = heappop(queue)

        if dist.get((node, keys), 99999) < length:
            continue

        for neighbour in graph[node]:
            if neighbour == '@':
                continue

            doors = graph[node][neighbour]['doors']
            index = full_key_set.index(neighbour)
            new_keys = keys[:index] + neighbour + keys[index + 1:]
            if any(door.lower() not in new_keys for door in doors):
                continue

            n_length = length + graph[node][neighbour]['length']
            if n_length < dist.get((neighbour, new_keys), 99999):
                dist[(neighbour, new_keys)] = n_length
                heappush(queue, (n_length, new_keys, neighbour))
                parent[(neighbour, new_keys)] = (node, keys)

    min_length = min(dist[d] for d in dist if d[1] == full_key_set)
    return dist, parent, min_length


def graph_qdijkstra(graph, start, full_key_set):
    queue = [(0, ' ' * len(full_key_set), start[0], start[1], start[2], start[3])]
    dist = {(start[0], start[1], start[2], start[3], ' ' * len(full_key_set)): 0}
    parent = {}

    while queue:
        length, keys, n0, n1, n2, n3 = heappop(queue)

        if dist.get((n0, n1, n2, n3, keys), 99999) < length:
            continue

        for node_index, node in enumerate((n0, n1, n2, n3)):
            for neighbour in graph[node]:
                if neighbour == start:
                    continue

                doors = graph[node][neighbour]['doors']
                index = full_key_set.index(neighbour)
                new_keys = keys[:index] + neighbour + keys[index + 1:]
                if any(door.lower() not in new_keys for door in doors):
                    continue

                n_length = length + graph[node][neighbour]['length']

                nodes = [n0, n1, n2, n3]
                nodes[node_index] = neighbour
                nodes = tuple(nodes)

                if n_length < dist.get((*nodes, new_keys), 99999):
                    dist[(*nodes, new_keys)] = n_length
                    heappush(queue,  (n_length, new_keys, *nodes))
                    parent[(*nodes, new_keys)] = (n0, n1, n2, n3, keys)
    min_length = min(dist[d] for d in dist if d[4] == full_key_set)
    return dist, parent, min_length


def shortest_path(grid, keys, entrances):
    graph = create_graph(grid, keys, entrances)

    if len(entrances) == 1:
        dist, parent, min_length = graph_dijkstra(graph, '@0', ''.join(sorted(keys.values())))
    else:
        start = [f'@{i}' for i in range(len(entrances))]
        dist, parent, min_length = graph_qdijkstra(graph, start, ''.join(sorted(keys.values())))
    return dist, min_length


tester = ic.Tester('vault')

grid, keys, doors, entrances = read_map('test1')
dist, min_dist = shortest_path(grid, keys, entrances)
tester.test_value(min_dist, 8)

grid, keys, _, entrances = read_map('test2')
_, min_dist = shortest_path(grid, keys, entrances)
tester.test_value(min_dist, 86)

grid, keys, _, entrances = read_map('test3')
_, min_dist = shortest_path(grid, keys, entrances)
tester.test_value(min_dist, 132)

grid, keys, _, entrances = read_map('test4')
_, min_dist = shortest_path(grid, keys, entrances)
tester.test_value(min_dist, 136)

grid, keys, _, entrances = read_map('test5')
_, min_dist = shortest_path(grid, keys, entrances)
tester.test_value(min_dist, 81)

grid, keys, _, entrances = read_map('input')
_, min_dist = shortest_path(grid, keys, entrances)
tester.test_value(min_dist, 5402, 'Solution to part 1 = %s')

grid, keys, _, entrances = read_map('test6')
_, min_dist = shortest_path(grid, keys, entrances)
tester.test_value(min_dist, 8)

grid, keys, _, entrances = read_map('test7')
_, min_dist = shortest_path(grid, keys, entrances)
tester.test_value(min_dist, 24)

grid, keys, _, entrances = read_map('test8')
_, min_dist = shortest_path(grid, keys, entrances)
tester.test_value(min_dist, 32)

grid, keys, _, entrances = read_map('input2')
_, min_dist = shortest_path(grid, keys, entrances)
tester.test_value(min_dist, 2138, 'Solution to part 2 = %s')

tester.summary()
