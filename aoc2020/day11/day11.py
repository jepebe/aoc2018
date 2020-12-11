import intcode as ic

tester = ic.Tester('Seating System')


def read_file(postfix=''):
    with open(f'input{postfix}') as f:
        lines = f.readlines()
    return lines


def create_grid(lines):
    grid = {}
    y = 0
    for line in lines:
        x = 0
        for c in line:
            if c != '.':
                grid[(x, y)] = c
            x += 1
        y += 1
    return grid


def count_adjacent(x, y, grid, max_x, max_y, extend=False):
    directions = ((-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1))
    count = 0
    for dx, dy in directions:
        pos = x + dx, y + dy
        if extend:
            while 0 <= pos[0] <= max_x and 0 <= pos[1] <= max_y and pos not in grid:
                pos = pos[0] + dx, pos[1] + dy
        if pos in grid and grid[pos] == '#':
            count += 1
    return count


def iterate(grid, max_neighbour=4, extend=False):
    new_grid = {}
    min_x, max_x, min_y, max_y = ic.find_extents(grid)
    changes = 0
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            if (x, y) in grid:
                neighbor_count = count_adjacent(x, y, grid, max_x, max_y, extend)
                if grid[(x, y)] == 'L' and neighbor_count == 0:
                    new_grid[(x, y)] = '#'
                    changes += 1
                elif grid[(x, y)] == '#' and neighbor_count >= max_neighbour:
                    new_grid[(x, y)] = 'L'
                    changes += 1
                else:
                    new_grid[(x, y)] = grid[(x, y)]

    return new_grid, changes


def stabilize(grid, extend=False):
    grid, changes = iterate(grid, 5 if extend else 4, extend)
    iterations = 1
    while changes > 0:
        grid, changes = iterate(grid, 5 if extend else 4, extend)
        # ic.print_map(grid, {'#': '#', 'L': 'L', '.': '.'})
        iterations += 1
    return iterations - 1, sum(1 for s in grid.values() if s == '#')


seats = """L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL""".split('\n')

grid = create_grid(seats)
tester.test_value(stabilize(grid), (5, 37))

grid = create_grid(read_file())
iterations, occupied = stabilize(grid)
tester.test_value(iterations, 77)
tester.test_value(occupied, 2263, 'solution to exercise 1=%s')

grid = create_grid(seats)
tester.test_value(stabilize(grid, extend=True), (6, 26))

grid = create_grid(read_file())
iterations, occupied = stabilize(grid, extend=True)
tester.test_value(iterations, 82)
tester.test_value(occupied, 2002, 'solution to exercise 2=%s')
