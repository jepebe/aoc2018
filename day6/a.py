import sys

lines = sys.stdin.readlines()


def parse_coords(lines):
    coords = []
    for line in lines:
        x, y = map(int, line.split(', '))
        coords.append((x, y))
    return coords


def find_extents(coords):
    min_x, min_y = coords[0]
    max_x, max_y = coords[0]

    for x, y in coords:
        if x < min_x:
            min_x = x
        elif x > max_x:
            max_x = x

        if y < min_y:
            min_y = y
        elif y > max_y:
            max_y = y
    # print(min_x, min_y, max_x, max_y)
    return min_x, min_y, max_x, max_y


def manhattan_distance(p, q):
    return abs(p[0] - q[0]) + abs(p[1] - q[1])


def create_grid(min_x, min_y, max_x, max_y, coords):
    grid = {}
    for y in range(min_y - 1, max_y + 2):
        # row = ''
        for x in range(min_x - 1, max_x + 2):
            dist = {}
            for index, coord in enumerate(coords):
                l = manhattan_distance((x, y), coord)
                if l not in dist:
                    dist[l] = []
                dist[l].append(index)

            value = dist[sorted(dist.keys())[0]]
            if len(value) == 1:
                grid[(x, y)] = value[0]
                #     row += str(value[0])
            else:
                grid[(x, y)] = -1
                #     row += '.'

        # print(row)
    return grid


def disqualify_infinite(min_x, min_y, max_x, max_y, grid):
    disqualified = set()
    for x in range(min_x - 1, max_x + 2):
        disqualified.add(grid[(x, min_y - 1)])
        disqualified.add(grid[(x, max_y + 1)])

    for y in range(min_y - 1, max_y + 2):
        disqualified.add(grid[(min_x - 1, y)])
        disqualified.add(grid[(max_x + 1, y)])
    # print(disqualified)
    return disqualified


def count_area(grid, disqualified):
    areas = {}
    for key, value in grid.items():
        if value not in disqualified:
            if value not in areas:
                areas[value] = 0
            areas[value] += 1

    return areas


coords = parse_coords(lines)
min_x, min_y, max_x, max_y = find_extents(coords)
grid = create_grid(min_x, min_y, max_x, max_y, coords)
disqualified = disqualify_infinite(min_x, min_y, max_x, max_y, grid)

areas = count_area(grid, disqualified)

print('Max area:', max(areas.values()))
