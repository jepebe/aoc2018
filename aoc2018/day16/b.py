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


opcodes = [seti, eqir, setr, gtir, addi, muli, mulr, gtrr, bani, gtri, bori, banr, borr, eqri, eqrr, addr]

registers = [0, 0, 0, 0]

lines = sys.stdin.readlines()

for line in lines:
    opcode, a, b, c = list(map(int, line.strip().split()))
    opcode = opcodes[opcode]
    opcode(registers, a, b, c)

print(registers)
