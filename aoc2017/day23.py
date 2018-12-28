def get_value(reg, v1):
    if v1 in reg:
        v1 = reg[v1]
    return int(v1)


def prn(reg):
    b = reg['b']
    c = reg['c']
    d = reg['d']
    e = reg['e']
    f = reg['f']
    g = reg['g']
    h = reg['h']
    print('b: %s c: %s d: %s e: %s f: %s g: %s h: %s' % (b, c, d, e, f, g, h))


def mul(reg, r1, v1):
    v1 = get_value(reg, v1)

    # print('mul %s=%s x %s' % (r1, reg[r1], v1))
    reg[r1] *= v1
    reg['mul_count'] += 1

    return reg[r1]


def sets(reg, r1, v1):
    if r1 == 'f':
        prn(reg)
    v1 = get_value(reg, v1)
    # print('set %s=%s = %s' % (r1, reg[r1], v1))
    reg[r1] = v1
    return reg[r1]


def sub(reg, r1, v1):
    v1 = get_value(reg, v1)
    # print('sub %s=%s - %s' % (r1, reg[r1], v1))
    reg[r1] -= v1
    return reg[r1]


def jnz(reg, r1, v1):
    v1 = get_value(reg, v1)

    try:
        j = int(r1)
    except:
        j = reg[r1]

    if j != 0:
        # print('jnz if %s=%s != 0 -> %s' % (r1, j, v1))
        return v1

    return None


def is_prime(n):
    if n == 2 or n == 3: return True
    if n < 2 or n % 2 == 0: return False
    if n < 9: return True
    if n % 3 == 0: return False
    r = int(n ** 0.5)
    f = 5
    while f <= r:
        if n % f == 0: return False
        if n % (f + 2) == 0: return False
        f += 6
    return True


def prime(reg, r1, v1):
    v1 = get_value(reg, v1)

    if is_prime(v1):
        reg[r1] = 1
    else:
        reg[r1] = 0


OPS = {
    'set': sets,
    'sub': sub,
    'mul': mul,
    'jnz': jnz,
    'prm': prime
}


def play(lines, a=0):
    reg = {
        'a': a,
        'b': 0,
        'c': 0,
        'd': 0,
        'e': 0,
        'f': 0,
        'g': 0,
        'h': 0,
        'instructions': [i.split() for i in lines],
        'pointer': 0,
        'mul_count': 0,
        'instruction_count': 0
    }

    while reg['pointer'] < len(reg['instructions']):

        instruction = reg['instructions'][reg['pointer']]

        if not instruction[0].startswith('#'):
            op = OPS[instruction[0]]
            result = op(reg, *instruction[1:])
        else:
            result = None

        if op == jnz and result is not None:
            reg['pointer'] += result
        else:
            reg['pointer'] += 1

        if reg['instruction_count'] % 10000 == 0:
            prn(reg)
        # print('e %s, g %s, d %s (%s, %s, %s)' % (reg['e'], reg['g'], reg['d'], reg['b'], reg['c'], reg['h']))
        reg['instruction_count'] += 1

    return reg['mul_count'], reg['h']


if __name__ == '__main__':
    with open('day23.txt', 'r') as f:
        lines = f.readlines()

    # print(play(lines))
    print(play(lines, a=1))
