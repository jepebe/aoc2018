import intcode as ic


def create_map(sm):
    grid = {}
    y = 0
    x = 0
    pos = None
    while ic.has_output(sm):
        v = ic.get_output(sm)
        if v != ord('\n'):
            if v in (ord('^'), ord('<'), ord('>'), ord('v')):
                pos = (x, y)
            grid[(x, y)] = v
            x += 1
        else:
            y += 1
            x = 0

    return grid, pos


def find_intersections(grid, missing='.'):
    intersection = '.#.###.#.'
    minx, maxx, miny, maxy = ic.find_extents(grid)
    intersections = []
    for j in range(miny, maxy):
        for i in range(minx, maxx):
            patch = []
            for y in range(3):
                for x in range(3):
                    if (i + x, j + y) in grid:
                        patch.append(chr(grid[(i + x, j + y)]))
                    else:
                        patch.append(missing)
            patch = ''.join(patch)
            if patch == intersection:
                intersections.append((i + 1, j + 1))
    return intersections


def find_path(grid, p):
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

        np = p
        while np in grid and grid[np] != ord('.'):
            i += 1
            np = ic.add_tuple(p, ic.scale_tuple(d, i))

        i -= 1
        p = ic.add_tuple(p, ic.scale_tuple(d, i))
        path.append(i)

        l = directions[d]['L']
        r = directions[d]['R']
        lp = ic.add_tuple(p, l)
        rp = ic.add_tuple(p, r)
        if lp in grid and grid[lp] == ord('#'):
            d = l
            path.append('L')
        elif rp in grid and grid[rp] == ord('#'):
            d = r
            path.append('R')
        else:
            break
    return path


def find_repeating_patterns(path, exclude=()):
    patt_dict = {}

    for n in range(4, len(path), 2):
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
                    'pattern': patt
                }
            else:
                f, t = patt_dict[patt]['range']
                if f >= i + n or t < i:
                    patt_dict[patt]['count'] += 1

    return {key: value for key, value in patt_dict.items() if patt_dict[key]['count'] >= 1}


def replace_repeating(path, repeating, label):
    result = ','.join(map(str, path)).replace(repeating, f'{label}, ')
    return list(result.split(','))


def find_function_set(path, labels, exclude,):
    repeating = find_repeating_patterns(path, exclude=exclude)
    for repeat in repeating:
        p = replace_repeating(path, repeat, labels[0])

        if len(labels) == 1:
            p = ','.join(map(str, p)).replace(', ', '')

            if all([c in ('A', 'B', 'C', ',') for c in p]) and len(p) <= 20:
                return p, {labels[0]: repeating[repeat]}
        else:
            p, funcs = find_function_set(p, labels[1:], exclude + [labels[0]])
            if p is not None:
                funcs[labels[0]] = repeating[repeat]
                return p, funcs

    return None, None


def create_map_and_find_alignment():
    sm = ic.load_state_machine('input')
    ic.run_state_machine(sm)
    grid, pos = create_map(sm)
    #ic.print_map(grid, func=lambda g, p: chr(g[p]))

    intersections = find_intersections(grid)
    alignment = sum(map(lambda p: p[0] * p[1], intersections))
    return grid, pos, alignment


tester = ic.Tester('ascii')

grid, robo_pos, alignment = create_map_and_find_alignment()
tester.test_value(alignment, 6520, 'Solution to part 1 = %s')


path = 'R,8,R,8,R,4,R,4,R,8,L,6,L,2,R,4,R,4,R,8,R,8,R,8,L,6,L,2'.split(',')

path = replace_repeating(path, 'R,4,R,4,R,8', 'B')
tester.test_value(','.join(path), 'R,8,R,8,B, ,L,6,L,2,B, ,R,8,R,8,L,6,L,2')

path = replace_repeating(path, 'R,8,R,8', 'A')
tester.test_value(','.join(path), 'A, ,B, ,L,6,L,2,B, ,A, ,L,6,L,2')

path = replace_repeating(path, 'L,6,L,2', 'C')
tester.test_value(','.join(path), 'A, ,B, ,C, ,B, ,A, ,C, ')

path = 'R,8,R,8,R,4,R,4,R,8,L,6,L,2,R,4,R,4,R,8,R,8,R,8,L,6,L,2'.split(',')
main, fns = find_function_set(path, ['A', 'B', 'C'], [])

tester.test_value(main, 'A,B,C,B,A,C')
tester.test_value(fns['A']['pattern'], 'R,8,R,8')
tester.test_value(fns['B']['pattern'], 'R,4,R,4')
tester.test_value(fns['C']['pattern'], 'R,8,L,6,L,2')


sm = ic.load_state_machine('input')
path = find_path(grid, robo_pos)
path, funcs = find_function_set(path, ['A', 'B', 'C'], [])

tester.test_value(path, 'B,A,B,A,C,A,B,C,A,C')
tester.test_value(funcs['A']['pattern'], 'L,6,L,4,L,12')
tester.test_value(funcs['B']['pattern'], 'L,12,L,8,R,10,R,10')
tester.test_value(funcs['C']['pattern'], 'R,10,L,8,L,4,R,10')

sm['instructions'][0] = 2
ic.run_state_machine(sm)

for c in path:
    ic.add_input(sm, ord(c))
ic.add_input(sm, ord('\n'))

for label in ('A', 'B', 'C'):
    for c in funcs[label]['pattern']:
        ic.add_input(sm, ord(c))
    ic.add_input(sm, ord('\n'))
ic.add_input(sm, ord('n'))
ic.add_input(sm, ord('\n'))
ic.run_state_machine(sm)
# ic.print_output(sm)
ic.flush_output(sm)

tester.test_value(ic.get_last_output(sm), 1071369, 'Solution to part 2 = %s')

tester.summary()

sm = ic.load_state_machine('input')
sm['instructions'][0] = 2
ic.terminal(sm)
