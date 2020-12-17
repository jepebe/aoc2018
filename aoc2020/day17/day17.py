import intcode as ic

tester = ic.Tester('Conway Cubes')


def read_file(postfix=''):
    with open(f'input{postfix}') as f:
        lines = f.readlines()
    return [line.strip() for line in lines]


def find_extents_3d(grid):
    minx = min(x[0] for x in grid)
    miny = min(x[1] for x in grid)
    minz = min(x[2] for x in grid)
    maxx = max(x[0] for x in grid)
    maxy = max(x[1] for x in grid)
    maxz = max(x[2] for x in grid)
    return minx, maxx, miny, maxy, minz, maxz


def print_map_3d(grid, look_up=None, missing=None, func=None):
    minx, maxx, miny, maxy, minz, maxz = find_extents_3d(grid)

    for z in range(minz, maxz + 1):
        print(f'z={z}')
        for y in range(miny, maxy + 1):
            row = []
            for x in range(minx, maxx + 1):
                if (x, y, z) not in grid:
                    if missing:
                        row.append(missing)
                    else:
                        row.append(' ')
                else:
                    if look_up:
                        row.append(look_up[grid[(x, y, z)]])
                    elif func:
                        row.append(func(grid, (x, y, z)))
                    else:
                        row.append('∞')

            print(''.join(row))


def create_grid(lines):
    grid = {}
    z = 0
    y = 0
    for line in lines:
        x = 0
        for c in line:
            if c != '.':
                grid[(x, y, z)] = c
            x += 1
        y += 1
    return grid

def create_grid_4d(lines):
    grid = {}
    w = 0
    z = 0
    y = 0
    for line in lines:
        x = 0
        for c in line:
            if c != '.':
                grid[(x, y, z)] = c
            x += 1
        y += 1
    return grid


def count_neighbours(grid, x, y, z):
    directions = ((-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1))
    count = 0
    for dz in (-1, 0, 1):
        if dz != 0 and (x, y, z + dz) in grid and grid[(x, y, z + dz)] == '#':
            count += 1

        for dx, dy in directions:
            pos = x + dx, y + dy, z + dz

            if pos in grid and grid[pos] == '#':
                count += 1
    return count


def iterate(grid):
    new_grid = {}
    extents = find_extents_3d(grid)
    changes = 0
    for z in range(extents[4] - 1, extents[5] + 2):
        for y in range(extents[2] - 1, extents[3] + 2):
            for x in range(extents[0] - 1, extents[1] + 2):
                neighbor_count = count_neighbours(grid, x, y, z)
                # print(x, y, z, neighbor_count)
                if (x, y, z) in grid and neighbor_count in (2, 3):
                    new_grid[(x, y, z)] = '#'
                elif (x, y, z) not in grid and neighbor_count == 3:
                    new_grid[(x, y, z)] = '#'
    return new_grid


def run(grid, n=6):
    for i in range(n):
        # print_map_3d(grid, {'#': '#'}, missing='.')
        grid = iterate(grid)
    return sum(1 for _ in grid.values())


lines = """.#.
..#
###""".splitlines()

grid = create_grid(lines)
tester.test_value(run(grid), 112)

grid = create_grid(read_file())
tester.test_value(run(grid), 338, 'solution to part 1=%s')
