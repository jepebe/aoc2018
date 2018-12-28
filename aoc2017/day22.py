directions = {
    'up': (0, -1),
    'down': (0, 1),
    'left': (-1, 0),
    'right': (1, 0)
}


def mappify(lines):
    nodes = {}
    size = len(lines)
    for y, row in enumerate(lines):
        for x, node in enumerate(row):
            nodes[(x, y)] = node
    x, y = size // 2, size // 2
    nodes['infected'] = 0

    return nodes, (x, y), sum(1 for n in nodes.values() if n == '#')


def infected(nodes, x, y):
    if not (x, y) in nodes:
        nodes[(x, y)] = '.'
    return nodes[(x, y)] == '#' or nodes[(x, y)] == '@'


def infect(nodes, x, y):
    if infected(nodes, x, y):
        print('Already infected: (%d, %d)' % (x, y))
    nodes[(x, y)] = '@'
    nodes['infected'] += 1


def clean(nodes, x, y):
    #if not infected(nodes, x, y):
    #    print('Already cleaned (%d, %d)' % (x, y))
    nodes[(x, y)] = '.'


def turn_left(direction):
    if direction == 'up':
        return 'left'
    elif direction == 'left':
        return 'down'
    elif direction == 'down':
        return 'right'
    elif direction == 'right':
        return 'up'
    else:
        print('Unknown direction %s' % direction)


def turn_right(direction):
    if direction == 'up':
        return 'right'
    elif direction == 'right':
        return 'down'
    elif direction == 'down':
        return 'left'
    elif direction == 'left':
        return 'up'
    else:
        print('Unknown direction %s' % direction)

def reverse(direction):
    if direction == 'up':
        return 'down'
    elif direction == 'down':
        return 'up'
    elif direction == 'left':
        return 'right'
    elif direction == 'right':
        return 'left'
    else:
        print('Unknown direction %s' % direction)


def burst(nodes, x, y, direction):
    if infected(nodes, x, y):
        direction = turn_right(direction)
        clean(nodes, x, y)
    else:
        direction = turn_left(direction)
        infect(nodes, x, y)

    dx, dy = directions[direction]
    return nodes, (x + dx, y + dy), direction


def iterate(nodes, x, y, n, burst=burst):
    direction = 'up'
    for i in range(n):
        nodes, (x, y), direction = burst(nodes, x, y, direction)
    return nodes['infected']


def part1():
    nodes = '..#\n#..\n...'
    nodes, (x, y), infected_count = mappify(nodes.splitlines(keepends=False))
    assert infected_count == 2
    assert nodes[(2, 0)] == '#'
    assert nodes[(0, 1)] == '#'
    assert nodes[(1, 1)] == '.'
    assert (x, y) == (1, 1)

    assert infected(nodes, 2, 0)
    infect(nodes, 1, 1)
    assert infected(nodes, 1, 1)
    clean(nodes, 1, 1)
    assert not infected(nodes, 1, 1)

    nodes, (x, y), direction = burst(nodes, 1, 1, 'up')
    assert infected(nodes, 1, 1)
    assert (x, y) == (0, 1)
    assert direction == 'left'

    nodes = '..#\n#..\n...'
    nodes, (x, y), infected_count = mappify(nodes.splitlines(keepends=False))
    infected_count = iterate(nodes, x, y, n=7)
    assert infected_count == 5

    nodes = '..#\n#..\n...'
    nodes, (x, y), infected_count = mappify(nodes.splitlines(keepends=False))
    infected_count = iterate(nodes, x, y, n=10000)
    assert infected_count == 5587

    with open('day22.txt', 'r') as f:
        lines = f.read().splitlines(keepends=False)

    nodes, (x, y), infected_count = mappify(lines)
    assert (x, y) == (12, 12)
    assert infected_count == 289
    print(iterate(nodes, x, y, n=10000))


def is_clean(nodes, x, y):
    if not (x, y) in nodes:
        nodes[(x, y)] = '.'
    return nodes[(x, y)] == '.'


def weaken(nodes, x, y):
    nodes[(x, y)] = 'w'


def is_weak(nodes, x, y):
    return nodes[(x, y)] == 'w'


def flag(nodes, x, y):
    nodes[(x, y)] = 'f'


def is_flagged(nodes, x, y):
    return nodes[(x, y)] == 'f'


def burst_cmplx(nodes, x, y, direction):
    if is_clean(nodes, x, y):
        direction = turn_left(direction)
        weaken(nodes, x, y)
    elif is_weak(nodes, x, y):
        infect(nodes, x, y)
    elif infected(nodes, x, y):
        direction = turn_right(direction)
        flag(nodes, x, y)
    elif is_flagged(nodes, x, y):
        direction = reverse(direction)
        clean(nodes, x, y)

    dx, dy = directions[direction]
    return nodes, (x + dx, y + dy), direction


if __name__ == '__main__':
    #part1()

    nodes = '..#\n#..\n...'
    nodes, (x, y), infected_count = mappify(nodes.splitlines(keepends=False))
    infected_count = iterate(nodes, x, y, n=100, burst=burst_cmplx)
    assert infected_count == 26

    nodes = '..#\n#..\n...'
    nodes, (x, y), infected_count = mappify(nodes.splitlines(keepends=False))
    infected_count = iterate(nodes, x, y, n=10000000, burst=burst_cmplx)
    assert infected_count == 2511944

    with open('day22.txt', 'r') as f:
        lines = f.read().splitlines(keepends=False)

    nodes, (x, y), infected_count = mappify(lines)
    infected_count = iterate(nodes, x, y, n=10000000, burst=burst_cmplx)
    print(infected_count)

