import intcode as ic

tester = ic.Tester('Medicine for Rudolph')


def read_file(postfix=''):
    with open(f'input{postfix}') as f:
        lines = f.readlines()
    return lines


def parse(lines):
    replacements = {}
    r = []
    u = set()

    molecule = None
    for line in lines:
        line = line.strip()
        if not line or molecule:
            molecule = True
            continue
        else:
            f, t = line.split(' => ')

            if f not in replacements:
                replacements[f] = []
            r.append(t)
            u.add(t)
            replacements[f].append(t)
    molecule = line

    return replacements, molecule


def count_replacements(replacement_table, molecule):
    variants = set()
    for i, c in enumerate(molecule):
        if i < len(molecule) - 1 and f'{c}{molecule[i + 1]}' in replacement_table:
            c = f'{c}{molecule[i + 1]}'

        if c in replacement_table:
            a = ''
            if i > 0:
                a = molecule[:i]
            b = molecule[i + len(c):]
            replacements = replacement_table[c]
        else:
            continue

        for replacement in replacements:
            variants.add(f'{a}{replacement}{b}')

    # print(variants)
    return len(variants)


def backwards(replacement_table, molecule):
    r = {}
    for key, replacements in replacement_table.items():
        for replacement in replacements:
            r[replacement] = key

    iterations = 0
    changes = -1
    fab = molecule
    while fab != 'e' and changes != 0:
        changes = 0
        for replacement in reversed(sorted(r.keys())):
            count = fab.count(replacement)
            if count > 0:
                fab = fab.replace(replacement, r[replacement])
            iterations += count
            changes += count
    return iterations


lines = """e => H
e => O
H => HO
H => OH
O => HH

HOH""".split('\n')

replacements, molecule = parse(lines)
replacement_count = count_replacements(replacements, molecule)
tester.test_value(replacement_count, 4)
tester.test_value(backwards(replacements, molecule), 3)

lines = """e => H
e => O
H => HO
H => OH
O => HH

HOHOHO""".split('\n')

replacements, molecule = parse(lines)
replacement_count = count_replacements(replacements, molecule)
tester.test_value(replacement_count, 7)
tester.test_value(backwards(replacements, molecule), 6)


replacements, molecule = parse(read_file())
replacement_count = count_replacements(replacements, molecule)
tester.test_value(replacement_count, 518, 'solution to exercise 1=%s')

tester.test_value(backwards(replacements, molecule), 200, 'solution to exercise 2=%s')
