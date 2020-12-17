import intcode as ic

tester = ic.Tester('Conway Cubes')


def read_file(postfix=''):
    with open(f'input{postfix}') as f:
        lines = f.readlines()
    return [line.strip() for line in lines]


def find_extents_4d(grid):
    minx = min(x[0] for x in grid)
    miny = min(x[1] for x in grid)
    minz = min(x[2] for x in grid)
    minw = min(x[3] for x in grid)
    maxx = max(x[0] for x in grid)
    maxy = max(x[1] for x in grid)
    maxz = max(x[2] for x in grid)
    maxw = max(x[3] for x in grid)
    return minx, maxx, miny, maxy, minz, maxz, minw, maxw


def print_map_4d(grid, look_up=None, missing=None, func=None):
    minx, maxx, miny, maxy, minz, maxz, minw, maxw = find_extents_4d(grid)

    for w in range(minw, maxw + 1):
        for z in range(minz, maxz + 1):
            print(f'z={z}, w={w}')
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


def create_grid_4d(lines):
    grid = {}
    w = 0
    z = 0
    y = 0
    for line in lines:
        x = 0
        for c in line:
            if c != '.':
                grid[(x, y, z, w)] = c
            x += 1
        y += 1
    return grid


def count_neighbours(grid, x, y, z, w):
    directions = ((-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1))
    count = 0

    for dw in (-1, 0, 1):
        pw = (x, y, z, w + dw)
        if dw != 0 and pw in grid and grid[pw] == '#':
            count += 1
        for dz in (-1, 0, 1):
            pz = (x, y, z + dz, w + dw)
            if dz != 0 and pz in grid and grid[pz] == '#':
                count += 1

            for dx, dy in directions:
                pos = x + dx, y + dy, z + dz, w + dw

                if pos in grid and grid[pos] == '#':
                    count += 1
    return count


def iterate(grid):
    new_grid = {}
    extents = find_extents_4d(grid)
    changes = 0
    for w in range(extents[6] - 1, extents[7] + 2):
        for z in range(extents[4] - 1, extents[5] + 2):
            for y in range(extents[2] - 1, extents[3] + 2):
                for x in range(extents[0] - 1, extents[1] + 2):
                    neighbor_count = count_neighbours(grid, x, y, z, w)
                    # print(x, y, z, neighbor_count)
                    if (x, y, z, w) in grid and neighbor_count in (2, 3):
                        new_grid[(x, y, z, w)] = '#'
                    elif (x, y, z) not in grid and neighbor_count == 3:
                        new_grid[(x, y, z, w)] = '#'
    return new_grid


def run(grid, n=6):
    for i in range(n):
        # print_map_3d(grid, {'#': '#'}, missing='.')
        grid = iterate(grid)
    return sum(1 for _ in grid.values())


lines = """.#.
..#
###""".splitlines()

grid = create_grid_4d(lines)
tester.test_value(run(grid), 848)

grid = create_grid_4d(read_file())
tester.test_value(run(grid), 2440, 'solution to part 2=%s')
