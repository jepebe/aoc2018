from collections import deque
from copy import copy

import intcode as ic


def read_map(filename):
    grid = {}
    partials = {}
    portal_pos = {}
    start = None
    end = None

    with open(filename) as f:
        y = 0
        for line in f.readlines():
            x = 0
            for c in line:
                if c == '\n':
                    continue
                pos = (x, y)
                grid[pos] = c

                if c.isalpha():
                    if (x - 1, y) in partials:
                        if (x - 2, y) in grid and grid[(x - 2, y)] == '.':
                            portal_pos[(x - 2, y)] = (partials[(x - 1, y)] + c)
                        else:
                            portal_pos[(x + 1, y)] = (partials[(x - 1, y)] + c)
                        del partials[(x - 1, y)]
                    elif (x, y - 1) in partials:
                        if (x, y - 2) in grid and grid[(x, y - 2)] == '.':
                            portal_pos[(x, y - 2)] = (partials[(x, y - 1)] + c)
                        else:
                            portal_pos[(x, y + 1)] = (partials[(x, y - 1)] + c)
                        del partials[(x, y - 1)]
                    else:
                        partials[(x, y)] = c

                x += 1
            y += 1

    minx, maxx, miny, maxy = ic.find_extents(grid)

    portals = {}
    for portal in portal_pos:
        if portal_pos[portal] == 'AA':
            start = portal
        elif portal_pos[portal] == 'ZZ':
            end = portal
        else:
            portals[portal] = {
                'name': portal_pos[portal],
                'destination': None,
                'outer': False,
                'inner': False,
                'pos': portal
            }

    for portal in portals:
        if abs(portal[0] - minx) == 2 or abs(portal[0] - maxx) == 2:
            portals[portal]['outer'] = True
        elif abs(portal[1] - miny) == 2 or abs(portal[1] - maxy) == 2:
            portals[portal]['outer'] = True
        else:
            portals[portal]['inner'] = True

    for portal in portals:
        if not portal.is_outer_portal():
            dst = outer[portal.value]
            dst.set_portal_destination(portal)
            portal.set_portal_destination(dst)

    return grid, start, end


class Node(object):
    def __init__(self, x, y, value, level=0):
        self._x = x
        self._y = y
        self._value = value
        self._level = level
        self._portal = False
        self._outer_portal = False
        self._portal_destination = None

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def pos(self):
        return self.x, self.y

    @property
    def value(self):
        return self._value

    def is_traversable(self):
        return self.value not in ('#', ' ')

    def set_is_portal(self, portal_name):
        self._portal = True
        self._value = portal_name

    def is_portal(self):
        return self._portal

    def set_is_outer_portal(self):
        self._outer_portal = True

    def is_outer_portal(self):
        return self._outer_portal

    def set_portal_destination(self, node):
        self._portal_destination = node

    def neighbours(self, grid, **kwargs):
        for d in ((0, -1), (-1, 0), (1, 0), (0, 1)):
            pos = ic.add_tuple(self.pos, d)

            if pos not in grid:
                continue

            if grid[pos].is_traversable():
                neighbour = grid[pos].copy()
                neighbour._level = self._level
                yield neighbour

        if self.is_portal():
            dst = self._portal_destination.copy()
            if 'mode' in kwargs and kwargs['mode'] == 'recursive':
                if self.is_outer_portal() and self._level == 0:
                    pass
                else:
                    level = self._level
                    level += -1 if self.is_outer_portal() else 1
                    dst._level = level
                    yield dst
            else:
                yield dst

    def copy(self):
        return copy(self)

    def __hash__(self):
        return hash((self.x, self.y, self._level))

    def __eq__(self, o):
        return (self.x, self.y, self._level) == (o.x, o.y, o._level)

    def __str__(self):
        return f'({self.x}, {self.y}) {self._level} {self.value} {self.is_outer_portal()}'

    def __repr__(self):
        return str(self)


def traverse_maze(topo, start, end, mode=None):
    queue = deque([[start]])
    seen = {start}
    while queue:
        path = queue.popleft()
        node = path[-1]

        if node == end:
            return len(path) - 1

        for neighbour in node.neighbours(topo, mode=mode):
            if neighbour in seen:
                continue

            queue.append(path + [neighbour])
            seen.add(neighbour)

    return None


tester = ic.Tester('donut')

grid, start, end = read_map('test1')
tester.test_value(traverse_maze(grid, start, end), 23)

grid, start, end = read_map('test2')
tester.test_value(traverse_maze(grid, start, end), 58)

grid, start, end = read_map('test3')
tester.test_value(traverse_maze(grid, start, end), 77)

grid, start, end = read_map('input')
tester.test_value(traverse_maze(grid, start, end), 600, 'Solution to part 1 = %s')


grid, start, end = read_map('test1')
tester.test_value(traverse_maze(grid, start, end, mode='recursive'), 26)

grid, start, end = read_map('test3')
tester.test_value(traverse_maze(grid, start, end, mode='recursive'), 396)

grid, start, end = read_map('input')
tester.test_value(traverse_maze(grid, start, end, mode='recursive'), 6666, 'Solution to part 2 = %s')

tester.summary()