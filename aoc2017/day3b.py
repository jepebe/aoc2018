def spiral_sum(spiro):
    memo = {}

    for x, y in spiro:
        if x == 0 and y == 0:
            s = 1
        else:
            s = 0

            if (x + 1, y) in memo:
                s += memo[(x + 1, y)]
            if (x + 1, y + 1) in memo:
                s += memo[(x + 1, y + 1)]
            if (x, y + 1) in memo:
                s += memo[(x, y + 1)]
            if (x - 1, y + 1) in memo:
                s += memo[(x - 1, y + 1)]
            if (x - 1, y) in memo:
                s += memo[(x - 1, y)]
            if (x - 1, y - 1) in memo:
                s += memo[(x - 1, y - 1)]
            if (x, y - 1) in memo:
                s += memo[(x, y - 1)]
            if (x + 1, y - 1) in memo:
                s += memo[(x + 1, y - 1)]

        memo[(x, y)] = s

    print(sorted(memo.values()))
    #print(memo)
    return s


def spiral(N):
    x = y = 0
    dx = 0
    dy = -1
    for i in range(N ** 2):
        if (-N / 2 < x <= N / 2) and (-N / 2 < y <= N / 2):
            yield (x, y)
        if x == y or (x < 0 and x == -y) or (x > 0 and x == 1 - y):
            dx, dy = -dy, dx
        x, y = x + dx, y + dy


if __name__ == '__main__':
    assert list(spiral(3)) == [
        (0, 0), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1),
        (1, -1)]

    assert spiral_sum(spiral(3)) == 25
    assert spiral_sum(spiral(5)) == 931

    #361527

    #print(spiral_sum(spiral(7)))
    print(spiral_sum(spiral(9)))
    #print(spiral_sum(spiral(11)))
