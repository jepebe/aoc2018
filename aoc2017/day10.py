def process(pos, length, skip, lst):
    to = pos + length
    if to >= len(lst):
        f1 = pos
        sub_len = (len(lst) - f1)
        t2 = length - sub_len

        sub = lst[f1:] + lst[0:t2]
        # print(lst, sub)
        sub = list(reversed(sub))
        lst[f1:] = sub[0:sub_len]
        lst[0:t2] = sub[sub_len:]
    else:
        sub = lst[pos:pos + length]
        lst[pos:pos + length] = reversed(sub)
    # print(pos + length + skip, lst)
    return (pos + length + skip) % len(lst), lst


def run(lst, inpt, rounds=1):
    if lst is None:
        lst = list(range(256))

    skip = 0
    pos = 0

    for _ in range(rounds):
        for i in inpt:
            pos, _ = process(pos, i, skip, lst)
            skip += 1

    return lst[0] * lst[1], lst


def asciify(seq):
    return [ord(c) for c in seq] + [17, 31, 73, 47, 23]


def densify(seq):
    result = 0
    for v in seq:
        result ^= v
    return result


def hashify(string):

    ascii = asciify(string)
    _, lst = run(None, ascii, 64)

    hex = []
    for i in range(0, 256, 16):
        hex.append(densify(lst[i:i+16]))
    hsh = ''.join('%02x' % h for h in hex)
    return hsh


if __name__ == '__main__':
    lst = [0, 1, 2, 3, 4]

    assert process(0, 3, 0, lst) == (3, [2, 1, 0, 3, 4])
    assert process(3, 4, 1, lst) == (3, [4, 3, 0, 1, 2])
    assert process(3, 1, 2, lst) == (1, [4, 3, 0, 1, 2])
    assert process(1, 5, 3, lst) == (4, [3, 4, 2, 1, 0])

    lst = [0, 1, 2, 3, 4]
    inpt = [3, 4, 1, 5]

    assert run(lst, inpt) == (12, [3, 4, 2, 1, 0])

    lst = list(range(256))
    inpt = [31, 2, 85, 1, 80, 109, 35, 63, 98, 255, 0, 13, 105, 254, 128, 33]

    print(run(lst, inpt))

    assert asciify('1,2,3') == [49, 44, 50, 44, 51, 17, 31, 73, 47, 23]

    assert densify([65, 27, 9, 1, 4, 3, 40, 50, 91, 7, 6, 0, 2, 5, 68, 22]) == 64

    #print(run(None, asciify('1,2,3'), rounds=64))

    assert hashify('') == 'a2582a3a0e66e6e86e3812dcb672a272'
    assert hashify('AoC 2017') == '33efeb34ea91902bb2f59c9920caa6cd'
    assert hashify('1,2,3') == '3efbe78a8d82f29979031a4aa0b16a9d'
    assert hashify('1,2,4') == '63960835bcdc130f0b66d7ff4f6a5a8e'

    print(hashify('31,2,85,1,80,109,35,63,98,255,0,13,105,254,128,33'))
