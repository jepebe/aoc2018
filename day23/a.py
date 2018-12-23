import sys
# pip install z3-solver
from z3 import Optimize, Int, If


def red(text):
    return f'\033[31m{text}\033[0m'


def green(text):
    return f'\033[92m{text}\033[0m'


def parse_input(lines):
    points = {}
    for line in lines:
        pos, r = line.split('>, r=')
        x, y, z = map(int, pos[5:].split(','))
        r = int(r)
        points[(x, y, z)] = r
    return points


def manhattan_distance(p, q):
    return abs(p[0] - q[0]) + abs(p[1] - q[1]) + abs(p[2] - q[2])


def brute_force(points):
    minx = min(x[0] for x in points)
    miny = min(x[1] for x in points)
    minz = min(x[2] for x in points)
    maxx = max(x[0] for x in points)
    maxy = max(x[1] for x in points)
    maxz = max(x[2] for x in points)

    best_point = (999999999, 999999999, 999999999)
    best_distance = 999999999
    best_count = 0
    for z in range(minz, maxz + 1):
        for y in range(miny, maxy + 1):
            for x in range(minx, maxx + 1):
                in_radius_count = 0
                for p in points:
                    if manhattan_distance((x, y, z), p) <= points[p]:
                        in_radius_count += 1

                if in_radius_count > best_count:
                    zd = manhattan_distance((x, y, z), (0, 0, 0))
                    best_point = (x, y, z)
                    best_count = in_radius_count
                    best_distance = zd
                elif in_radius_count == best_count:
                    zd = manhattan_distance((x, y, z), (0, 0, 0))
                    if zd < best_distance:
                        best_point = (x, y, z)
                        best_count = in_radius_count
                        best_distance = zd
    print(best_point, best_count, best_distance)


def find_nanobots_in_max_radius(points):
    max_radius_point = max(points, key=lambda x: points[x])
    max_radius = points[max_radius_point]

    print(f'Max radius is {max_radius} at {max_radius_point}')
    in_radius = 0
    for point in points:
        distance = manhattan_distance(max_radius_point, point)
        if distance <= max_radius:
            in_radius += 1

    print(f'Total number of points in radius {in_radius}')

    return in_radius


if __name__ == '__main__':
    points = parse_input(sys.stdin.readlines())

    count = find_nanobots_in_max_radius(points)

    if count in (6, 7, 442):
        print(green(f'Success! Radius count of {count} is correct'))
    else:
        print(red(f'Failed! Radius count of {count} is correct'))


    def z3abs(x):
        return If(x >= 0, x, -x)


    def dist(x1, y1, z1, x2, y2, z2):
        return z3abs(x1 - x2) + z3abs(y1 - y2) + z3abs(z1 - z2)


    x = Int('x')
    y = Int('y')
    z = Int('z')
    d = Int('d')
    opt = Optimize()

    for p in points:
        x2, y2, z2 = p
        opt.add_soft(dist(x, y, z, x2, y2, z2) <= points[p])
    opt.add(d == dist(x, y, z, 0, 0, 0))

    opt.minimize(d)  # apparently my input doesn't need this, but 'test' fails
    opt.check()
    m = opt.model()

    result = (m[x].as_long(), m[y].as_long(), m[z].as_long(), m[d].as_long())

    test_data = ((19992232, 58718915, 22274751, 100985898), (12, 12, 12, 36), (1, 0, 0, 1))
    if result in test_data:
        print(green(f'Success! Distance from (0, 0, 0) is {m[d]} from ({m[x], m[y], m[z]})'))
    else:
        print(red(f'Failed! Distance from (0, 0, 0) is not {m[d]} from ({m[x], m[y], m[z]})'))
