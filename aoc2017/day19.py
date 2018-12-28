import string

PATH = ['|', '-', '+']
LETTERS = list(string.ascii_uppercase)
VALID = PATH + LETTERS

DIR = {
    'up': (0, -1),
    'down': (0, 1),
    'left': (-1, 0),
    'right': (1, 0)
}

horizontal = (DIR['left'], DIR['right'])
vertical = (DIR['up'], DIR['down'])


def create_maze(lines):
    w = max([len(line) for line in lines])
    h = len(lines)
    m = [[' ' for x in range(w)] for y in range(h)]
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            m[y][x] = c
    return m


def find_starting_point(m):
    return m[0].index('|'), 0


def move(m, x, y, dx, dy, w, h):
    x = x + dx
    y = y + dy

    if 0 <= x < w and 0 <= y < h:
        if m[y][x] != ' ':
            return x, y
    #print('Move failed: %s, %s %s, %s' % (x, y, dx, dy))
    return None


def find_direction(m, x, y, dirs, w, h):
    for d in dirs:
        res = move(m, x, y, d[0], d[1], w, h)

        if res is not None:
            return d

    print('Direction not found!')


def mazerunner(m, x, y):
    d = DIR['down']
    w = len(m[0])
    h = len(m)
    found = []
    count = 0
    while True:
        c = m[y][x]
        m[y][x] = '#'

        if c in LETTERS:
            found.append(c)
        elif c == '+':
            if d in vertical:
                d = find_direction(m, x, y, horizontal, w, h)
            elif d in horizontal:
                d = find_direction(m, x, y, vertical, w, h)
        elif c == ' ':
            print('Mazerunner failed! Found empty space!')

        mv = move(m, x, y, d[0], d[1], w, h)
        count += 1
        if mv is None:
            print(x, y, d)
            break

        x, y = mv

    # print(found)
    # print('steps %d' % count)

    # for line in m:
    #     print(''.join(line))

    return ''.join(found), count


if __name__ == '__main__':
    with open('day19_test.txt', 'r') as f:
        lines = f.read().splitlines(keepends=False)

    m = create_maze(lines)

    assert m[0][5] == '|'
    assert m[2][5] == 'A'
    assert m[3][10] == 'E'
    assert m[1][8] == '+'

    x, y = find_starting_point(m)
    assert mazerunner(m, x, y) == ('ABCDEF', 38)

    with open('day19.txt', 'r') as f:
        lines = f.read().splitlines(keepends=False)

    m = create_maze(lines)
    x, y = find_starting_point(m)
    print(mazerunner(m, x, y))
