from itertools import permutations
from intcode import Tester, lcms


def load_moons(filename):
    moons = []
    with open(filename) as f:
        for line in f.readlines():
            line = line.replace('<', '')
            line = line.replace('>', '')
            coords = line.split(',')
            x, y, z = [int(c.split('=')[1]) for c in coords]
            moon = {
                'position': (x, y, z),
                'velocity': (0, 0, 0),
            }
            moons.append(moon)
    return moons


def gravity(a, b):
    def g(a, b):
        grav = 0
        if a < b:
            grav = +1
        elif a > b:
            grav = -1
        return grav

    return g(a[0], b[0]), g(a[1], b[1]), g(a[2], b[2])


def step_moons(moons):
    for a, b in permutations(moons, 2):
        g = gravity(a['position'], b['position'])
        av = a['velocity']
        a['velocity'] = av[0] + g[0], av[1] + g[1], av[2] + g[2]

    for moon in moons:
        ap = moon['position']
        av = moon['velocity']
        moon['position'] = ap[0] + av[0], ap[1] + av[1], ap[2] + av[2]


def energy(moons):
    energy = 0
    for moon in moons:
        mp = moon['position']
        mv = moon['velocity']
        p = abs(mp[0]) + abs(mp[1]) + abs(mp[2])
        k = abs(mv[0]) + abs(mv[1]) + abs(mv[2])
        energy += p * k
    return energy


def run_simulation(moons, steps):
    for i in range(steps):
        step_moons(moons)
    return energy(moons)


def find_periodicity_for_axis(moons, axis):
    initial = [(m['position'][axis], m['velocity'][axis]) for i, m in enumerate(moons)]

    iterations = 0
    while True:
        iterations += 1
        step_moons(moons)
        current = [(m['position'][axis], m['velocity'][axis]) for i, m in enumerate(moons)]
        if current == initial:
            return iterations


def find_periodicity(moons):
    a = find_periodicity_for_axis(moons, 0)
    b = find_periodicity_for_axis(moons, 1)
    c = find_periodicity_for_axis(moons, 2)
    return lcms(a, b, c)


tester = Tester('moons')

moons = load_moons('test1')
run_simulation(moons, 10)
tester.test_value(energy(moons), 179)

moons = load_moons('test2')
run_simulation(moons, 100)
tester.test_value(energy(moons), 1940)

moons = load_moons('input')
run_simulation(moons, 1000)
tester.test_value(energy(moons), 10845)

moons = load_moons('test1')
tester.test_value(find_periodicity(moons), 2772)

moons = load_moons('test2')
tester.test_value(find_periodicity(moons), 4686774924)

moons = load_moons('input')
tester.test_value(find_periodicity(moons), 551272644867044)

tester.summary()






