from collections import deque


def bfsf(grid, start, end, neighbours, cmp=lambda a: a, meta=None):
    queue = deque([[start]])
    seen = {start}
    dist = {}
    while queue:
        path = queue.popleft()
        node = path[-1]
        dist[cmp(node)] = len(path) - 1

        if end is not None and cmp(node) == end:
            length = len(path) - 1
            return meta(length, node) if meta else length

        for neighbour in neighbours(grid, node):
            if cmp(neighbour) in seen:
                continue

            queue.append(path + [neighbour])
            seen.add(cmp(neighbour))
    if end is not None:
        return None
    return dist


def bfs(topo, start, walkable=('*',)):
    def fn(grid, pos):
        for d in ((0, -1), (-1, 0), (1, 0), (0, 1)):
            npos = (pos[0] + d[0], pos[1] + d[1])

            if npos not in grid:
                continue

            if grid[npos] not in walkable:
                continue
            yield npos

    return bfsf(topo, start, None, neighbours=fn)


if __name__ == '__main__':
    from aoc import Tester, print_map
    topo = {
        (0, 0): '*',
        (0, 1): '*',
        (0, 2): '*',
        (0, 3): '*',
        (1, 3): '*',
        (2, 3): '*',
        (2, 2): '*',
        (1, 0): '*',
        (2, 0): '*',
        (3, 0): '*',
        (4, 0): '*',
        (4, 1): '*',
        (4, 2): '*',
        (5, 0): '*',
        (6, 0): '*',
        (6, 1): '*',
        (6, 2): '*',
        (5, 2): '*',
    }

    tester = Tester('BFS')

    dist = bfs(topo, (0, 0))
    tester.test_value(dist[(1, 0)], 1)
    tester.test_value(dist[(4, 2)], 6)
    tester.test_value(dist[(2, 2)], 6)
    tester.test_value(dist[(6, 2)], 8)
    tester.summary()

    def fn(g, p):
        return str(dist[p])

    print_map(topo, missing='#', func=fn)
