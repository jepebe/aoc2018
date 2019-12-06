import sys

lines = sys.stdin.readline().split(',')
instructions = [int(x) for x in lines]


def read(state_machine, parameter):
    mode = state_machine['parameter_modes'][parameter]
    pos = state_machine['pos']
    state_machine['pos'] += 1
    if mode == 0:
        addr = state_machine['instructions'][pos]
        return state_machine['instructions'][addr]
    elif mode == 1:
        return state_machine['instructions'][pos]
    else:
        raise ('Unknown addressing mode %i for read' % mode)


def write(state_machine, parameter, value):
    mode = state_machine['parameter_modes'][parameter]
    pos = state_machine['pos']
    state_machine['pos'] += 1
    if mode == 0:
        addr = state_machine['instructions'][pos]
        state_machine['instructions'][addr] = value
    elif mode == 1:
        print('Writing in immediate mode?')
        state_machine['instructions'][pos] = value
    else:
        raise ('Unknown addressing mode %i for write' % mode)


def add(state_machine):
    a = read(state_machine, 0)
    b = read(state_machine, 1)
    write(state_machine, 2, a + b)


def mult(state_machine):
    a = read(state_machine, 0)
    b = read(state_machine, 1)
    write(state_machine, 2, a * b)


def get_input(state_machine):
    inpt = state_machine['input'].pop(0)
    write(state_machine, 0, inpt)


def output(state_machine):
    value = read(state_machine, 0)
    state_machine['output'].append(value)
    print('Output from state machine %s' % value)


def jump_if_true(state_machine):
    a = read(state_machine, 0)
    b = read(state_machine, 1)
    if a != 0:
        state_machine['pos'] = b


def jump_if_false(state_machine):
    a = read(state_machine, 0)
    b = read(state_machine, 1)
    if a == 0:
        state_machine['pos'] = b


def less_than(state_machine):
    a = read(state_machine, 0)
    b = read(state_machine, 1)

    write(state_machine, 2, 1 if a < b else 0)


def equals(state_machine):
    a = read(state_machine, 0)
    b = read(state_machine, 1)

    write(state_machine, 2, 1 if a == b else 0)


def halt(state_machine):
    state_machine['halt'] = True
    # print('Instruction count: %i' % state_machine['instruction_count'])


def create_state_machine(instructions):
    return {
        'instructions': list(instructions),
        'operation': 0,
        'parameter_modes': [0],
        'pos': 0,
        'instruction_count': 0,
        'input': [1],
        'output': [],
        'opcodes': {
            1: add,
            2: mult,
            3: get_input,
            4: output,
            5: jump_if_true,
            6: jump_if_false,
            7: less_than,
            8: equals,
            99: halt
        },
        'halt': False
    }


def parse(state_machine):
    pos = state_machine['pos']
    opcode = state_machine['instructions'][pos]
    opcode = str(opcode)
    opcode = '0' * (5 - len(opcode)) + opcode
    state_machine['operation'] = state_machine['opcodes'][int(opcode[3:])]
    state_machine['parameter_modes'] = [int(opcode[2]), int(opcode[1]), int(opcode[0])]

    state_machine['pos'] += 1


def run(state_machine):
    while not state_machine['halt']:
        parse(state_machine)
        operation = state_machine['operation']
        operation(state_machine)
        state_machine['instruction_count'] += 1


def test_state_machine(instructions, result):
    sm = create_state_machine(instructions)
    run(sm)
    if sm['instructions'] != result:
        print('%s != %s' % (sm['instructions'], result))
        raise AssertionError


def test_state_machine_output(instructions, input, output):
    sm = create_state_machine(instructions)
    sm['input'] = [input]
    run(sm)
    if sm['output'] != [output]:
        print('%s != %s' % (sm['output'], [output]))
        raise AssertionError


test_state_machine([1, 0, 0, 0, 99], [2, 0, 0, 0, 99])
test_state_machine([2, 3, 0, 3, 99], [2, 3, 0, 6, 99])
test_state_machine([2, 4, 4, 5, 99, 0], [2, 4, 4, 5, 99, 9801])
test_state_machine([1, 1, 1, 4, 99, 5, 6, 0, 99], [30, 1, 1, 4, 2, 5, 6, 0, 99])
test_state_machine([1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50],
                   [3500, 9, 10, 70, 2, 3, 11, 0, 99, 30, 40, 50])

run(create_state_machine(instructions))

test_state_machine_output([3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], 7, 0)
test_state_machine_output([3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], 8, 1)

test_state_machine_output([3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8], 7, 1)
test_state_machine_output([3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8], 8, 0)

test_state_machine_output([3, 3, 1108, -1, 8, 3, 4, 3, 99], 8, 1)
test_state_machine_output([3, 3, 1108, -1, 8, 3, 4, 3, 99], 7, 0)

test_state_machine_output([3, 3, 1107, -1, 8, 3, 4, 3, 99], 7, 1)
test_state_machine_output([3, 3, 1107, -1, 8, 3, 4, 3, 99], 8, 0)

test_state_machine_output([3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9], 0, 0)
test_state_machine_output([3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9], 1, 1)

test_state_machine_output([3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1], 0, 0)
test_state_machine_output([3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1], 1, 1)

inst = [3, 21, 1008, 21, 8, 20, 1005, 20, 22, 107, 8, 21, 20, 1006, 20, 31,
        1106, 0, 36, 98, 0, 0, 1002, 21, 125, 20, 4, 20, 1105, 1, 46, 104,
        999, 1105, 1, 46, 1101, 1000, 1, 20, 4, 20, 1105, 1, 46, 98, 99]

test_state_machine_output(inst, 7, 999)
test_state_machine_output(inst, 8, 1000)
test_state_machine_output(inst, 9, 1001)

state_machine = create_state_machine(instructions)
state_machine['input'] = [5]
run(state_machine)
assert state_machine['output'] == [773660]
