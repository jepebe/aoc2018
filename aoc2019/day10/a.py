import itertools

from intcode import Tester


def load_map(filename):
    grid = {}
    with open(filename) as f:
        lines = f.readlines()
        y = 0
        for line in lines:
            for x, value in enumerate(line.strip()):
                grid[(x, y)] = value
            y += 1

    return grid


def calculate_in_sight(grid):
    asteroids = {pos: 0 for pos, asteroid in grid.items() if asteroid == '#'}
    in_sight = {pos: 0 for pos in asteroids}
    for a, b in itertools.combinations(asteroids, 2):
        dx = b[0] - a[0]
        dy = b[1] - a[1]
        blocked = False

        if abs(dy) > abs(dx):
            steps = abs(dy)
            dx /= steps
            dy = -1 if dy < 0 else 1
        else:
            steps = abs(dx)
            dy /= steps
            dx = -1 if dx < 0 else 1

        for i in range(1, steps):
            p = a[0] + dx * i, a[1] + dy * i
            if float(p[0]).is_integer():
                p = int(p[0]), p[1]

            if float(p[1]).is_integer():
                p = p[0], int(p[1])

            if p in asteroids:
                blocked = True
                break

        if not blocked:
            in_sight[a] += 1
            in_sight[b] += 1

    return in_sight


tester = Tester('in_sight')

grid = load_map('test1')
in_sight = calculate_in_sight(grid)

tester.test_value(in_sight[(1, 0)], 7)
tester.test_value(in_sight[(4, 0)], 7)
tester.test_value(in_sight[(0, 2)], 6)
tester.test_value(in_sight[(1, 2)], 7)
tester.test_value(in_sight[(2, 2)], 7)
tester.test_value(in_sight[(3, 2)], 7)
tester.test_value(in_sight[(4, 2)], 5)
tester.test_value(in_sight[(4, 3)], 7)
tester.test_value(in_sight[(3, 4)], 8)
tester.test_value(in_sight[(4, 4)], 7)


grid = load_map('test2')
in_sight = calculate_in_sight(grid)
tester.test_value(in_sight[(5, 8)], 33)

grid = load_map('test3')
in_sight = calculate_in_sight(grid)
tester.test_value(in_sight[(1, 2)], 35)

grid = load_map('test4')
in_sight = calculate_in_sight(grid)
tester.test_value(in_sight[(6, 3)], 41)

grid = load_map('test5')
in_sight = calculate_in_sight(grid)
tester.test_value(in_sight[(11, 13)], 210)


grid = load_map('input')
in_sight = calculate_in_sight(grid)
max_key = max(in_sight, key=in_sight.get)
print(max_key, in_sight[max_key])
tester.test_value(in_sight[max_key], 286)

tester.summary()