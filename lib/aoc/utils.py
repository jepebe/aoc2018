from heapq import heappop, heappush


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
