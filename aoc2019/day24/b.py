import intcode as ic


def load_grid(filename):
    grid = {}
    with open(filename) as f:
        for y in range(5):
            line = f.readline().strip()
            for x in range(5):
                if (x, y) != (2, 2):
                    grid[(x, y, 0)] = line[x]
    return grid


def recursive_adjacency(x, y, level):
    adjacencies = []
    for n in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        nx, ny = ic.add_tuple((x, y), n)

        if nx == -1 or nx == 5 or ny == -1 or ny == 5:
            adjacencies.append((2 + n[0], 2 + n[1], level - 1))
        elif (nx, ny) == (2, 2):
            for i in range(5):
                nx = 2 * (abs(n[0]) - n[0]) + i * abs(n[1])
                ny = 2 * (abs(n[1]) - n[1]) + i * abs(n[0])
                adjacencies.append((nx, ny, level + 1))
        else:
            adjacencies.append((nx, ny, level))
    return sorted(adjacencies)


def simulate_level(grid, level=0):
    new_grid = {}
    for y in range(5):
        for x in range(5):
            if (x, y) != (2, 2):
                grid[(x, y, -(level + 1))] = '.'
                grid[(x, y, level + 1)] = '.'

    for (x, y, lvl) in grid:
        neighbour_count = 0
        for n in recursive_adjacency(x, y, lvl):
            if n in grid and grid[n] == '#':
                neighbour_count += 1

        if grid[(x, y, lvl)] == '#' and neighbour_count != 1:
            new_grid[(x, y, lvl)] = '.'
        elif 1 <= neighbour_count <= 2:
            new_grid[(x, y, lvl)] = '#'
        else:
            new_grid[(x, y, lvl)] = '.'
    return new_grid


def simulate(grid, steps):
    for i in range(steps):
        grid = simulate_level(grid, level=i)
    return grid


def count_bugs(grid):
    return sum(1 for v in grid.values() if v == '#')


tester = ic.Tester('recursive bugs')
tester.test_value(recursive_adjacency(3, 3, 0), [(2, 3, 0), (3, 2, 0), (3, 4, 0), (4, 3, 0)])
tester.test_value(recursive_adjacency(1, 1, 1), [(0, 1, 1), (1, 0, 1), (1, 2, 1), (2, 1, 1)])
tester.test_value(recursive_adjacency(3, 0, 1), [(2, 0, 1), (2, 1, 0), (3, 1, 1), (4, 0, 1)])
tester.test_value(recursive_adjacency(4, 0, 1), [(2, 1, 0), (3, 0, 1), (3, 2, 0), (4, 1, 1)])
tester.test_value(recursive_adjacency(3, 2, 1), [(3, 1, 1), (3, 3, 1), (4, 0, 2), (4, 1, 2), (4, 2, 1), (4, 2, 2), (4, 3, 2), (4, 4, 2)])

grid = load_grid('test1')
grid = simulate(grid, 10)

tester.test_value(count_bugs(grid), 99)

grid = load_grid('input')
grid = simulate(grid, 200)

tester.test_value(count_bugs(grid), 1928, 'solution to part 2 is %s')

# for lvl in range(-10, 10):
#     print(f'depth {lvl}')
#     for y in range(5):
#         row = []
#         for x in range(5):
#             if (x, y) == (2, 2):
#                 row.append('?')
#             else:
#                 row.append(grid[(x, y, lvl)])
#         print(''.join(row))
