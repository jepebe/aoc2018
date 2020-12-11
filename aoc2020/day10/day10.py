import intcode as ic

tester = ic.Tester('Adapter Array')


def read_file(postfix=''):
    with open(f'input{postfix}') as f:
        lines = f.readlines()
    return list(sorted(map(int, lines)))


def joltages(adapters):
    diffs = {}
    joltage = 0
    for adapter in adapters:
        diff = adapter - joltage
        if diff not in diffs:
            diffs[diff] = 0
        diffs[diff] += 1
        joltage = adapter
    diffs[3] += 1

    return diffs, diffs[1] * diffs[3]


def arrange_adapters(adapters: list):
    adapters.insert(0, 0)
    adapters.append(adapters[-1] + 3)

    group_idx = 0
    groups = []
    for i, adapter in enumerate(adapters):
        if i > 0 and adapter - adapters[i - 1] == 3:
            groups.append(adapters[group_idx:i])
            group_idx = i

    groups.append(adapters[group_idx:len(adapters)])

    paths = 1
    for group in groups:
        if len(group) in (1, 2):
            continue

        if len(group) - 2 == 1:
            if group[-1] - group[0] <= 3:
                paths *= 2

        if len(group) - 2 == 2:
            if group[-1] - group[0] <= 3:
                paths *= 4

        if len(group) - 2 == 3:
            if group[-1] - group[0] > 3:
                paths *= 7

    return paths


numbers = list(sorted(map(int, """16 10 15 5 1 11 7 19 6 12 4""".split())))

tester.test_value(joltages(numbers), ({1: 7, 3: 5}, 35))
tester.test_value(arrange_adapters(numbers), 8)

numbers = list(sorted(map(int, """28 33 18 42 31 14 46 20 48 47 24 23 49 45 19 38 
                          39 11 1 32 25 35 8 17 7 9 4 2 34 10 3""".split())))
tester.test_value(joltages(numbers), ({1: 22, 3: 10}, 220))
tester.test_value(arrange_adapters(numbers), 19208)

numbers = read_file()
jolts, mult = joltages(numbers)
routes = arrange_adapters(numbers)
tester.test_value(jolts, {1: 74, 3: 41})
tester.test_value(mult, 3034, 'solution to exercise 1=%s')
tester.test_value(routes, 259172170858496, 'solution to exercise 2=%s')
