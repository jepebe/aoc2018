import sys

lines = sys.stdin.readlines()


class Point(object):
    def __init__(self, p, v):
        self.p = p
        self.v = v

    def step(self):
        self.p = (self.p[0] + self.v[0], self.p[1] + self.v[1])

    def step_back(self):
        self.p = (self.p[0] - self.v[0], self.p[1] - self.v[1])


def min_max_of_cloud(points):
    min_x = min(points, key=lambda x: x.p[0]).p[0]
    max_x = max(points, key=lambda x: x.p[0]).p[0]

    min_y = min(points, key=lambda x: x.p[1]).p[1]
    max_y = max(points, key=lambda x: x.p[1]).p[1]
    return min_x, max_x, min_y, max_y


def area_of_cloud(points):
    min_x, max_x, min_y, max_y = min_max_of_cloud(points)

    area = (max_x - min_x) * (max_y - min_y)
    return area


def print_grid(points):
    min_x, max_x, min_y, max_y = min_max_of_cloud(points)
    w, h = max_x - min_x, max_y - min_y
    w += 1
    h += 1

    grid = [['.'] * w for _ in range(h)]

    for p in points:
        x = p.p[0] - min_x
        y = p.p[1] - min_y

        grid[y][x] = '#'

    for row in grid:
        print(''.join(row))


points = []
for line in lines:
    p, v = line.strip().split('> ')
    px, py = map(int, p[10:].split(', '))
    vx, vy = map(int, v[10:-1].split(', '))

    points.append(Point((px, py), (vx, vy)))

min_area = area_of_cloud(points)
seconds = -1
while True:
    area = area_of_cloud(points)

    if area <= min_area:
        min_area = area
        seconds += 1
    else:
        for p in points:
            p.step_back()
        break

    for p in points:
        p.step()

print(min_area, seconds, min_max_of_cloud(points))

print_grid(points)
