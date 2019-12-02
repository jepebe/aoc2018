def power(serial, x, y):
    rack_id = x + 10
    power_level = rack_id * y
    power_level += serial
    power_level *= rack_id

    if power_level < 99:
        power_level = 0

    power_level = int(str(power_level)[-3])
    power_level -= 5
    return power_level


def power_grid(serial):
    grid = [[0] * 301 for n in range(301)]
    for y in range(1, 301):
        for x in range(1, 301):
            power_level = power(serial, x, y)
            grid[y][x] = power_level
    return grid


def find_max_power(grid, size, memo=None):
    max_sum = 0
    X, Y = None, None
    if memo is None:
        memo = {}
    for y in range(1, 301 - (size - 1)):
        for x in range(1, 301 - (size - 1)):
            if (x, y, size - 1) in memo:
                memo_sum = memo[(x, y, size - 1)]
                row_sum = sum(grid[y + size - 1][x:x + size - 1])
                col_sum = sum(grid[y + n][x + size - 1] for n in range(size))
                del memo[(x, y, size - 1)]
                power_sum = memo_sum + row_sum + col_sum

            else:
                power_sum = sum([sum(grid[y + n][x:x + size]) for n in range(size)])

            memo[(x, y, size)] = power_sum

            if power_sum > max_sum:
                max_sum = power_sum
                X = x
                Y = y

    return max_sum, X, Y, memo


grid_18 = power_grid(serial=18)
grid_42 = power_grid(serial=42)
grid_4172 = power_grid(serial=4172)

print(find_max_power(grid_18, 3)[0:3], (29, 33, 45))
print(find_max_power(grid_42, 3)[0:3], (30, 21, 61))
print(find_max_power(grid_4172, 3)[0:3], (29, 243, 43))

print(find_max_power(grid_18, 16)[0:3], (113, 90, 269))
print(find_max_power(grid_42, 12)[0:3], (119, 232, 251))


def find_total_max_power(grid):
    max_p = 0
    memo = {}
    X, Y, SIZE = None, None, None
    for size in range(1, 301):
        print(size)
        power, x, y, memo = find_max_power(grid, size, memo)
        if power > max_p:
            max_p = power
            SIZE = size
            X = x
            Y = y
    return max_p, X, Y, SIZE


#print(find_total_max_power(grid_18), (90,269,16))
#print(find_total_max_power(grid_42), (232,251,12))
print(find_total_max_power(grid_4172))
