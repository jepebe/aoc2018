def jump(idx, state):
    state = list(state)
    step = state[idx]
    state[idx] += 1
    return idx + step, tuple(state)


def jumpy(idx, state):
    state = list(state)
    step = state[idx]

    if step >= 3:
        state[idx] -= 1
    else:
        state[idx] += 1
    return idx + step, tuple(state)


def run(state, jmp=jump):
    idx = 0
    count = 0
    while idx < len(state):
        idx, state = jmp(idx, state)
        count += 1
    return count


if __name__ == '__main__':
    assert jump(0, (0, 3, 0, 1, -3)) == (0, (1, 3, 0, 1, -3))
    assert jump(0, (1, 3, 0, 1, -3)) == (1, (2, 3, 0, 1, -3))
    assert jump(1, (2, 3, 0, 1, -3)) == (4, (2, 4, 0, 1, -3))
    assert jump(4, (2, 4, 0, 1, -3)) == (1, (2, 4, 0, 1, -2))
    assert jump(1, (2, 4, 0, 1, -2)) == (5, (2, 5, 0, 1, -2))

    assert run((0, 3, 0, 1, -3)) == 5
    assert run((0, 3, 0, 1, -3), jumpy) == 10

    with open('day5.txt', 'r') as f:
        lines = f.read().split()
        data = [int(v) for v in lines]
        #print(data)

    print(run(tuple(data)))
    print(run(tuple(data), jumpy))
