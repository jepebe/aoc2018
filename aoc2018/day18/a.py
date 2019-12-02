import sys

lines = sys.stdin.readlines()

directions = [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]


def parse_input(lines):
    grid = {}
    y = 0
    for line in lines:
        x = 0
        for c in line.strip():
            grid[(x, y)] = c
            x += 1
        y += 1

    return grid


def count(adjacent, acre_type):
    return sum(1 for c in adjacent if c == acre_type)


def print_grid(grid):
    max_x = max(grid, key=lambda x: x[0])[0]
    max_y = max(grid, key=lambda x: x[1])[1]
    for y in range(max_y + 1):
        row = []
        for x in range(max_x + 1):
            row.append(grid[(x, y)])
        print(''.join(row))


def flatten(grid):
    max_x = max(grid, key=lambda x: x[0])[0]
    max_y = max(grid, key=lambda x: x[1])[1]
    acres = []
    for y in range(max_y + 1):
        for x in range(max_x + 1):
            acres.append(grid[(x, y)])
    return ''.join(acres)


def magic(grid):
    result = {}

    for pos, acre in grid.items():
        x, y = pos

        adjacent = []
        for dx, dy in directions:
            p = (x + dx, y + dy)
            if p in grid:
                adjacent.append(grid[p])

        result[pos] = grid[pos]

        if acre == '.' and count(adjacent, '|') >= 3:
            result[pos] = '|'
        elif acre == '|' and count(adjacent, '#') >= 3:
            result[pos] = '#'
        elif acre == '#':
            if count(adjacent, '#') >= 1 and count(adjacent, '|') >= 1:
                result[pos] = '#'
            else:
                result[pos] = '.'

    return result


def calculate_10_mins(grid):
    for i in range(10):
        grid = magic(grid)
        print_grid(grid)
    lumber = count(grid.values(), '|')
    lumber_yards = count(grid.values(), '#')
    print('resource value %d * %d = %d' % (lumber, lumber_yards, lumber * lumber_yards))


def calculate_resource(indexes, first_match, pattern_size, target):
    match_index = ((target - first_match) % pattern_size) + first_match
    return indexes[match_index]


def find_repeat_pattern(grid):
    patterns = {}
    indexes = {}
    first_match = None
    for i in range(1001):
        grid = magic(grid)
        flat_grid = flatten(grid)
        lumber = count(grid.values(), '|')
        lumber_yards = count(grid.values(), '#')

        if flat_grid not in patterns:
            patterns[flat_grid] = i
            indexes[i] = {'index': i,
                          'lumber': lumber,
                          'lumber_yards': lumber_yards,
                          'resource_value': lumber * lumber_yards
                          }
        elif first_match is None:
            first_match = patterns[flat_grid]
            pattern_size = i - patterns[flat_grid]
            break

    return indexes, first_match, pattern_size


original_grid = parse_input(lines)
print_grid(original_grid)
calculate_10_mins(original_grid)
indexes, first_match, pattern_size = find_repeat_pattern(original_grid)

# found 816 -> 189336
# found 817 -> 184886

print('idx for 816 -> %s' % calculate_resource(indexes, first_match, pattern_size, 816))
print('idx for 817 -> %s' % calculate_resource(indexes, first_match, pattern_size, 817))
print('idx for 999 -> %s' % calculate_resource(indexes, first_match, pattern_size, 999))
print('idx for 10000 -> %s' % calculate_resource(indexes, first_match, pattern_size, 10000))
print('idx for 999999999 -> %s' % calculate_resource(indexes, first_match, pattern_size, 1000000000 - 1))

# 208384
# 210630
# 207900 <- !
