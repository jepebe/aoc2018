import sys

lines = sys.stdin.readlines()

if len(sys.argv) == 1:
    print('Missing argument: 32 or 10000')
    exit(1)
else:
    max_size = int(sys.argv[1])


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


def create_grid(min_x, min_y, max_x, max_y, coords, max_size):
    grid = {}
    for y in range(min_y - 1, max_y + 2):
        # row = ''
        for x in range(min_x - 1, max_x + 2):
            dist = 0
            for coord in coords:
                dist += manhattan_distance((x, y), coord)

            grid[(x, y)] = 1 if dist < max_size else 0
            # row += str(dist) if dist < max_size else '.'

        # print(row)
    return grid


def count_area(grid, label):
    area = 0
    for key, value in grid.items():
        if value == label:
            area += 1

    return area


coords = parse_coords(lines)
min_x, min_y, max_x, max_y = find_extents(coords)
grid = create_grid(min_x, min_y, max_x, max_y, coords, max_size)

print('Area:', count_area(grid, 1))

