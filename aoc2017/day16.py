def spin(sz, p):
    l = len(p)
    r = list(p[l - sz:])
    r.extend(p[:l - sz])
    return r


def exchange(a, b, p):
    temp = p[a]
    p[a] = p[b]
    p[b] = temp
    return p


def partner(a, b, p):
    a = p.index(a)
    b = p.index(b)
    return exchange(a, b, p)


def dance(d, p):
    d = d.split(',')

    for m in d:
        if m.startswith('s'):
            p = spin(int(m[1:]), p)
        elif m.startswith('x'):
            a, b = m[1:].split('/')
            p = exchange(int(a), int(b), p)
        elif m.startswith('p'):
            a, b = m[1:].split('/')
            p = partner(a, b, p)

    return p


def dance_gen(data, p):
    first = ''.join(p)
    yield first

    while True:
            p = dance(data, p)
            joined = ''.join(p)

            if first == joined:
                break

            yield joined


if __name__ == '__main__':
    d = 's1,x3/4,pe/b'

    assert spin(1, list('abcde')) == list('eabcd')
    assert spin(3, list('abcde')) == list('cdeab')
    assert exchange(3, 4, list('eabcd')) == list('eabdc')
    assert partner('e', 'b', list('eabdc')) == list('baedc')

    assert dance(d, list('abcde')) == list('baedc')

    with open('day16.txt', 'r') as f:
        data = f.read()

    danced = dance(data, list('abcdefghijklmnop'))
    print(''.join(danced))

    cycle = [n for n in dance_gen(data, list('abcdefghijklmnop'))]

    print(len(cycle), cycle)

    rest = 100000000 % len(cycle)

    print(cycle[rest])
