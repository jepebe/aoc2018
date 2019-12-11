from collections import deque

from intcode import Tester


def print_map(topo, dist):
    minx = min(x[0] for x in topo)
    miny = min(x[1] for x in topo)
    maxx = max(x[0] for x in topo)
    maxy = max(x[1] for x in topo)

    for y in range(miny, maxy + 1):
        row = []
        for x in range(minx, maxx + 1):
            if x == 0 and y == 0:
                row.append('X')
            elif (x, y) in topo:
                #if topo[(x, y)] == '.':
                #    row.append(str(dist[(x, y)]))
                #else:
                    row.append(topo[(x, y)])
            else:
                row.append('#')
        print(''.join(row))


def bfs(topo, start):
    dist = {}
    queue = deque([[start]])
    seen = {start}
    while queue:
        path = queue.popleft()
        x, y = path[-1]
        dist[(x, y)] = len(path)

        for d in ((0, -1), (-1, 0), (1, 0), (0, 1)):
            pos = (x + d[0], y + d[1])

            if pos in topo and topo[pos] in ['*']:
                pos = (pos[0] + d[0], pos[1] + d[1])
            else:
                continue

            if pos not in topo:
                continue

            if pos in seen:
                continue

            queue.append(path + [pos])
            seen.add(pos)
    print(dist)
    return dist


if __name__ == '__main__':
    topo = {
        (0, 0): '*',
        (0, 1): '*',
        (0, 2): '*',
        (0, 3): '*',
        (1, 3): '*',
        (2, 3): '*',
        (2, 2): '*',
        (1, 2): '*',
        (1, 0): '*',
        (2, 0): '*',
        (3, 0): '*',
        (4, 0): '*',
        (4, 1): '*',
        (4, 2): '*',

    }



    tester = Tester('BFS')

    dist = bfs(topo, (0, 0))
    tester.test_value(dist[(1, 0)], 1)
    tester.test_value(dist[(4, 2)], 6)
    tester.test_value(dist[(2, 2)], 6)

    print_map(topo, dist)