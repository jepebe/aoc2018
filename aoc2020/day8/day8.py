import intcode as ic

tester = ic.Tester('Handheld Halting')


def read_file(postfix=''):
    with open(f'input{postfix}') as f:
        lines = f.readlines()
    return lines


def NOP(cpu):
    # if cpu['pc'] + cpu['immediate'] == len(cpu['program']):
    #     print(f'change ${cpu["pc"]}')
    pass


def ACC(cpu):
    cpu['a'] += cpu['immediate']


def JMP(cpu):
    cpu['pc'] += cpu['immediate'] - 1
    # print(f'jmp to ${cpu["pc"] + 2}')


def clock(cpu):
    cpu['clock'] += 1
    opcode, immediate = cpu['program'][cpu['pc']].split(' ')

    if opcode in ('jmp', 'nop'):
        if cpu['jmp_nop_switch'] == cpu['jmp_nop_count']:
            if opcode == 'jmp':
                opcode = 'nop'
            else:
                opcode = 'jmp'
            # print(f'switch to {opcode} at ${cpu["pc"]}')
        cpu['jmp_nop_count'] += 1

    #     print(f'${cpu["pc"] + 1:<4} {opcode} ${imm:<5} | {cpu["clock"]}')
    cpu['immediate'] = int(immediate)
    cpu['instructions'][opcode](cpu)
    cpu['pc'] += 1


def run(cpu):
    visited = set()
    while cpu['pc'] < len(cpu['program']) and cpu['pc'] not in visited:
        visited.add(cpu['pc'])
        a = cpu['a']
        clock(cpu)

    if cpu['pc'] >= len(cpu['program']):
        a = cpu['a']

    return a, cpu['pc'] in visited


def disassemble(program):
    pc = 1
    for line in program:
        opcode, immediate = line.split(' ')
        immediate = int(immediate)
        if opcode in ('jmp', 'nop'):
            immediate = f'${pc + immediate}'

        print(f'${pc:<4} {opcode} {immediate:<5}')

        pc += 1


def reset(cpu):
    cpu['a'] = 0
    cpu['pc'] = 0
    cpu['immediate'] = None
    cpu['clock'] = 0
    cpu['jmp_nop_count'] = 0


def create_cpu(data):
    cpu = {
        'a': 0,
        'pc': 0,
        'immediate': None,
        'instructions': {
            'nop': NOP,
            'acc': ACC,
            'jmp': JMP
        },
        'program': data,
        'clock': 0,
        'jmp_nop_count': 0,
        'jmp_nop_switch': -1
    }
    return cpu


def find_jmp_nop(cpu):
    for i in range(len(cpu['program'])):
        cpu['jmp_nop_switch'] = i
        reset(cpu)
        a, halt = run(cpu)
        if not halt:
            return a, halt



program = """nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6""".split('\n')

# disassemble(program)
cpu = create_cpu(program)

tester.test_value(run(cpu), (5, True))

cpu = create_cpu(read_file())
tester.test_value(run(cpu), (2058, True))

cpu = create_cpu(program)
tester.test_value(find_jmp_nop(cpu), (8, False))

# disassemble(read_file())
cpu = create_cpu(read_file())
tester.test_value(find_jmp_nop(cpu), (1000, False))
