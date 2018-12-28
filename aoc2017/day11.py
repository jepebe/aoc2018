DIR = {
    'n': (-1, -1),
    'ne': (0, -1),
    'nw': (-1, 0),
    's': (1, 1),
    'se': (1, 0),
    'sw': (0, 1),

}


def distance(p0, p1):
    dist = max(
        abs(p1[1] - p0[1]),
        abs(p1[0] - p0[0]),
        abs((p1[0] - p1[1]) * -1 - (p0[0] - p0[1]) * -1)
    )
    return dist


def length(path):
    steps = path.split(',')

    max_distance = 0
    x = 0
    y = 0
    for step in steps:
        dx, dy = DIR[step]
        x += dx
        y += dy

        max_distance = max((distance((0, 0), (x, y))), max_distance)

    return distance((0, 0), (x, y)), max_distance


if __name__ == '__main__':
    assert length('ne,ne,ne') == (3, 3)
    assert length('ne,ne,sw,sw') == (0, 2)
    assert length('ne,ne,s,s') == (2, 2)
    assert length('se,sw,se,sw,sw') == (3, 3)

    with open('day11.txt', 'r') as f:
        data = f.read()

    print(length(data))
