import sys
from heapq import heappop, heappush
from itertools import product
from math import log, ceil
from operator import sub


def manhattan_distance(p, q):
    return abs(p[0] - q[0]) + abs(p[1] - q[1]) + abs(p[2] - q[2])


def parse_input(lines):
    points = []
    for line in lines:
        pos, r = line.split('>, r=')
        x, y, z = map(int, pos[5:].split(','))
        r = int(r)
        points.append((x, y, z, r))
    return points


def find_size(points):
    _min = tuple(map(min, zip(*points)))
    _max = tuple(map(max, zip(*points)))

    max_size = max(map(sub, _max[:3], _min[:3]))
    max_size = 2 ** (ceil(log(max_size, 2)))

    return _min[:3], max_size


def find(points, minimum, size):
    cubes = [Cube(minimum, size, points)]
    iterations = 0
    while cubes:
        cube = heappop(cubes)

        if cube.size == 0:
            print(f'Number of iterations before finding solution: {iterations}')
            return cube.p, cube.distance

        half_size = cube.size // 2

        x, y, z = cube.p
        for dx, dy, dz in product([0, half_size], repeat=3):
            heappush(cubes, Cube((x + dx, y + dy, z + dz), half_size, points))

        iterations += 1

    return (0, 0, 0), -1


class Cube(object):
    def __init__(self, p, size, points):
        self.p = p
        self.size = size
        self.distance = manhattan_distance(p, (0, 0, 0))
        self.in_radius = len([x for x in points if self.intersect(x)])

    def intersect(self, p):
        def f(a, b, sz):
            return 0 if a <= b <= a + sz else min(abs(b - a), abs(b - (a + sz)))

        s = sum(f(a, b, self.size) for a, b in zip(self.p, p))
        return s <= p[3]

    def __lt__(self, other):
        if self.in_radius == other.in_radius:
            return self.distance < other.distance
        return self.in_radius > other.in_radius

    def __repr__(self):
        return f'{self.p} {self.size} {self.in_radius}'


if __name__ == '__main__':
    points = parse_input(sys.stdin.readlines())

    minimum, size = find_size(points)

    (x, y, z), d = find(points, minimum, size)

    print(f'{x, y, z} -> {d}')
