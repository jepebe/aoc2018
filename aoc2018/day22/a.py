# (a + b) mod n = [(a mod n) + (b mod n)] mod n.
# ab mod n = [(a mod n)(b mod n)] mod n.
from heapq import heappop, heappush


def red(text):
    return f'\033[31m{text}\033[0m'


def green(text):
    return f'\033[92m{text}\033[0m'


def yellow(text):
    return f'\033[33m{text}\033[0m'


def blue(text):
    return f'\033[34m{text}\033[0m'


def create_map(depth, target):
    w, h = target
    erosion_level = {}
    region_type = {}
    h += 1
    w += 1
    for y in range(h + 20):
        for x in range(w * 5):
            if (x, y) == target:
                gi = 0
            elif y == 0:
                gi = 16807 * x
            elif x == 0:
                gi = 48271 * y
            else:
                gi = erosion_level[(x - 1, y)] * erosion_level[(x, y - 1)]

            erosion_level[(x, y)] = (gi + depth) % 20183
            region_type[(x, y)] = erosion_level[(x, y)] % 3

    return region_type


def find_neighbours(regions, pos, equipped):
    x, y = pos

    for x, y in [(x - 1, y), (x, y - 1), (x + 1, y), (x, y + 1)]:
        if (x, y) in regions:
            r = regions[(x, y)]  # (0 = rocky, 1 = wet, 2 = narrow)
            for ne in (0, 1, 2):  # (neither, torch, climbing gear)
                # rocky in (torch, climbing gear)
                # wet in (neither, climbing gear)
                # narrow in (neither, torch)
                if r != ne and r != equipped:
                    distance = 8 if ne != equipped else 1
                    yield Node((x, y), ne, distance=distance)


class Node(object):
    def __init__(self, pos, equipped, distance=999999):
        self.pos = pos
        self.equipped = equipped
        self.distance = distance

    @property
    def x(self):
        return self.pos[0]

    @property
    def y(self):
        return self.pos[1]

    def __lt__(self, other):
        return self.distance < other.distance

    def __hash__(self):
        return hash((self.pos, self.equipped))

    def __eq__(self, other):
        if not isinstance(other, Node):
            return False
        return self.pos == other.pos and self.equipped == other.equipped


def dijkstra(regions, start, end):
    # add start position with distance 0 and torch (1)
    queue = [Node(start, 1, distance=0)]
    # store nodes as (x, y, equipped) : distance
    dist = {queue[0]: 0}
    parent = {}  # predecessors

    while queue:
        node = heappop(queue)

        if node.pos == end and node.equipped == 1:
            return node.distance, parent

        if dist.get(node, 99999) < node.distance:
            continue

        for neighbour in find_neighbours(regions, node.pos, node.equipped):
            nd = node.distance + neighbour.distance
            if nd < dist.get(neighbour, 99999):
                dist[neighbour] = nd
                neighbour.distance = nd
                heappush(queue, neighbour)
                parent[neighbour] = node

    return dist[Node(end, 0, 1)], parent


def print_map(regions, parents, start, target):
    parent = Node(target, 1)
    path = {parent.pos: parent}
    while parent != Node((0, 0), 1):
        parent = parents[parent]
        path[parent.pos] = parent

    types = {0: '.', 1: '=', 2: '|'}

    minx = min(x[0] for x in path)
    miny = min(x[1] for x in path)
    maxx = max(x[0] for x in path)
    maxy = max(x[1] for x in path)

    for y in range(miny, maxy + 2):
        row = []
        for x in range(minx, maxx + 2):
            if (x, y) == start:
                row.append(red('X'))
            elif (x, y) == target:
                row.append(red('T'))
            elif (x, y) in regions:
                if (x, y) in path:
                    e = path[(x, y)].equipped
                    if e == 0:
                        row.append(blue('x'))
                    elif e == 1:
                        row.append(yellow('x'))
                    else:
                        row.append(green('x'))
                else:
                    row.append(types[regions[(x, y)]])
            else:
                row.append('#')
        print(''.join(row))


if __name__ == '__main__':
    caves = [
        {'depth': 51, 'target': (5, 5), 'risk_level': 32, 'shortest_path': 10},
        {'depth': 510, 'target': (10, 10), 'risk_level': 114, 'shortest_path': 45},
        {'depth': 11820, 'target': (7, 15), 'risk_level': 129, 'shortest_path': 24},
        {'depth': 11820, 'target': (7, 20), 'risk_level': 169, 'shortest_path': 29},
        {'depth': 6939, 'target': (79, 30), 'risk_level': 2455, 'shortest_path': 132},
        {'depth': 11820, 'target': (7, 782), 'risk_level': 6318, 'shortest_path': 1075},
        {'depth': 6969, 'target': (9, 796), 'risk_level': 7901, 'shortest_path': 1087}
    ]

    for cave in caves:
        tx, ty = cave['target']
        rt = create_map(cave['depth'], (tx, ty))

        risk_level = sum(rt[(x, y)] for x, y in rt if 0 <= x <= tx and 0 <= y <= ty)

        shortest_path, parents = dijkstra(rt, (0, 0), (tx, ty))

        print_map(rt, parents, (0, 0), (tx, ty))

        if risk_level == cave['risk_level']:
            print(green(f'Success! Risk level {risk_level} == {cave["risk_level"]}'))
        else:
            print(red(f'Failed! Risk level {risk_level} != {cave["risk_level"]}'))

        if shortest_path == cave['shortest_path']:
            print(green(f'Success! Shortest path {shortest_path} == {cave["shortest_path"]}'))
        else:
            print(red(f'Failed! Shortest path {shortest_path} != {cave["shortest_path"]}'))
