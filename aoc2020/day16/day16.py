from functools import reduce

import intcode as ic

tester = ic.Tester('Ticket Translation')


def read_file(postfix=''):
    with open(f'input{postfix}') as f:
        lines = f.readlines()
    return lines


def parse(lines):
    ranges = {}
    my_ticket = None
    nearby = []
    mode = 'range'
    for line in lines:
        line = line.strip()
        if not line:
            continue
        elif line.startswith('your'):
            mode = 'your'
            continue
        elif line.startswith('nearby'):
            mode = 'nearby'
            continue
        if mode == 'range':
            attr, r = line.split(': ')
            r1, r2 = r.split(' or ')
            r11, r12 = list(map(int, r1.split('-')))
            r21, r22 = list(map(int, r2.split('-')))
            ranges[attr] = (r11, r12, r21, r22)
        elif mode == 'your':
            my_ticket = list(map(int, line.split(',')))
        elif mode == 'nearby':
            nearby.append(list(map(int, line.split(','))))

    return ranges, my_ticket, nearby


def find_valid(ranges, nearby):
    valid = {}
    for a, b, c, d in ranges.values():
        for i in range(a, b + 1):
            valid[i] = True
        for i in range(c, d + 1):
            valid[i] = True

    error = 0
    valid_tickets = []
    for ticket in nearby:
        v = True
        for n in ticket:
            if n not in valid:
                error += n
                v = False
        if v:
            valid_tickets.append(ticket)
    return error, valid_tickets


def find_fields(ranges, nearby, my_ticket):
    fields = {}
    t = list(map(list, zip(*nearby)))
    matches = {}
    for attr, rng in ranges.items():
        a, b, c, d = rng
        matches[attr] = []
        for i, column in enumerate(t):
            valid = True
            for v in column:
                if a <= v <= b or c <= v <= d:
                    pass
                else:
                    valid = False

            if valid:
                matches[attr].append(i)

    while len(matches) > 0:
        for attr, m in matches.items():
            if len(m) == 1:
                idx = m[0]
                fields[attr] = my_ticket[idx]
                for v in matches.values():
                    if idx in v:
                        v.remove(idx)
        matches = {k: v for k, v in matches.items() if v}

    return fields


lines = """class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12""".splitlines()

ranges, my_ticket, nearby = parse(lines)
error, _ = find_valid(ranges, nearby)
tester.test_value(error, 71)

ranges, my_ticket, nearby = parse(read_file())
error, _ = find_valid(ranges, nearby)
tester.test_value(error, 23954, 'solution to part 1=%s')


lines = """class: 0-1 or 4-19
row: 0-5 or 8-19
seat: 0-13 or 16-19

your ticket:
11,12,13

nearby tickets:
3,9,18
15,1,5
5,14,9""".splitlines()

ranges, my_ticket, nearby = parse(lines)
_, nearby = find_valid(ranges, nearby)
fields = find_fields(ranges, nearby, my_ticket)
tester.test_value(fields, {'class': 12, 'row': 11, 'seat': 13})

ranges, my_ticket, nearby = parse(read_file())
_, nearby = find_valid(ranges, nearby)
fields = find_fields(ranges, nearby, my_ticket)
dep_fields = [fields[f] for f in fields if f.startswith('departure')]
checksum = reduce(lambda x, y: x * y, dep_fields)
tester.test_value(checksum, 453459307723, 'solution to part 2=%s')

