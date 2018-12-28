import math


def ring_center(start, width, ring):
    start = start + ring
    width = width - 1
    return start, start + width, start + width * 2, start + width * 3


def dist(n):
    if n == 1:
        return 0

    ring = 0
    width = 1
    while math.pow(width, 2) < n:
        ring += 1
        width += 2

    rc = ring_center(math.pow(width - 2, 2), width, ring)
    min_dist = min([abs(x - n) for x in rc])

    return ring + min_dist


if __name__ == '__main__':
    assert ring_center(2, 3, 0) == (2, 4, 6, 8)
    assert ring_center(10, 5, 1) == (11, 15, 19, 23)
    assert ring_center(26, 7, 2) == (28, 34, 40, 46)

    assert dist(1) == 0
    assert dist(2) == 1
    assert dist(11) == 2
    assert dist(28) == 3

    assert dist(9) == 2
    assert dist(12) == 3
    assert dist(13) == 4
    assert dist(23) == 2
    assert dist(1024) == 31
    print(dist(361527))
