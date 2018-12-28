PREDICATOR = {
    '==': lambda a, b: a == b,
    '!=': lambda a, b: a != b,
    '>=': lambda a, b: a >= b,
    '<=': lambda a, b: a <= b,
    '<': lambda a, b: a < b,
    '>': lambda a, b: a > b,
}


def process(reg, line):
    r1, op, v1, _, r3, pred, v2 = line.split()

    v1 = int(v1)
    v2 = int(v2)

    if r1 not in reg:
        reg[r1] = 0

    if r3 not in reg:
        reg[r3] = 0

    pred = PREDICATOR[pred]

    if pred(reg[r3], v2):
        if op == 'inc':
            reg[r1] += v1
        elif op == 'dec':
            reg[r1] -= v1
        else:
            print('Syntax error')

    return reg


def run(lines):
    reg = {}
    memory_max = 0
    for line in lines:
        process(reg, line)
        memory_max = max(memory_max, max(reg.values()))

    print(reg)
    return max(reg.values()), memory_max


if __name__ == '__main__':
    reg = {}
    assert process(reg, 'b inc 5 if a > 1') == {'a': 0, 'b': 0}
    assert process(reg, 'a inc 1 if b < 5') == {'a': 1, 'b': 0}
    assert process(reg, 'c dec -10 if a >= 1') == {'a': 1, 'b': 0, 'c': 10}
    assert process(reg, 'c inc -20 if c == 10') == {'a': 1, 'b': 0, 'c': -10}

    assert max(reg.values()) == 1

    with open('day8_test.txt', 'r') as f:
        lines = f.read().splitlines()

    assert run(lines) == (1, 10)

    with open('day8.txt', 'r') as f:
        lines = f.read().splitlines()

    print(run(lines))
