def state(scanners, step):
    result = {}
    for scanner, length in scanners.items():
        result[scanner] = scanner_state(length, step)
    return result


def scanner_state(scanner_length, step):
    cycles, rest = divmod(step, (scanner_length - 1))
    return scanner_length - rest - 1 if cycles % 2 != 0 else rest


def ride(scanners, delay=0):
    severity = None
    for step, scanner_length in scanners.items():
        current_state = scanner_state(scanner_length, step + delay)

        if current_state == 0:
            if severity is None:
                severity = 0
            severity += scanner_length * step
    return severity


def delayed(scanners):
    delay = 0
    severity = ride(scanners, delay=delay)

    while severity is not None:
        delay += 1
        severity = ride(scanners, delay=delay)

    return delay


if __name__ == '__main__':
    scanners = {
        0: 3,
        1: 2,
        4: 4,
        6: 4
    }

    assert state(scanners, 0) == {0: 0, 1: 0, 4: 0, 6: 0}
    assert state(scanners, 1) == {0: 1, 1: 1, 4: 1, 6: 1}
    assert state(scanners, 2) == {0: 2, 1: 0, 4: 2, 6: 2}
    assert state(scanners, 3) == {0: 1, 1: 1, 4: 3, 6: 3}
    assert state(scanners, 4) == {0: 0, 1: 0, 4: 2, 6: 2}
    assert state(scanners, 5) == {0: 1, 1: 1, 4: 1, 6: 1}
    assert state(scanners, 6) == {0: 2, 1: 0, 4: 0, 6: 0}

    assert ride(scanners) == 24
    assert ride(scanners, delay=10) is None
    assert delayed(scanners) == 10

    with open('day13.txt', 'r') as f:
        lines = f.readlines()
        lines = [line.split(':') for line in lines]

    scanners = {int(line[0]): int(line[1]) for line in lines}

    print(ride(scanners))
    print(delayed(scanners)) #3876272
