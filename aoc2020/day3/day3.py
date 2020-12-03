import intcode as ic


def parse_grid(lines):
    grid = {}
    y = 0
    mx = 0
    for line in lines:
        x = 0
        for c in line.strip():
            grid[(x, y)] = c
            x += 1
        if x > mx:
            mx = x
        y += 1
    return grid, mx, y


def toboggan(grid, dx=3, dy=1, mx=11, my=11):
    x = 0
    y = 0
    trees = 0
    while y < my:
        x += dx
        y += dy
        if y < my and grid[(x % mx, y)] == '#':
            trees += 1

    return trees


def test_slopes(grid, mx, my):
    slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
    product = 1

    for slope in slopes:
        product *= toboggan(grid, slope[0], slope[1], mx, my)

    return product


tester = ic.Tester("Toboggan Trajectory")

lines = """..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#""".split()

grid, mx, my = parse_grid(lines)
tester.test_value(mx, 11)
tester.test_value(my, 11)
tester.test_value(toboggan(grid, dx=3, dy=1, mx=mx, my=my), 7)
tester.test_value(test_slopes(grid, mx=mx, my=my), 336)

with open('input') as f:
    lines = f.readlines()

grid, mx, my = parse_grid(lines)
trees = toboggan(grid, dx=3, dy=1, mx=mx, my=my)
tester.test_value(trees, 195, 'solution to exercise 1=%s')
tester.test_value(test_slopes(grid, mx, my), 3772314000, 'solution to exercise 2=%s')
