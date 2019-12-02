import sys
from collections import deque

lines = sys.stdin.readlines()

dirs = {
    'N': ((0, -1), '-'),
    'E': ((1, 0), '|'),
    'W': ((-1, 0), '|'),
    'S': ((0, 1), '-')
}


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


def parse_line(line):
    end = line.index('$')
    regex = line[1:end]
    test_target = None
    if line.index('=') > 0:
        test_target = int(line[end + 2:])
    return regex, test_target


def bfs(topo, start):
    dist = {}
    queue = deque([[start]])
    seen = {start}
    while queue:
        path = queue.popleft()
        x, y = path[-1]
        dist[(x, y)] = len(path) - 1

        for d in ((0, - 1), (- 1, 0), (1, 0), (0, 1)):
            pos = (x + d[0], y + d[1])

            if pos in topo and topo[pos] in ('|', '-'):
                pos = (pos[0] + d[0], pos[1] + d[1])
            else:
                continue

            if pos not in topo:
                continue
            #if topo[pos] == '#':
            #    continue
            if pos in seen:
                continue

            queue.append(path + [pos])
            seen.add(pos)
    return dist


def expand_map(topo, regex):
    stack = []
    index = 0
    x, y = 0, 0
    while index < len(regex):
        c = regex[index]

        if c in ('N', 'E', 'W', 'S'):
            (dx, dy), w = dirs[c]
            x, y = (x + dx, y + dy)
            topo[(x, y)] = w
            x, y = (x + dx, y + dy)
            topo[(x, y)] = '.'

        elif c == '(':
            stack.append((x, y))
        elif c == '|':
            x, y = stack[-1]
        elif c == ')':
            stack.pop()
        else:
            print('what?')

        index += 1


for line in lines[0:]:
    regex, test = parse_line(line)

    topo = {}
    topo[(0, 0)] = '.'

    expand_map(topo, regex)

    dist_map = bfs(topo, (0, 0))

    dist_count = sum(1 for d in dist_map if dist_map[d] >= 1000)
    print(f'Number of rooms with distance >= 1000 = {dist_count}')

    max_dist = max(dist_map.values())

    if test == max_dist:
        print(f'\033[92mSuccess! {test} == {max_dist}\033[0m')
    else:
        print(f'\033[31mFailed! {test} != {max_dist}\033[0m')


    #print_map(topo, dist_map)
