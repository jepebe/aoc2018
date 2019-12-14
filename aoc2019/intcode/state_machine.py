from collections import defaultdict


def get_address(state_machine, parameter, write_mode=False):
    mode = state_machine['parameter_modes'][parameter]
    pos = state_machine['pos']

    if mode == 0:
        addr = state_machine['instructions'][pos]
    elif mode == 1:
        if write_mode:
            print('Writing in immediate mode?')
        addr = pos
    elif mode == 2:
        addr = state_machine['instructions'][pos]
        relative_pos = state_machine['relative_pos']
        addr = addr + relative_pos
    else:
        raise ('Unknown addressing mode %i for read' % mode)
    return addr


def read(state_machine, parameter):
    addr = get_address(state_machine, parameter)
    state_machine['pos'] += 1

    if addr >= len(state_machine['instructions']):
        return state_machine['memory'][addr]
    else:
        return state_machine['instructions'][addr]


def write(state_machine, parameter, value):
    addr = get_address(state_machine, parameter, write_mode=True)
    state_machine['pos'] += 1

    if addr >= len(state_machine['instructions']):
        state_machine['memory'][addr] = value
    else:
        state_machine['instructions'][addr] = value


def add(state_machine):
    a = read(state_machine, 0)
    b = read(state_machine, 1)
    write(state_machine, 2, a + b)


def multiply(state_machine):
    a = read(state_machine, 0)
    b = read(state_machine, 1)
    write(state_machine, 2, a * b)


def get_input(state_machine):
    if len(state_machine['input']) == 0:
        state_machine['wait'] = True
        state_machine['pos'] -= 1
        state_machine['instruction_count'] -= 1
    else:
        data = state_machine['input'].pop(0)
        write(state_machine, 0, data)


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
        'memory': defaultdict(int),
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
            2: multiply,
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
    op = opcode % 100
    p1 = ((opcode - op) // 100) % 10
    p2 = ((opcode - op) // 1000) % 10
    p3 = ((opcode - op) // 10000) % 10
    state_machine['operation'] = state_machine['opcodes'][op]
    state_machine['parameter_modes'] = [p1, p2, p3]

    state_machine['pos'] += 1


def run_state_machine(state_machine):
    while not state_machine['halt'] and not state_machine['wait']:
        parse(state_machine)
        operation = state_machine['operation']
        operation(state_machine)
        state_machine['instruction_count'] += 1


def add_input(state_machine, data):
    state_machine['input'].append(data)
    if state_machine['wait']:
        state_machine['wait'] = False


def get_output(state_machine):
    return state_machine['output'].pop(0)


def has_output(state_machine):
    return len(state_machine['output']) > 0


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
