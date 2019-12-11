def read(state_machine, parameter):
    mode = state_machine['parameter_modes'][parameter]
    pos = state_machine['pos']
    state_machine['pos'] += 1
    if mode == 0:
        addr = state_machine['instructions'][pos]
    elif mode == 1:
        addr = pos
    elif mode == 2:
        addr = state_machine['instructions'][pos]
        rpos = state_machine['relative_pos']
        addr = addr + rpos
    else:
        raise ('Unknown addressing mode %i for read' % mode)

    if addr >= len(state_machine['instructions']):
        return 0 if not addr in state_machine['memory'] else state_machine['memory'][addr]
    else:
        return state_machine['instructions'][addr]


def write(state_machine, parameter, value):
    mode = state_machine['parameter_modes'][parameter]
    pos = state_machine['pos']
    state_machine['pos'] += 1
    if mode == 0:
        addr = state_machine['instructions'][pos]
    elif mode == 1:
        print('Writing in immediate mode?')
        addr = pos
    elif mode == 2:
        addr = state_machine['instructions'][pos]
        rpos = state_machine['relative_pos']
        addr = addr + rpos
    else:
        raise ('Unknown addressing mode %i for write' % mode)

    if addr >= len(state_machine['instructions']):
        state_machine['memory'][addr] = value
    else:
        state_machine['instructions'][addr] = value


def add(state_machine):
    a = read(state_machine, 0)
    b = read(state_machine, 1)
    write(state_machine, 2, a + b)


def mult(state_machine):
    a = read(state_machine, 0)
    b = read(state_machine, 1)
    write(state_machine, 2, a * b)


def get_input(state_machine):
    if len(state_machine['input']) == 0:
        state_machine['wait'] = True
        state_machine['pos'] -= 1
    else:
        inpt = state_machine['input'].pop(0)
        write(state_machine, 0, inpt)


def output(state_machine):
    value = read(state_machine, 0)
    state_machine['output'].append(value)
    if state_machine['output_enabled']:
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


def adjust_relative(state_machine):
    a = read(state_machine, 0)
    state_machine['relative_pos'] += a


def halt(state_machine):
    state_machine['halt'] = True
    # print('Instruction count: %i' % state_machine['instruction_count'])


def create_state_machine(instructions):
    return {
        'instructions': list(instructions),
        'memory': {},
        'operation': 0,
        'parameter_modes': [0],
        'pos': 0,
        'relative_pos': 0,
        'instruction_count': 0,
        'input': [],
        'output': [],
        'output_enabled': False,
        'opcodes': {
            1: add,
            2: mult,
            3: get_input,
            4: output,
            5: jump_if_true,
            6: jump_if_false,
            7: less_than,
            8: equals,
            9: adjust_relative,
            99: halt
        },
        'halt': False,
        'wait': False
    }


def parse(state_machine):
    pos = state_machine['pos']
    opcode = state_machine['instructions'][pos]
    opcode = str(opcode)
    opcode = '0' * (5 - len(opcode)) + opcode
    state_machine['operation'] = state_machine['opcodes'][int(opcode[3:])]
    state_machine['parameter_modes'] = [int(opcode[2]), int(opcode[1]), int(opcode[0])]

    state_machine['pos'] += 1


def run_state_machine(state_machine):
    while not state_machine['halt'] and not state_machine['wait']:
        parse(state_machine)
        operation = state_machine['operation']
        operation(state_machine)
        state_machine['instruction_count'] += 1


def add_input(state_machine, input):
    state_machine['input'].append(input)
    if state_machine['wait']:
        state_machine['wait'] = False


def get_output(state_machine):
    return state_machine['output'].pop(0)


def load_instructions(filename):
    with open(filename) as f:
        instructions = f.readline().split(',')
        instructions = [int(x) for x in instructions]
    return instructions


def load_state_machine(filename):
    instructions = load_instructions(filename)
    return create_state_machine(instructions)


def is_running(state_machine):
    return not state_machine['halt']
