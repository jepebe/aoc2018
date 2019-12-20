from collections import deque

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



    temp = {}
    portals = {}
    for portal in portal_pos:
        portal_name = portal_pos[portal]
        if portal_name == 'AA':
            start = portal
        elif portal_name == 'ZZ':
            end = portal
        else:
            portals[portal] = {
                'name': portal_name,
                'destination': None,
                'outer': False,
                'inner': False,
                'pos': portal
            }
            if portal_name in temp:
                portals[portal]['destination'] = temp[portal_name]
                portals[temp[portal_name]]['destination'] = portal
            else:
                temp[portal_name] = portal

    minx, maxx, miny, maxy = ic.find_extents(grid)
    for portal in portals:
        if abs(portal[0] - minx) == 2 or abs(portal[0] - maxx) == 2:
            portals[portal]['outer'] = True
        elif abs(portal[1] - miny) == 2 or abs(portal[1] - maxy) == 2:
            portals[portal]['outer'] = True
        else:
            portals[portal]['inner'] = True

    return grid, portals, start, end


def neighbours(grid, portals, pos):
    for d in ((0, -1), (-1, 0), (1, 0), (0, 1)):
        npos = ic.add_tuple(pos, d)

        if npos not in grid:
            continue

        if grid[npos] != '.':
            continue

        yield npos

    if pos in portals:
        yield portals[pos]['destination']


def recursive_neighbours(grid, portals, pos):
    level = pos[1]
    pos = pos[0]
    for d in ((0, -1), (-1, 0), (1, 0), (0, 1)):
        npos = ic.add_tuple(pos, d)

        if npos not in grid or grid[npos] != '.':
            continue

        yield npos, level

    if pos in portals:
        is_outer = portals[pos]['outer']
        if level == 0 and is_outer:
            pass
        else:
            dst = portals[pos]['destination']
            adj = -1 if is_outer else 1
            yield dst, level + adj


# def bfs(grid, start, end, neighbours):
#     queue = deque([[start]])
#     seen = {start}
#     dist = {}
#     while queue:
#         path = queue.popleft()
#         node = path[-1]
#         dist[node] = len(path) - 1
#
#         if end is not None and node == end:
#             return len(path) - 1
#
#         for neighbour in neighbours(grid, node):
#             if neighbour in seen:
#                 continue
#
#             queue.append(path + [neighbour])
#             seen.add(neighbour)
#
#     return dist


def traverse_maze(grid, portals, start, end):
    def neigh(grid, pos):
        return neighbours(grid, portals, pos)

    min_dist = ic.bfsf(grid, start, end, neigh)
    return min_dist


def traverse_recursive_maze(grid, portals, start, end):
    def neigh(grid, pos):
        return recursive_neighbours(grid, portals, pos)

    min_dist = ic.bfsf(grid, (start, 0), (end, 0), neigh)
    return min_dist


tester = ic.Tester('donut')


grid, portals, start, end = read_map('test1')
tester.test_value(traverse_maze(grid, portals, start, end), 23)

grid, portals, start, end = read_map('test2')
tester.test_value(traverse_maze(grid, portals, start, end), 58)

grid, portals, start, end = read_map('test3')
tester.test_value(traverse_maze(grid, portals, start, end), 77)

grid, portals, start, end = read_map('input')
tester.test_value(traverse_maze(grid, portals, start, end), 600, 'Solution to part 1 = %s')


grid, portals, start, end = read_map('test1')
tester.test_value(traverse_recursive_maze(grid, portals, start, end), 26)

grid, portals, start, end = read_map('test3')
tester.test_value(traverse_recursive_maze(grid, portals, start, end), 396)

grid, portals, start, end = read_map('input')
tester.test_value(traverse_recursive_maze(grid, portals, start, end), 6666, 'Solution to part 2 = %s')

tester.summary()