import sys


def addr(registers, reg_a, reg_b, reg_c):
    registers[reg_c] = registers[reg_a] + registers[reg_b]


def addi(registers, reg_a, val_b, reg_c):
    registers[reg_c] = registers[reg_a] + val_b


def mulr(registers, reg_a, reg_b, reg_c):
    registers[reg_c] = registers[reg_a] * registers[reg_b]


def muli(registers, reg_a, val_b, reg_c):
    registers[reg_c] = registers[reg_a] * val_b


def banr(registers, reg_a, reg_b, reg_c):
    registers[reg_c] = registers[reg_a] & registers[reg_b]


def bani(registers, reg_a, val_b, reg_c):
    registers[reg_c] = registers[reg_a] & val_b


def borr(registers, reg_a, reg_b, reg_c):
    registers[reg_c] = registers[reg_a] | registers[reg_b]


def bori(registers, reg_a, val_b, reg_c):
    registers[reg_c] = registers[reg_a] | val_b


def setr(registers, reg_a, _, reg_c):
    registers[reg_c] = registers[reg_a]


def seti(registers, val_a, _, reg_c):
    registers[reg_c] = val_a


def gtir(registers, val_a, reg_b, reg_c):
    registers[reg_c] = 1 if val_a > registers[reg_b] else 0


def gtri(registers, reg_a, val_b, reg_c):
    registers[reg_c] = 1 if registers[reg_a] > val_b else 0


def gtrr(registers, reg_a, reg_b, reg_c):
    registers[reg_c] = 1 if registers[reg_a] > registers[reg_b] else 0


def eqir(registers, val_a, reg_b, reg_c):
    registers[reg_c] = 1 if val_a == registers[reg_b] else 0


def eqri(registers, reg_a, val_b, reg_c):
    registers[reg_c] = 1 if registers[reg_a] == val_b else 0


def eqrr(registers, reg_a, reg_b, reg_c):
    registers[reg_c] = 1 if registers[reg_a] == registers[reg_b] else 0


opcodes = {
    'addi': addi,
    'addr': addr,
    'seti': seti,
    'setr': setr,
    'muli': muli,
    'mulr': mulr,
    'bani': bani,
    'banr': banr,
    'bori': bori,
    'borr': borr,
    'gtir': gtir,
    'gtri': gtri,
    'gtrr': gtrr,
    'eqir': eqir,
    'eqri': eqri,
    'eqrr': eqrr
}


def parse_input(lines):
    machine = {
        'pointer': 0,
        'pointer_register': None,
        #'opcodes': opcodes,
        'instructions': [],
        'registers': [1, 0, 0, 0, 0, 0]
    }

    for line in lines:
        if line.startswith('#ip'):
            machine['pointer_register'] = int(line[4:])
        elif line.startswith('#'):
            continue
        else:

            opcode, a, b, c = line.strip().split()
            opcode = opcodes[opcode]
            machine['instructions'].append((opcode, int(a), int(b), int(c)))

    return machine


def run(machine):
    while 0 <= machine['pointer'] < len(machine['instructions']):
        pointer = machine['pointer']
        registers = machine['registers']
        opc, a, b, c = machine['instructions'][pointer]

        registers[machine['pointer_register']] = pointer
        opc(registers, a, b, c)
        machine['pointer'] = registers[machine['pointer_register']]

        machine['pointer'] += 1

        print(pointer, registers)


def run2(machine):
    pointer = 0
    pointer_reg = machine['pointer_register']
    registers = [1, 0, 0, 0, 0, 0]
    instruction_count = len(machine['instructions'])
    cycles = 0
    while 0 <= pointer < instruction_count:
        opc, a, b, c = machine['instructions'][pointer]
        registers[pointer_reg] = pointer
        cp = registers[:]
        opc(registers, a, b, c)
        pointer = registers[pointer_reg]

        if cp[0] != registers[0]:
            print(pointer, cycles, cp, registers)

        pointer += 1
        cycles += 1
        # print(pointer, registers, cycles)

        if pointer in (26, 35):
            print('Created number %d' % registers[4])


def run3(number=10551275):
    s = 0
    hit = 0
    for r1 in range(1, number + 1):
        # print(r1)
        if number % r1 == 0:
            s += r1
        # for r2 in range(number - hit, 0, -1):
        #     if r1 * r2 == number:
        #         s += r1
        #         hit = r1
        #         print(r1)

    print(s)

lines = sys.stdin.readlines()

machine = parse_input(lines)

run3(875)
run3()
#run2(machine)




# 1632?