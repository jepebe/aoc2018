from collections import deque


def bfs(topo, start, walkable=('*',)):
    dist = {}
    queue = deque([[start]])
    seen = {start}
    while queue:
        path = queue.popleft()
        x, y = path[-1]
        dist[(x, y)] = len(path) - 1

        for d in ((0, -1), (-1, 0), (1, 0), (0, 1)):
            pos = (x + d[0], y + d[1])

            if pos in topo and topo[pos] in walkable:
                pass
            else:
                continue

            if pos not in topo:
                continue

            if pos in seen:
                continue

            queue.append(path + [pos])
            seen.add(pos)

    return dist


if __name__ == '__main__':
    from intcode import Tester, print_map
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
