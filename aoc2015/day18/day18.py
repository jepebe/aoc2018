import intcode as ic

tester = ic.Tester('Like a GIF For Your Yard')


def read_file(postfix=''):
    with open(f'input{postfix}') as f:
        lines = f.readlines()
    return lines


def create_grid(lines):
    grid = {}
    y = 0
    for line in lines:
        x = 0
        for c in line.strip():
            if c != '.':
                grid[(x, y)] = c
            x += 1
        y += 1
    return grid


def count_adjacent(x, y, grid):
    directions = ((-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1))
    count = 0
    for dx, dy in directions:
        pos = x + dx, y + dy
        if pos in grid and grid[pos] == '#':
            count += 1
    return count


def iterate(grid, extents, lock_corners=False):
    new_grid = {}
    min_x, max_x, min_y, max_y = extents

    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            neighbor_count = count_adjacent(x, y, grid)
            if (x, y) in grid and grid[(x, y)] == '#' and 2 <= neighbor_count <= 3:
                new_grid[(x, y)] = '#'
            elif (x, y) not in grid and neighbor_count == 3:
                new_grid[(x, y)] = '#'

    if lock_corners:
        new_grid[0, 0] = '#'
        new_grid[max_x, 0] = '#'
        new_grid[0, max_y] = '#'
        new_grid[max_x, max_y] = '#'

    return new_grid


def run_iterations(grid, count=4, lock_corners=False):
    min_x, max_x, min_y, max_y = ic.find_extents(grid)
    if lock_corners:
        grid[0, 0] = '#'
        grid[max_x, 0] = '#'
        grid[0, max_y] = '#'
        grid[max_x, max_y] = '#'

    extents = min_x, max_x, min_y, max_y
    # print(extents)
    # ic.print_map(grid, {'#': '#'}, missing='.')
    for i in range(count):
        grid = iterate(grid, extents, lock_corners)
        # print(i + 1)
        # ic.print_map(grid, {'#': '#'}, missing='.')
    return len(grid)


lines = """.#.#.#
...##.
#....#
..#...
#.#..#
####..""".split('\n')

grid = create_grid(lines)
tester.test_value(run_iterations(grid), 4)

grid = create_grid(read_file())
tester.test_value(run_iterations(grid, 100), 768, 'solution to exercise 1=%s')

grid = create_grid(lines)
tester.test_value(run_iterations(grid, count=5, lock_corners=True), 17)

grid = create_grid(read_file())
tester.test_value(run_iterations(grid, 100, True), 781, 'solution to exercise 2=%s')
