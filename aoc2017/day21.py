def flip(pattern):
    rows = pattern.split('/')

    result = []
    for row in rows:
        result.append(''.join(reversed(row)))
    return '/'.join(result)


def transpose(ptrn):
    if len(ptrn) == 5:
        return ptrn[0] + ptrn[3] + '/' + ptrn[1] + ptrn[4]
    elif len(ptrn) == 11:
        return ptrn[0] + ptrn[4] + ptrn[8] + '/' + \
               ptrn[1] + ptrn[5] + ptrn[9] + '/' + \
               ptrn[2] + ptrn[6] + ptrn[10]
    else:
        print('Transpose What?')


def rotate90(ptrn):
    return flip(transpose(ptrn))


def rotate180(ptrn):
    return rotate90(rotate90(ptrn))


def rotate270(ptrn):
    return rotate90(rotate90(rotate90(ptrn)))


def create_rules(lines):
    rules = {}

    for line in lines:
        ptrn, rule = line.split('=>')
        ptrn = ptrn.strip()
        rule = rule.strip()

        for i in range(4):
            rules[ptrn] = rule
            rules[flip(ptrn)] = rule
            ptrn = rotate90(ptrn)
    return rules


def split_grid(grid):
    size = grid.count('/') + 1
    grid = grid.replace('/', '')

    tot = 0
    if size % 2 == 0:
        sub = size // 2
        tot = 2
    elif size % 3 == 0:
        sub = size // 3
        tot = 3
    else:
        print('Whatiness?')

    rows = []
    for row in range(sub):
        c = []
        for col in range(sub):
            block = []
            for j in range(tot * row, tot * (row + 1)):
                line = ''
                for i in range(tot * col, tot * (col + 1)):
                    index = j * size + i
                    line += grid[index]
                block.append(line)
            c.append('/'.join(block))
        rows.append(c)
    return rows


def join(lines):
    grid = [''.join(row) for line in lines for row in zip(*line)]

    return '/'.join(grid)


def apply_rules(rules, grid):
    sub_grids = split_grid(grid)
    result = [[rules[x].split('/') for x in row] for row in sub_grids]

    return join(result)


def active(rules, grid, iterations):
    for i in range(iterations):
        grid = apply_rules(rules, grid)
    return grid.count('#')


if __name__ == '__main__':
    grid = '.#./..#/###'

    with open('day21_test.txt', 'r') as f:
        lines = f.read().splitlines(keepends=False)

    assert flip('abc/def/ghi') == 'cba/fed/ihg'
    assert transpose('ab/cd') == 'ac/bd'
    assert transpose('abc/def/ghi') == 'adg/beh/cfi'
    assert rotate90('abc/def/ghi') == 'gda/heb/ifc'
    assert rotate180('abc/def/ghi') == 'ihg/fed/cba'
    assert rotate270('abc/def/ghi') == 'cfi/beh/adg'

    assert split_grid('abcd/efgh/ijkl/mnop') == [['ab/ef', 'cd/gh'],
                                                 ['ij/mn', 'kl/op']]
    rules = create_rules(lines)

    assert apply_rules(rules, grid) == '#..#/..../..../#..#'

    size_6 = '##.##./#..#../....../##.##./#..#../......'
    assert apply_rules(rules, '#..#/..../..../#..#') == size_6

    grid = '.#./..#/###'
    assert active(rules, grid, 2) == 12

    with open('day21.txt', 'r') as f:
        lines = f.read().splitlines(keepends=False)

    grid = '.#./..#/###'
    rules = create_rules(lines)

    print(active(rules, grid, 5))
    print(active(rules, grid, 18))