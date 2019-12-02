import sys

lines = sys.stdin.readline().split(',')
opcodes = [int(x) for x in lines]


def add(opcodes, pos):
    addr_a = opcodes[pos + 1]
    addr_b = opcodes[pos + 2]
    addr_c = opcodes[pos + 3]

    opcodes[addr_c] = opcodes[addr_a] + opcodes[addr_b]
    return pos + 4


def mult(opcodes, pos):
    addr_a = opcodes[pos + 1]
    addr_b = opcodes[pos + 2]
    addr_c = opcodes[pos + 3]

    opcodes[addr_c] = opcodes[addr_a] * opcodes[addr_b]
    return pos + 4


instructions = {1: add, 2: mult}


def run(opcodes):
    pos = 0
    while opcodes[pos] != 99:
        op = opcodes[pos]
        pos = instructions[op](opcodes, pos)
    return opcodes


assert (run([1, 0, 0, 0, 99]) == [2, 0, 0, 0, 99])
assert (run([2, 3, 0, 3, 99]) == [2, 3, 0, 6, 99])
assert (run([2, 4, 4, 5, 99, 0]) == [2, 4, 4, 5, 99, 9801])
assert (run([1, 1, 1, 4, 99, 5, 6, 0, 99]) == [30, 1, 1, 4, 2, 5, 6, 0, 99])
assert (run([1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50]) == [3500, 9, 10, 70, 2, 3, 11, 0, 99, 30, 40, 50])


def intcode(opcodes, noun, verb):
    opcodes = list(opcodes)
    opcodes[1] = noun
    opcodes[2] = verb
    result = run(opcodes)
    return result[0]


assert(intcode(opcodes, opcodes[1], opcodes[2]) == 655695)

assert(intcode(opcodes, 12, 2) == 3085697)

for noun in range(0, 100):
    for verb in range(0, 100):

        if intcode(opcodes, noun, verb) == 19690720:
            print(noun, verb, 100 * noun + verb)


