import sys
from math import floor

lines = sys.stdin.readlines()


def fuel_req(mass):
    fr = floor(mass / 3) - 2
    if fr < 0:
        fr = 0
    else:
        fr += fuel_req(fr)
    return fr


assert(fuel_req(12) == 2)
assert(fuel_req(14) == 2)
assert(fuel_req(1969) == 966)
assert(fuel_req(100756) == 50346)

lines = map(int, lines)
print(sum(map(fuel_req, lines)))
