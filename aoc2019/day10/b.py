
from math import atan2, pi, sqrt

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


def calculate_in_sight(grid, src):
    asteroids = {pos: 0 for pos, asteroid in grid.items() if asteroid == '#'}
    del asteroids[src]
    can_see = []

    for a in asteroids:
        dx = src[0] - a[0]
        dy = src[1] - a[1]
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
            can_see.append(a)

    return can_see


tester = Tester('vaporize')

grid = load_map('test4')
can_see = calculate_in_sight(grid, (6, 3))
tester.test_value(len(can_see), 41)

grid = load_map('test5')
can_see = calculate_in_sight(grid, (11, 13))
tester.test_value(len(can_see), 210)


def angle(v1, v2):
    angl = atan2(v2[1], v2[0]) - atan2(v1[1], v1[0])
    if angl < 0:
        angl += 2 * pi
    return angl


def cw_angler(v1):
    def func(v2):
        v2 = (v2[0] - v1[0], v2[1] - v1[1])
        l = sqrt(v2[0]*v2[0] + v2[1]*v2[1])
        v2 = (v2[0] / l, v2[1] / l)
        return angle((0, -1), v2)
    return func


def vaporizer(grid, v0):
    vaporized = []
    cwa = cw_angler(v0)
    while len(vaporized) < 200:
        can_see = calculate_in_sight(grid, v0)
        order = sorted(can_see, key=cwa)
        vaporized.extend(order)
        for a in order:
            del grid[a]

    return vaporized


tester.test_value(angle((0, -1), (1, 0)), pi / 2)
tester.test_value(angle((0, -1), (1, -1)), pi / 4)
tester.test_value(angle((0, -1), (0, -1)), 0)

vaporized = vaporizer(grid, (11, 13))
tester.test_value(vaporized[0], (11, 12))
tester.test_value(vaporized[1], (12, 1))
tester.test_value(vaporized[2], (12, 2))
tester.test_value(vaporized[9], (12, 8))
tester.test_value(vaporized[19], (16, 0))
tester.test_value(vaporized[49], (16, 9))
tester.test_value(vaporized[99], (10, 16))
tester.test_value(vaporized[198], (9, 6))
tester.test_value(vaporized[199], (8, 2))

grid = load_map('input')
can_see = calculate_in_sight(grid, (22, 25))
tester.test_value(len(can_see), 286)
vaporized = vaporizer(grid, (22, 25))
print(vaporized[199], vaporized[199][0] * 100 + vaporized[199][1])
tester.summary()