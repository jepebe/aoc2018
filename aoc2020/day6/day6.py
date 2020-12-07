import intcode as ic

tester = ic.Tester('Custom Customs')


def read_file():
    with open('input') as f:
        lines = f.read()
    return lines.split('\n')


def parse_lines(lines):
    groups = {0: {'unique': set(), 'all': {}, 'p': 0}}
    i = 0
    for line in lines:

        if line == '':
            i += 1
            groups[i] = {'unique': set(), 'all': {}, 'p': 0}
        else:
            groups[i]['p'] += 1
            for c in line:
                groups[i]['unique'].add(c)
                if c not in groups[i]['all']:
                    groups[i]['all'][c] = 0
                groups[i]['all'][c] += 1

    unique = sum(len(item['unique']) for item in groups.values())
    all_in_group = 0
    for g in groups.values():
        p = g['p']

        for q in g['all'].values():
            if q == p:
                all_in_group += 1

    return unique, all_in_group


lines = """abc

a
b
c

ab
ac

a
a
a
a

b""".split('\n')

tester.test_value(parse_lines(lines), (11, 6))

lines = read_file()
answers = parse_lines(lines)
tester.test_value(answers, (6504, 3351), 'solution to exercise 1=%s and 2=%s')

