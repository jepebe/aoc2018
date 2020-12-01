import intcode as ic
import re


def count_lights(grid: dict):
    return sum(light for light in grid.values() if light == 1)


def turn_on(grid, start, stop):
    for y in range(start[1], stop[1] + 1):
        for x in range(start[0], stop[0] + 1):
            grid[(x, y)] = 1


def turn_off(grid, start, stop):
    for y in range(start[1], stop[1] + 1):
        for x in range(start[0], stop[0] + 1):
            grid[(x, y)] = 0


def toggle(grid, start, stop):
    for y in range(start[1], stop[1] + 1):
        for x in range(start[0], stop[0] + 1):
            if (x, y) not in grid:
                grid[(x, y)] = 0
            grid[(x, y)] = 0 if grid[(x, y)] == 1 else 1


tester = ic.Tester("lights")

tester.test_value(count_lights({}), 0)
tester.test_value(count_lights({1: 0, 2: 1, 3: 1}), 2)

test_grid = {}
turn_on(test_grid, (0, 0), (9, 9))

tester.test_value(count_lights(test_grid), 100)

turn_off(test_grid, (0, 0), (4, 4))
tester.test_value(count_lights(test_grid), 75)

toggle(test_grid, (0, 0), (9, 4))
tester.test_value(count_lights(test_grid), 75)

toggle(test_grid, (5, 0), (9, 4))
tester.test_value(count_lights(test_grid), 100)

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

tester.test_value(count_lights(grid), 569999)