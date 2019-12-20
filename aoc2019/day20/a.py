from collections import deque

import intcode as ic


def read_map(filename):
    grid = {}
    portals = {}
    partials = {}

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
                            portals[(x - 2, y)] = partials[(x - 1, y)] + c
                        else:
                            portals[(x + 1, y)] = partials[(x - 1, y)] + c
                        del partials[(x - 1, y)]
                    elif (x, y - 1) in partials:
                        if (x, y - 2) in grid and grid[(x, y - 2)] == '.':
                            portals[(x, y - 2)] = partials[(x, y - 1)] + c
                        else:
                            portals[(x, y + 1)] = partials[(x, y - 1)] + c
                        del partials[(x, y - 1)]
                    else:
                        partials[(x, y)] = c

                x += 1
            y += 1

    minx, maxx, miny, maxy = ic.find_extents(grid)

    outer_portals = set()
    temp_portals = {}
    for portal in portals.keys():
        if abs(portal[0] - minx) == 2 or abs(portal[0] - maxx) == 2:
            outer_portals.add(portal)
        elif abs(portal[1] - miny) == 2 or abs(portal[1] - maxy) == 2:
            outer_portals.add(portal)
        name = portals[portal]
        if name not in temp_portals:
            temp_portals[name] = []
        temp_portals[name].append(portal)
        temp_portals[portal] = portals[portal]

    return grid, temp_portals, outer_portals


def traverse_maze(topo, portals, start='AA', end='ZZ'):
    start = portals[start][0]
    end = portals[end][0]
    queue = deque([[(start, 0)]])
    seen = {(start, 0)}
    while queue:
        path = queue.popleft()
        (x, y), portal_count = path[-1]

        if (x, y) == end:
            return len(path) - 1 + portal_count

        for d in ((0, -1), (-1, 0), (1, 0), (0, 1)):
            pos = (x + d[0], y + d[1])

            if pos not in topo:
                continue

            cell = topo[pos]
            if cell in ('#', ' '):
                continue

            pc = 0
            if pos in portals:
                portal = portals[pos]
                for p in portals[portal]:
                    if p == pos:
                        continue
                    else:
                        pos = p
                        pc += 1
                        break

            if pos in seen:
                continue

            queue.append(path + [(pos, portal_count + pc)])
            seen.add(pos)

    return None


def traverse_recursive_maze(topo, portals, outer, start='AA', end='ZZ'):
    start_pos = portals[start][0]
    end_pos = portals[end][0]
    queue = deque([[(start_pos, 0, 0)]])
    seen = {(start_pos, 0, 0)}
    while queue:
        path = queue.popleft()
        (x, y), portal_count, lvl = path[-1]

        if ((x, y), lvl) == (end_pos, 0):
            return len(path) - 1 + portal_count

        for d in ((0, -1), (-1, 0), (1, 0), (0, 1)):
            pos = (x + d[0], y + d[1])

            if pos not in topo:
                continue

            cell = topo[pos]
            if cell in ('#', ' '):
                continue

            pc = 0
            plvl = 0
            if pos in portals and portals[pos] not in (start, end):
                if pos in outer and lvl == 0:
                    pass
                else:
                    portal = portals[pos]
                    for p in portals[portal]:
                        if p != pos:
                            plvl = -1 if pos in outer else 1
                            pos = p
                            pc = 1
                            break

            if (pos, lvl + plvl) in seen:
                continue

            queue.append(path + [(pos, portal_count + pc, lvl + plvl)])
            seen.add((pos, lvl + plvl))

    return None


tester = ic.Tester('donut')

grid, portals, _ = read_map('test1')
tester.test_value(traverse_maze(grid, portals), 23)

grid, portals, _ = read_map('test2')
tester.test_value(traverse_maze(grid, portals), 58)

grid, portals, _ = read_map('test3')
tester.test_value(traverse_maze(grid, portals), 77)

grid, portals, _ = read_map('input')
tester.test_value(traverse_maze(grid, portals), 600, 'Solution to part 1 %s')


grid, portals, outer = read_map('test1')
tester.test_value(traverse_recursive_maze(grid, portals, outer), 26)

grid, portals, outer = read_map('test3')
tester.test_value(traverse_recursive_maze(grid, portals, outer), 396)

grid, portals, outer = read_map('input')
tester.test_value(traverse_recursive_maze(grid, portals, outer), 6666, 'Solution to part 2 %s')

tester.summary()