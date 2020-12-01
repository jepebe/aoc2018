import intcode as ic
import re


def brightness(grid: dict):
    return sum(light for light in grid.values())


def turn_on(grid, start, stop):
    for y in range(start[1], stop[1] + 1):
        for x in range(start[0], stop[0] + 1):
            if (x, y) not in grid:
                grid[(x, y)] = 0
            grid[(x, y)] += 1


def turn_off(grid, start, stop):
    for y in range(start[1], stop[1] + 1):
        for x in range(start[0], stop[0] + 1):
            if (x, y) not in grid:
                grid[(x, y)] = 0
            if grid[(x, y)] > 0:
                grid[(x, y)] -= 1


def toggle(grid, start, stop):
    for y in range(start[1], stop[1] + 1):
        for x in range(start[0], stop[0] + 1):
            if (x, y) not in grid:
                grid[(x, y)] = 0
            grid[(x, y)] += 2


tester = ic.Tester("lights")

test_grid = {}

turn_on(test_grid, (0, 0), (0, 0))
tester.test_value(brightness(test_grid), 1)

test_grid = {}

toggle(test_grid, (0, 0), (999, 999))
tester.test_value(brightness(test_grid), 2000000)

with open("input") as f:
    lines = f.readlines()

functions = {
    'turn off': turn_off,
    'toggle': toggle,
    'turn on': turn_on,
}
grid = {}
for line in lines:
    m = re.search("(\D+) (\d+),(\d+)\D+(\d+),(\d+)", line)
    command = m.group(1)
    start = int(m.group(2)), int(m.group(3))
    stop = int(m.group(4)), int(m.group(5))
    functions[command](grid, start, stop)

tester.test_value(brightness(grid), 17836115)