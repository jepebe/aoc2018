from advent import timeit


def generate(a, b):
    a = (a * 16807) % 2147483647
    b = (b * 48271) % 2147483647
    return a, b


def agen(a, n):
    i = 0
    while i < n:
        a = (a * 16807) % 2147483647

        if ((a >> 2) << 2) != a:
            continue

        yield a
        i += 1


def bgen(b, n):
    i = 0
    while i < n:
        b = (b * 48271) % 2147483647

        if ((b >> 3) << 3) != b:
            continue

        yield b
        i += 1


def diverator(a, b):
    a = (a * 16807) % 2147483647
    while ((a >> 2) << 2) != a:
        a = (a * 16807) % 2147483647

    b = (b * 48271) % 2147483647

    while ((b >> 3) << 3) != b:
        b = (b * 48271) % 2147483647

    return a, b


def low_match(a, b):
    return (a & 65535) == (b & 65535)


@timeit
def count_matches(a, b, n=40000000, f=generate):
    match = 0
    for i in range(n):
        a, b = f(a, b)
        if low_match(a, b):
            match += 1
    return match


@timeit
def gen_count_matches(a, b, n=40000000):
    match = [(a, b) for a, b in zip(agen(a, n), bgen(b, n)) if low_match(a, b)]

    print(len(match))
    return len(match)


if __name__ == '__main__':
    assert generate(a=65, b=8921) == (1092455, 430625591)
    assert generate(1092455, 430625591) == (1181022009, 1233683848)
    assert not low_match(1181022009, 1233683848)
    assert generate(1181022009, 1233683848) == (245556042, 1431495498)
    assert low_match(245556042, 1431495498)

    # assert count_matches(65, 8921) == 588

    # print(count_matches(591, 393))

    assert diverator(a=65, b=8921) == (1352636452, 1233683848)
    # assert count_matches(65, 8921, n=5000000, f=diverator) == 309
    assert gen_count_matches(65, 8921, n=5000000) == 309

    print(count_matches(591, 393, n=5000000, f=diverator))
    print(gen_count_matches(591, 393, n=5000000))
