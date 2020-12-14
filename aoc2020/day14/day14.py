import itertools

import intcode as ic

tester = ic.Tester('Docking Data')


def read_file(postfix=''):
    with open(f'input{postfix}') as f:
        lines = f.readlines()
    return lines


def maskify(lines):
    mem = {}
    set_mask = 0
    clear_mask = 1
    for line in lines:
        op, value = line.split(' = ')
        if op == 'mask':
            set_mask = int(value.replace('X', '0'), 2)
            clear_mask = int(value.replace('X', '1'), 2)
        else:
            addr = int(op[4:len(op) - 1])
            value = int(value)
            value |= set_mask
            value &= clear_mask
            mem[addr] = value

    return sum(mem.values())


def floating_mask(lines):
    mem = {}
    clear_mask = 0
    masks = None

    for line in lines:
        op, value = line.split(' = ')
        if op == 'mask':
            m = int(value.replace('X', '0'), 2)
            masks = []
            idx = []
            for i, c in enumerate(value):
                if c == 'X':
                    idx.append(i)

            # A mask to clear all floating bits
            clear_mask = 0
            for i in range(36):
                b = 1
                if i in idx:
                    b = 0
                clear_mask |= b << (35 - i)

            # create all permutations
            perm = itertools.product([0, 1], repeat=len(idx))
            for p in perm:
                mask = m
                for i, b in enumerate(p):
                    mask |= b << (35 - idx[i])
                masks.append(mask)
        else:
            addr = int(op[4:len(op) - 1])
            value = int(value)
            for mask in masks:
                mem[(addr & clear_mask) | mask] = value
    return sum(mem.values())


data = """mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0""".splitlines()

tester.test_value(maskify(data), 165)
tester.test_value(maskify(read_file()), 14925946402938, 'solution to part 1=%s')

data = """mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1""".splitlines()

tester.test_value(floating_mask(data), 208)
tester.test_value(floating_mask(read_file()), 3706820676200, 'solution to part 2=%s')
