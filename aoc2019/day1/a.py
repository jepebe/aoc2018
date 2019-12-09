import sys
from math import floor

lines = sys.stdin.readlines()


def fuel_req(mass):
    return floor(mass / 3) - 2


assert(fuel_req(12) == 2)
assert(fuel_req(14) == 2)
assert(fuel_req(1969) == 654)
assert(fuel_req(100756) == 33583)

lines = map(int, lines)
print(sum(map(fuel_req, lines)))