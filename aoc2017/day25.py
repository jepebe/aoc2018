import re

begin = re.compile('Begin in state ([A-Z]).')
diag = re.compile('Perform a diagnostic checksum after ([0-9]+) steps.')
in_stat = re.compile('In state ([A-Z]):')
if_cur = re.compile('\s+If the current value is ([0|1]):')
wr_val = re.compile('\s+- Write the value ([0|1]).')
mv_cur = re.compile('\s+- Move one slot to the (right|left).')
cont = re.compile('\s+- Continue with state ([A-Z]).')


def match(ptrn, line):
    return ptrn.match(line).group(1)


def test_regex(ptrn, line, expected):
    match = ptrn.match(line)
    return match and match.group(1) == expected


def create_sub_routine(lines):
    name = match(in_stat, lines[0])

    def state_machine(program):
        cur = program['cursor']
        tape = program['tape']

        if tape.get(cur, 0) == 0:
            tape[cur] = int(match(wr_val, lines[2]))
            cur += -1 if match(mv_cur, lines[3]) == 'left' else 1
            next_state = match(cont, lines[4])
        else:
            tape[cur] = int(match(wr_val, lines[6]))
            cur += -1 if match(mv_cur, lines[7]) == 'left' else 1
            next_state = match(cont, lines[8])

        program['cursor'] = cur
        program['next_state'] = next_state

    return name, state_machine


def parse(lines):
    program = {
        'cursor': 0,
        'tape': {},
        'next_state': match(begin, lines[0]),
        'count': 0,
        'n': int(match(diag, lines[1])),
        'state_machines': {}
    }

    i = 2
    while i < len(lines):
        if in_stat.match(lines[i]):
            name, state_machine = create_sub_routine(lines[i:i + 9])
            program['state_machines'][name] = state_machine
            i += 9
        else:
            i += 1

    return program


def run(program):
    while program['count'] < program['n']:
        next_state = program['next_state']
        state_machine = program['state_machines'][next_state]
        state_machine(program)

        if program['count'] % 1000000 == 0:
            print(program)
        program['count'] += 1

    return len([x for x in program['tape'].values() if x == 1])



if __name__ == '__main__':
    with open('day25_test.txt', 'r') as f:
        lines = f.readlines()

    assert test_regex(begin, lines[0], 'A')
    assert test_regex(diag, lines[1], '6')
    assert test_regex(in_stat, lines[3], 'A')
    assert test_regex(if_cur, lines[4], '0')
    assert test_regex(wr_val, lines[5], '1')
    assert test_regex(mv_cur, lines[6], 'right')
    assert test_regex(cont, lines[7], 'B')
    assert test_regex(if_cur, lines[8], '1')
    assert test_regex(wr_val, lines[9], '0')
    assert test_regex(mv_cur, lines[10], 'left')
    assert test_regex(cont, lines[11], 'B')

    program = parse(lines)
    assert run(program) == 3

    with open('day25.txt', 'r') as f:
        lines = f.readlines()

    program = parse(lines)
    assert run(program) == 4217
