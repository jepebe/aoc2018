import intcode as ic


def load_grid(filename):
    grid = {}
    with open(filename) as f:
        for y in range(5):
            line = f.readline().strip()
            for x in range(5):
                grid[(x, y)] = line[x]
    return grid


def simulate(grid):
    new_grid = {}

    for (x, y) in grid:
        neighbour_count = 0
        for n in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            neighbour = ic.add_tuple((x, y), n)
            if neighbour in grid and grid[neighbour] == '#':
                neighbour_count += 1

        if grid[(x, y)] == '#' and neighbour_count != 1:
            new_grid[(x, y)] = '.'
        elif 1 <= neighbour_count <= 2:
            new_grid[(x, y)] = '#'
        else:
            new_grid[(x, y)] = '.'
    return new_grid


def flatten(grid):
    result = []
    for y in range(5):
        for x in range(5):
            result.append(grid[(x, y)])
    return ''.join(result)


def biodiversity_score(flat_grid):
    score = 0
    for i, c in enumerate(flat_grid):
        if c == '#':
            score += pow(2, i)
    return score


def run_simulation(grid):
    seen = {flatten(grid): 0}
    i = 0
    while True:
        grid = simulate(grid)
        flat_grid = flatten(grid)
        if flat_grid in seen:
            return biodiversity_score(flat_grid)
        seen[flat_grid] = i
        i += 1


tester = ic.Tester('bugs')

tester.test_value(biodiversity_score('...............#.....#...'), 2129920)

grid = load_grid('test1')
grid = simulate(grid)
tester.test_value(flatten(grid), '#..#.####.###.###.##.##..')
grid = simulate(grid)
tester.test_value(flatten(grid), '#####....#....#...#.#.###')
grid = simulate(grid)
tester.test_value(flatten(grid), '#....####....###.##..##.#')
grid = simulate(grid)
tester.test_value(flatten(grid), '####.....###..#.....##...')


grid = load_grid('test1')
tester.test_value(run_simulation(grid), 2129920)


grid = load_grid('input')
tester.test_value(run_simulation(grid), 1113073, 'solution for part 1 is %s')
# ic.print_map(grid, func=lambda g, p: str(g[p]))



