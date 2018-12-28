def stepinator(state, pos, count, skip=3):
    ins = skip % len(state)
    ins += pos

    if ins >= len(state):
        ins -= len(state)

    ins += 1
    state.insert(ins, count)

    return ins, state


def full_stepinator(n=2017, step=3):
    state = [0]
    pos = 0
    for i in range(1, n):
        pos, state = stepinator(state, pos, i, skip=step)

    #print(state[pos], state[pos + 1])
    #print(pos, state)
    print(state[:5])
    return state[pos + 1]


def strange_stepinator(n, skip):
    l = 1
    pos = 0
    value = -1

    for i in range(1, n):
        ins = skip % l
        ins += pos

        if ins >= l:
            ins -= l

        pos = ins + 1

        if pos == 1:
            value = i

        l += 1
    print(pos, value)
    return value


if __name__ == '__main__':
    state = [0]
    assert stepinator(state, 0, 1) == (1, [0, 1])
    assert stepinator(state, 1, 2) == (1, [0, 2, 1])
    assert stepinator(state, 1, 3) == (2, [0, 2, 3, 1])
    assert stepinator(state, 2, 4) == (2, [0, 2, 4, 3, 1])
    assert stepinator(state, 2, 5) == (1, [0, 5, 2, 4, 3, 1])

    assert full_stepinator(n=2018, step=3) == 638

    assert strange_stepinator(n=2018, skip=3) == 1226
    assert strange_stepinator(n=2018, skip=343) == 1447

    print(full_stepinator(n=2018, step=343))
    print(strange_stepinator(n=50000000, skip=343))
