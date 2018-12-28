def get_value(reg, v1):
    if v1 in reg:
        v1 = reg[v1]
    return int(v1)


def init_reg(reg, r1):
    if r1 not in reg:
        reg[r1] = 0


def snd(reg, r1):
    if r1 not in reg:
        reg[r1] = 0

    #print('snd %s=%s > 0 -> %s' % (r1, reg[r1], reg[r1]))
    if reg[r1] > 0:
        reg['last'] = reg[r1]
        return reg['last']
    return None


def sets(reg, r1, v1):
    v1 = get_value(reg, v1)
    #print('set %s = %s' % (r1, v1))
    reg[r1] = v1
    return reg[r1]


def adds(reg, r1, v1):
    v1 = get_value(reg, v1)
    init_reg(reg, r1)

    #print('add %s=%s + %s -> %s' % (r1, reg[r1], v1, reg[r1] + v1))
    reg[r1] += v1

    return reg[r1]


def muls(reg, r1, v1):
    v1 = get_value(reg, v1)
    init_reg(reg, r1)

    #print('mul %s=%s * %s -> %s' % (r1, reg[r1], v1, reg[r1] * v1))
    reg[r1] *= v1

    return reg[r1]


def mods(reg, r1, v1):
    v1 = get_value(reg, v1)
    init_reg(reg, r1)

    #print('mod %s=%s %% %s -> %s' % (r1, reg[r1], v1, reg[r1] % v1))
    reg[r1] %= v1

    return reg[r1]


def rcv(reg, r1):
    init_reg(reg, r1)

    f = reg[r1]
    #print('rcv %s=%s != 0 -> %s' % (r1, f, reg['last']))
    if f != 0:
        return reg['last']

    return None


def jgz(reg, r1, v1):
    v1 = get_value(reg, v1)

    try:
        j = int(r1)
    except:
        init_reg(reg, r1)
        j = reg[r1]

    #print('jgz %s=%d > 0 %s' % (r1, j, v1))
    if j > 0:
        return v1

    return None


OPS = {
    'snd': snd,
    'set': sets,
    'add': adds,
    'mul': muls,
    'mod': mods,
    'rcv': rcv,
    'jgz': jgz
}


def play(lines):
    reg = {
        'last': 0,
        'instructions': [i.split() for i in lines],
        'pointer': 0
    }

    while reg['pointer'] < len(reg['instructions']):

        instruction = reg['instructions'][reg['pointer']]
        op = OPS[instruction[0]]
        result = op(reg, *instruction[1:])

        if op == jgz and result is not None:
            reg['pointer'] += result
        elif op == rcv and result is not None:
            break
        else:
            reg['pointer'] += 1

    return reg['last']


def program_valid(reg):
    return reg['pointer'] < len(reg['instructions'])


def snd_duet(reg0, reg1, v1):
    v1 = get_value(reg0, v1)
    reg1['msg_queue'].append(v1)
    reg0['snd_count'] += 1


def rcv_duet(reg, r1):
    if reg['msg_queue']:
        sets(reg, r1, reg['msg_queue'].pop(0))
        reg['rcv_count'] += 1
        return True
    else:
        return False


def play_duet(lines):
    reg0 = {
        'p': 0,
        'instructions': [i.split() for i in lines],
        'pointer': 0,
        'snd_count': 0,
        'rcv_count': 0,
        'msg_queue': [],
        'waiting': False
    }

    reg1 = {
        'p': 1,
        'instructions': [i.split() for i in lines],
        'pointer': 0,
        'snd_count': 0,
        'rcv_count': 0,
        'msg_queue': [],
        'waiting': False
    }

    current = reg0
    other = reg1
    wait_count = 0
    while program_valid(reg0) and program_valid(reg1):
        instruction = current['instructions'][current['pointer']]
        op = OPS[instruction[0]]
        current['waiting'] = False

        if op == snd:
            snd_duet(current, other, *instruction[1:])
            current['pointer'] += 1
        elif op == rcv:
            state = rcv_duet(current, *instruction[1:])
            if not state:
                current['waiting'] = True
                current, other = other, current
            else:
                wait_count = 0
                current['pointer'] += 1
        else:
            result = op(current, *instruction[1:])

            if op == jgz and result is not None:
                current['pointer'] += result
            else:
                current['pointer'] += 1

        if reg0['waiting'] and reg1['waiting']:
            wait_count += 1

            if wait_count > 10:
                print('Deadlock')
                break


    # print(reg0['instructions'][reg0['pointer']])
    # print(reg1['instructions'][reg1['pointer']])
    # print(reg0)
    # print(reg1)
    # print(reg0['snd_count'])
    # print(reg1['snd_count'])

    return reg0['snd_count'], reg1['snd_count']




if __name__ == '__main__':
    reg = {
        'x': 5,
        'last': -1
    }

    assert snd(reg, 'a') is None
    assert snd(reg, 'x') == reg['x']
    assert sets(reg, 'a', 2) == reg['a']
    assert sets(reg, 'a', '2') == reg['a']
    assert sets(reg, 'b', 'a') == reg['a']
    assert adds(reg, 'a', 3) == 5
    assert adds(reg, 'c', 'b') == 2
    assert muls(reg, 'c', 2) == 4
    assert muls(reg, 'c', 'b') == 8
    assert muls(reg, 'd', 3) == 0
    assert mods(reg, 'c', 3) == 2
    assert mods(reg, 'a', 'c') == 1
    assert rcv(reg, 'a') == reg['last']
    assert rcv(reg, 'd') is None
    assert jgz(reg, 'a', -2) == -2
    assert jgz(reg, 'd', -2) is None

    with open('day18_test.txt', 'r') as f:
        lines = f.readlines()

    assert play(lines) == 4
    print(play_duet(lines))

    lines = ['snd 1', 'snd 2', 'snd p', 'rcv a', 'rcv b', 'rcv c', 'rcv d']

    assert play_duet(lines) == (3, 3)

    with open('day18.txt', 'r') as f:
        lines = f.readlines()

    print(play(lines))
    print(play_duet(lines))
