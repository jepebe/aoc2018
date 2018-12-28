def cyclic_indexer(start, count, max):
    n = 0
    idx = start
    if idx >= max:
        idx = 0

    while n < count:
        yield idx
        idx += 1
        if idx >= max:
            idx = 0
        n += 1


def distribute(conf):
    m = max(conf)
    idx = conf.index(m)

    conf = list(conf)
    conf[idx] = 0

    for i in cyclic_indexer(idx + 1, m, len(conf)):
        conf[i] += 1

    return tuple(conf)


def cycles(conf):
    confs = set()
    confs.add(conf)
    count = 0
    while True:
        conf = distribute(conf)
        if conf in confs:
            print(conf)
            break
        confs.add(conf)
        count += 1


    return len(confs)


if __name__ == '__main__':
    assert distribute((0, 2, 7, 0)) == (2, 4, 1, 2)
    assert distribute((2, 4, 1, 2)) == (3, 1, 2, 3)
    assert distribute((3, 1, 2, 3)) == (0, 2, 3, 4)
    assert distribute((0, 2, 3, 4)) == (1, 3, 4, 1)
    assert distribute((1, 3, 4, 1)) == (2, 4, 1, 2)

    assert cycles((0, 2, 7, 0)) == 5
    assert cycles((2, 4, 1, 2)) == 4

    print(cycles((4, 1, 15, 12, 0, 9, 9, 5, 5, 8, 7, 3, 14, 5, 12, 3)))
    print(cycles((0, 14, 13, 12, 11, 10, 8, 8, 6, 6, 5, 3, 3, 2, 1, 10)))