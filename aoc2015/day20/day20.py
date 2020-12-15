import intcode as ic
from functools import reduce

tester = ic.Tester('Infinite Elves and Infinite Houses')


def factors(n):
    return set(reduce(list.__add__,
                      ([i, n // i] for i in range(1, int(n ** 0.5) + 1) if n % i == 0)))


def present_count(n):
    return sum(10 * f for f in factors(n))


def present_count_50(n):
    return sum(11 * f for f in factors(n) if n // f < 50)


def find_presents(num=34000000):
    c = present_count(1)
    i = 1
    while c < num:
        i += 1
        c = present_count(i)
        # print(i, c)
    return i


def find_presents_50(num=34000000):
    c = present_count_50(1)
    i = 1
    while c < num:
        i += 1
        c = present_count_50(i)
        # print(i, c)
    return i


tester.test_value(find_presents(70), 4)
tester.test_value(find_presents(120), 6)
tester.test_value(find_presents(150), 8)

tester.test_value(find_presents(), 786240, 'solution to part 1=%s')
tester.test_value(find_presents_50(), 831600, 'solution to part 2=%s')
