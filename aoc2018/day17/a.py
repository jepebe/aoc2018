import sys

sys.setrecursionlimit(100000)
lines = sys.stdin.readlines()


def parse_input(lines):
    clay = set()
    for line in lines:
        a, b = line.split(', ')

        a, val = a.split('=')

        val = int(val)

        b, rng = b.split('=')
        start, end = map(int, rng.split('..'))

        if a == 'x':
            for y in range(start, end + 1):
                clay.add((val, y))
        elif a == 'y':
            for x in range(start, end + 1):
                clay.add((x, val))
    min_x = min(clay, key=lambda x: x[0])[0]
    max_x = max(clay, key=lambda x: x[0])[0]
    min_y = min(clay, key=lambda x: x[1])[1]
    max_y = max(clay, key=lambda x: x[1])[1]
    return clay, (min_x, max_x, min_y, max_y)


def print_clay(clay, spring, rect, water):
    for y in range(0, rect[3] + 2):
        row = []
        for x in range(rect[0] - 1, rect[1] + 2):
            if (x, y) == spring:
                row.append('+')
            elif (x, y) in water:
                row.append(water[(x, y)])
            elif (x, y) in clay:
                row.append('#')
            else:
                row.append(' ')
        print(''.join(row))


def mark(clay, water, pos, direction):
    if pos not in clay and (pos in water and water[pos] in ('|', '~')):
        water[pos] = '~'
        x, y = pos
        mark(clay, water, (x + direction, y), direction)


def flow_left(clay, water, rect, pos):
    x, y = pos

    if pos not in clay and pos not in water:
        water[pos] = '|'

        flowing_down = waterfall(clay, water, rect, (x, y + 1))

        if not flowing_down:
            return flow_left(clay, water, rect, (x - 1, y))
        else:
            return True

    return False


def flow_right(clay, water, rect, pos):
    x, y = pos

    if pos not in clay and pos not in water:
        water[pos] = '|'

        flowing_down = waterfall(clay, water, rect, (x, y + 1))

        if not flowing_down:
            return flow_right(clay, water, rect, (x + 1, y))
        else:
            return True

    return False


def waterfall(clay, water, rect, pos):
    x, y = pos

    if y > rect[3]:
        return True

    if pos in water and water[pos] == '|':
        return True

    if pos not in clay and pos not in water:
        water[pos] = '|'

        flowing_down = waterfall(clay, water, rect, (x, y + 1))

        if not flowing_down:
            flowing_left = flow_left(clay, water, rect, (x - 1, y))
            flowing_right = flow_right(clay, water, rect, (x + 1, y))

            if not flowing_left and not flowing_right:
                mark(clay, water, pos, -1)
                mark(clay, water, pos, 1)
                return False
            else:
                return True
        else:
            return True

    return False


spring = (500, 0)
clay, rect = parse_input(lines)
water = {}

waterfall(clay, water, rect, spring)

print_clay(clay, spring, rect, water)

water_count = sum(1 for p in water if rect[2] <= p[1] <= rect[3])
water_retain = sum(1 for p in water if rect[2] <= p[1] <= rect[3] and water[p] == '~')


print('water particles: %s' % water_count)
print('water retained: %s' % water_retain)



# 31949 <-
# 26384 Retained