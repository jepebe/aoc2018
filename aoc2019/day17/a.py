import intcode as ic


def create_map(sm):
    look_up = {35: '#', 46: '.', 94: '^', 60: '<', 62: '>', 118: 'v', 88: 'X', 32: ' '}
    grid = {}
    y = 0
    x = 0
    pos = None
    while ic.has_output(sm):
        v = ic.get_output(sm)
        if v != 10:
            # if v not in look_up:
            #     print(v)
            if v == 94:
                pos = (x, y)
            grid[(x, y)] = v
            x += 1
        else:
            y += 1
            x = 0

    return grid, look_up, pos


def find_intersections(grid, look_up, missing='.'):
    intersection = '.#.###.#.'
    minx = min(x[0] for x in grid)
    miny = min(x[1] for x in grid)
    maxx = max(x[0] for x in grid)
    maxy = max(x[1] for x in grid)
    intersections = []
    for j in range(miny, maxy):
        for i in range(minx, maxx):
            patch = []
            for y in range(3):
                for x in range(3):
                    if (i + x, j + y) in grid:
                        patch.append(look_up[grid[(i + x, j + y)]])
                    else:
                        patch.append(missing)
            patch = ''.join(patch)
            if patch == intersection:
                intersections.append((i + 1, j + 1))
    return intersections


def find_path(grid, p):
    char = 65
    directions = {
        (-1, 0): {'L': (0, 1), 'R': (0, -1)},
        (1, 0): {'L': (0, -1), 'R': (0, 1)},
        (0, 1): {'L': (1, 0), 'R': (-1, 0)},
        (0, -1): {'L': (-1, 0), 'R': (1, 0)},
    }
    path = ['L']
    d = (-1, 0)
    while True:
        i = 0

        np = (p[0] + d[0] * i, p[1] + d[1] * i)
        while np in grid and grid[np] != ord('.'):
            grid[np] = char
            i += 1
            np = (p[0] + d[0] * i, p[1] + d[1] * i)

        i -= 1
        p = (p[0] + d[0] * i, p[1] + d[1] * i)
        path.append(i)

        l = directions[d]['L']
        r = directions[d]['R']
        lp = (p[0] + l[0], p[1] + l[1])
        rp = (p[0] + r[0], p[1] + r[1])
        if lp in grid and grid[lp] == ord('#'):
            d = l
            path.append('L')
        elif rp in grid and grid[rp] == ord('#'):
            d = r
            path.append('R')
        else:
            break
        char += 1
    return path


def find_repeating_patterns(path, exclude=()):
    patt_dict = {}

    for n in range(2, len(path), 2):
        for i in range(0, len(path) - n, 2):
            patt = (','.join(map(str, path[i:i + n])))
            if any(excl in patt for excl in exclude):
                continue

            if len(patt) > 20:
                continue

            if patt not in patt_dict:
                patt_dict[patt] = {
                    'sub': path[i:i + n],
                    'count': 1,
                    'range': (i, i + n),
                    'length': (i + n) - i,
                    'c': [i]
                }
            else:
                f, t = patt_dict[patt]['range']
                if f >= i + n or t < i:
                    patt_dict[patt]['count'] += 1
                    patt_dict[patt]['c'].append(i)

    return {key: value for key, value in patt_dict.items() if patt_dict[key]['count'] >= 1}


def replace_repeating(path, repeating, label):
    sub = ','.join(map(str, repeating['sub']))
    result = ','.join(map(str, path)).replace(sub, f'{label}, ')
    return list(result.split(','))


def find_function_set(path, labels, exclude,):
    repeating = find_repeating_patterns(path, exclude=exclude)
    for repeat in repeating:
        p = list(path)
        p = replace_repeating(p, repeating[repeat], labels[0])

        if len(labels) == 1:
            sp = ''.join(map(str, p)).replace(' ', '')

            if all([c in ('A', 'B', 'C') for c in sp]) and len(sp) <= 20:
                return sp, {labels[0]: repeating[repeat]}
        else:
            p, funcs = find_function_set(p, labels[1:], exclude + [labels[0]])
            if p is not None:
                funcs[labels[0]] = repeating[repeat]
                return p, funcs

    return None, None


sm = ic.load_state_machine('input')
ic.run_state_machine(sm)
grid, look_up, pos = create_map(sm)
ic.print_map(grid, func=lambda g, p: chr(g[p]))

intersections = find_intersections(grid, look_up)
alignment = sum(map(lambda p: p[0] * p[1], intersections))
print(alignment)

sm = ic.load_state_machine('input')
path = find_path(grid, pos)
ic.print_map(grid, func=lambda g, p: chr(g[p]))

path, funcs = find_function_set(path, ['A', 'B', 'C'], [])

sm['instructions'][0] = 2
ic.run_state_machine(sm)

print('main function', ','.join(map(str, path)))
for c in ','.join(map(str, path)):
    ic.add_input(sm, ord(c))
ic.add_input(sm, ord('\n'))

for label in ('A', 'B', 'C'):
    print(f'Function {label}', ','.join(map(str, funcs[label]['sub'])))
    for c in ','.join(map(str, funcs[label]['sub'])):
        ic.add_input(sm, ord(c))
    ic.add_input(sm, ord('\n'))
ic.add_input(sm, ord('n'))
ic.add_input(sm, ord('\n'))
ic.run_state_machine(sm)

grid, look_up, pos = create_map(sm)
ic.print_map(grid, func=lambda g, p: str(g[p]) if g[p] > 255 else chr(g[p]))
