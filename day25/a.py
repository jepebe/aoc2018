import sys


def red(text):
    return f'\033[31m{text}\033[0m'


def green(text):
    return f'\033[92m{text}\033[0m'


def parse_input(lines):
    points = []
    test_value = 0
    for line in lines:
        if line.startswith('#'):
            test_value = int(line[1:])
        else:
            x, y, z, t = map(int, line.split(','))
            points.append((x, y, z, t))
    return points, test_value


def manhattan_distance(p, q):
    return abs(p[0] - q[0]) + abs(p[1] - q[1]) + abs(p[2] - q[2]) + abs(p[3] - q[3])


def find_constellations(points):
    neighbours = {}
    for p1 in points:
        neighbours[p1] = []

        for p2 in points:
            if p2 != p1:
                if manhattan_distance(p1, p2) <= 3:
                    neighbours[p1].append(p2)

    consts = {}
    queue = []
    visited = []
    const = -1
    for point in points:
        if point not in visited:
            queue.append(point)
            const += 1
            consts[const] = []

        while queue:
            p = queue.pop()
            consts[const].append(p)
            visited.append(p)
            for n in neighbours[p]:
                if n not in visited and n not in queue:
                    queue.append(n)

    return consts


if __name__ == '__main__':
    lines = sys.stdin.readlines()
    points, test_value = parse_input(lines)

    consts = find_constellations(points)
    constellation_count = len(consts)
    if test_value == len(consts):
        print(green(f'Success! Constellations is {constellation_count} == {test_value}'))
    else:
        print(red(f'Failed! Constellations is not {constellation_count} == {test_value}'))
