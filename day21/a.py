import sys
R = ['R0', 'R1', 'R2', 'R3', 'R4', 'R5']

#insts = (8, 9, 10, 11, 12, 13, 14, 15)
insts = ()


def print_oprr(regs, ra, rb, rc, p, c, op):
    if p + 2 in insts:
        print(f'[{p+2} {c}] {R[rc]} = {R[ra]}={regs[ra]} {op} {R[rb]}={regs[rb]}')


def print_opri(regs, ra, vb, rc, p, c, op):
    if p + 2 in insts:
        print(f'[{p+2} {c}] {R[rc]} = {R[ra]}={regs[ra]} {op} {vb}')


def print_opir(regs, va, rb, rc, p, c, op):
    if p + 2 in insts:
        print(f'[{p+2} {c}] {R[rc]} = {va} {op} {R[rb]}={regs[rb]}')


def addr(registers, reg_a, reg_b, reg_c, p='', c=''):
    #print_oprr(registers, reg_a, reg_b, reg_c, p, c, '+')
    registers[reg_c] = registers[reg_a] + registers[reg_b]


def addi(registers, reg_a, val_b, reg_c, p='', c=''):
    #print_opri(registers, reg_a, val_b, reg_c, p, c, '+')
    registers[reg_c] = registers[reg_a] + val_b


def mulr(registers, reg_a, reg_b, reg_c, p='', c=''):
    #print_oprr(registers, reg_a, reg_b, reg_c, p, c, '*')
    registers[reg_c] = registers[reg_a] * registers[reg_b]


def muli(registers, reg_a, val_b, reg_c, p='', c=''):
    #print_opri(registers, reg_a, val_b, reg_c, p, c, '*')
    registers[reg_c] = registers[reg_a] * val_b


def banr(registers, reg_a, reg_b, reg_c, p='', c=''):
    #print_oprr(registers, reg_a, reg_b, reg_c, p, c, '&')
    registers[reg_c] = registers[reg_a] & registers[reg_b]


def bani(registers, reg_a, val_b, reg_c, p='', c=''):
    #print_opri(registers, reg_a, val_b, reg_c, p, c, '&')
    registers[reg_c] = registers[reg_a] & val_b


def borr(registers, reg_a, reg_b, reg_c, p='', c=''):
    #print_oprr(registers, reg_a, reg_b, reg_c, p, c, '|')
    registers[reg_c] = registers[reg_a] | registers[reg_b]


def bori(registers, reg_a, val_b, reg_c, p='', c=''):
    #print_opri(registers, reg_a, val_b, reg_c, p, c, '|')
    registers[reg_c] = registers[reg_a] | val_b


def setr(registers, reg_a, _, reg_c, p='', c=''):
    #print(f'[{p} {c}] {R[reg_c]} = {R[reg_a]}={registers[reg_a]}')
    registers[reg_c] = registers[reg_a]


def seti(registers, val_a, _, reg_c, p='', c=''):
    #print(f'[{p} {c}] {R[reg_c]} = {val_a}')
    registers[reg_c] = val_a


def gtir(registers, val_a, reg_b, reg_c, p='', c=''):
    #print_opir(registers, val_a, reg_b, reg_c, p, c, '>')
    registers[reg_c] = 1 if val_a > registers[reg_b] else 0


def gtri(registers, reg_a, val_b, reg_c, p='', c=''):
    #print_opri(registers, reg_a, val_b, reg_c, p, c, '>')
    registers[reg_c] = 1 if registers[reg_a] > val_b else 0


def gtrr(registers, reg_a, reg_b, reg_c, p='', c=''):
    #print_oprr(registers, reg_a, reg_b, reg_c, p, c, '>')
    registers[reg_c] = 1 if registers[reg_a] > registers[reg_b] else 0


def eqir(registers, val_a, reg_b, reg_c, p='', c=''):
    #print_opir(registers, val_a, reg_b, reg_c, p, c, '==')
    registers[reg_c] = 1 if val_a == registers[reg_b] else 0


def eqri(registers, reg_a, val_b, reg_c, p='', c=''):
    #print_opri(registers, reg_a, val_b, reg_c, p, c, '==')
    registers[reg_c] = 1 if registers[reg_a] == val_b else 0


def eqrr(registers, reg_a, reg_b, reg_c, p='', c=''):
    #print_oprr(registers, reg_a, reg_b, reg_c, p, c, '==')
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
        'cycles': 0,
        'pointer': 0,
        'pointer_register': None,
        # 'opcodes': opcodes,
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


def run2(machine, reg0):
    pointer = 0
    pointer_reg = machine['pointer_register']
    registers = [reg0, 0, 0, 0, 0, 0]
    instruction_count = len(machine['instructions'])
    #min_r2 = 9999999999
    halting_codes = set()
    while 0 <= pointer < instruction_count:
        opc, a, b, c = machine['instructions'][pointer]
        registers[pointer_reg] = pointer
        opc(registers, a, b, c, pointer, machine['cycles'])
        pointer = registers[pointer_reg]

        if pointer == 28:
            if not registers[2] in halting_codes:
                halting_codes.add(registers[2])
                print('.', machine['cycles'], registers[2], len(halting_codes))
            else:
                break

            #if registers[a] < min_r2:
            #    min_r2 = registers[a]
            #    print(f'Minimum so far: {min_r2} after { machine["cycles"] }')

        pointer += 1
        machine['cycles'] += 1

    #print(halting_codes)
    #print(sorted(halting_codes, key=lambda x: halting_codes[x])[0:10])
    return machine['cycles']


if __name__ == '__main__':

    lines = sys.stdin.readlines()
    machine = parse_input(lines)

    print('cycles to halt:', run2(machine, 0))
    #Minimum so far: 17813 after 100700213 <- too low?
    #Minimum so far: 8797248 after 1846 <- Puzzle 1

    # 3007673 <- puzzle 2 (16622 halting codes before answer!!!!)



