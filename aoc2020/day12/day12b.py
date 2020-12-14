import intcode as ic

tester = ic.Tester('Rain Risk')


def rotate_left(string, n):
    return string[n:] + string[:n]


def rotate_right(string, n):
    return string[-n:] + string[:-n]


def read_file(postfix=''):
    with open(f'input{postfix}') as f:
        lines = f.readlines()
    return lines


def N(boat, units):
    n, e = boat['waypoint']
    boat['waypoint'] = n + units, e


def S(boat, units):
    n, e = boat['waypoint']
    boat['waypoint'] = n - units, e


def E(boat, units):
    n, e = boat['waypoint']
    boat['waypoint'] = n, e + units


def W(boat, units):
    n, e = boat['waypoint']
    boat['waypoint'] = n, e - units


def L(boat, units):
    units = units // 90
    n, e = boat['waypoint']

    for i in range(units):
        n, e = e, -n
    boat['waypoint'] = (n, e)


def R(boat, units):
    units = units // 90
    n, e = boat['waypoint']

    for i in range(units):
        n, e = -e, n
    boat['waypoint'] = (n, e)


def F(boat, units):
    n, e = boat['waypoint']
    boat['N'] += n * units
    boat['E'] += e * units


def navigate(lines):
    boat = {'N': 0, 'E': 0, 'waypoint': (1, 10)}
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

tester.test_value(navigate(lines), 286)

tester.test_value(navigate(read_file()), 40014, 'solution to exercise 2=%s')
