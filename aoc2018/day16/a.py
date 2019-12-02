import sys

lines = sys.stdin.readlines()


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


opcodes = [addr, addi, mulr, muli, banr, bani, bori, borr, setr, seti, gtir, gtri, gtrr, eqir, eqri, eqrr]


def test_opcodes(candidates, registers, instruction, expected):
    counter = 0
    opcode = instruction[0]

    if opcode not in candidates:
        candidates[opcode] = {'samples': 0, '3ormore': 0}
    candidates[opcode]['samples'] += 1

    for opc in opcodes:
        reg_copy = registers[:]
        opc(reg_copy, *instruction[1:])
        # print(registers, instruction, reg_copy, expected, opc)
        if reg_copy == expected:
            if opc not in candidates[opcode]:
                candidates[opcode][opc] = 0

            candidates[opcode][opc] += 1
            counter += 1
        else:
            if opc in candidates[opcode]:
                candidates[opcode][opc] -= 1
    if counter >= 3:
        candidates[opcode]['3ormore'] += 1


def parse_instructions(lines):
    candidates = {}
    registers = [0, 0, 0, 0]
    instruction = None

    for line in lines:
        if line.strip() == '':
            continue
        elif line.startswith('Before'):
            registers = list(map(int, line[9:line.index(']')].split(', ')))

        elif line.startswith('After'):
            expected = list(map(int, line[9:line.index(']')].split(', ')))
            test_opcodes(candidates, registers, instruction, expected)
        else:
            instruction = list(map(int, line.strip().split()))
    return candidates


def prune(candidates):
    pruned = 0
    for candidate in candidates.values():
        candidate['list'] = []
        for opc in opcodes:
            if opc in candidate and candidate[opc] < candidate['samples']:
                del candidate[opc]
                pruned += 1
            elif opc in candidate and candidate[opc] == candidate['samples']:
                candidate['list'].append(opc)

    for i in range(16):
        for candidate in candidates.values():
            if len(candidate['list']) == 1:
                opc = candidate['list'][0]

                for cndt in candidates.values():
                    if candidate != cndt and opc in cndt['list']:
                        cndt['list'].remove(opc)
                        pruned += 1
    print('pruned %d opcodes' % pruned)


def create_instruction_set(candidates):
    instruction_set = {}

    for candidate in candidates:
        instruction_set[candidate] = candidates[candidate]['list'][0]
    return instruction_set


candidates = parse_instructions(lines)
prune(candidates)
instruction_set = create_instruction_set(candidates)

print(instruction_set)
print([instruction_set[m].__name__ for m in sorted(instruction_set)])

opcode_counter = 0
for opc in sorted(candidates):
    # print(opc, candidates[opc]['list'])
    opcode_counter += candidates[opc]['3ormore']

print('opcode count > 3 = %d' % opcode_counter)  # 646
