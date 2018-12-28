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
        hex.append(densify(lst[i:i + 16]))
    hsh = ''.join('%02x' % h for h in hex)
    return hsh


def defrag_hash(key):
    h = hashify(key)
    b = bin(int(h, 16))[2:].zfill(128)
    # print(b)
    return b


def build_grid(key):
    grid = []
    for i in range(128):
        dh = defrag_hash(key % i)
        grid.append(str(dh))
    return ''.join(grid)


def count_blocks(key):
    blocks = 0
    for i in range(128):
        dh = defrag_hash(key % i)
        blocks += str(dh).count('1')
    return blocks


def bfs(grid, i):
    if i < 0 or i >= len(grid):
        return

    if grid[i] != '1':
        return

    grid[i] = '#'

    if i % 128 != 0:
        bfs(grid, i - 1)

    if (i + 1) % 128 != 0:
        bfs(grid, i + 1)

    bfs(grid, i - 128)
    bfs(grid, i + 128)


def count_regions(key):
    grid = [c for c in build_grid(key)]

    region_count = 0
    for i, c in enumerate(grid):
        if c == '1':
            bfs(grid, i)
            region_count += 1
    #print(region_count, grid)
    return region_count


if __name__ == '__main__':
    key = 'flqrgnkx-%d'

    assert str(defrag_hash(key % 0))[0:8] == '11010100'
    assert str(defrag_hash(key % 1))[0:8] == '01010101'
    assert str(defrag_hash(key % 2))[0:8] == '00001010'

    assert count_blocks(key) == 8108
    assert count_regions(key) == 1242

    key = 'hfdlxzhv-%d'
    print(count_blocks(key))
    print(count_regions(key))
