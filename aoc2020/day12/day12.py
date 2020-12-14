import intcode as ic

tester = ic.Tester('Rain Risk')


def read_file(postfix=''):
    with open(f'input{postfix}') as f:
        lines = f.readlines()
    return lines


def rotate_left(string, n):
    return string[n:] + string[:n]


def rotate_right(string, n):
    return string[-n:] + string[:-n]


def N(boat, units):
    boat['N'] += units


def S(boat, units):
    boat['N'] -= units


def E(boat, units):
    boat['E'] += units


def W(boat, units):
    boat['E'] -= units


def L(boat, units):
    units = units // 90
    boat['direction'] = rotate_right(boat['direction'], units)


def R(boat, units):
    units = units // 90
    boat['direction'] = rotate_left(boat['direction'], units)


def F(boat, units):
    direction = boat['direction'][0]
    if direction == 'N':
        N(boat, units)
    elif direction == 'S':
        S(boat, units)
    elif direction == 'E':
        E(boat, units)
    elif direction == 'W':
        W(boat, units)


def navigate(lines):
    boat = {'direction': 'ESWN', 'N': 0, 'E': 0}
    for line in lines:
        op = line[0]
        units = int(line[1:])
        if op == 'N':
            N(boat, units)
        elif op == 'S':
            S(boat, units)
        elif op == 'E':
            E(boat, units)
        elif op == 'W':
            W(boat, units)
        elif op == 'L':
            L(boat, units)
        elif op == 'R':
            R(boat, units)
        elif op == 'F':
            F(boat, units)
    print(boat)
    return abs(boat['N']) + abs(boat['E'])


lines = """F10
N3
F7
R90
F11""".split('\n')

tester.test_value(navigate(lines), 25)

tester.test_value(navigate(read_file()), 441, 'solution to exercise 1=%s')
