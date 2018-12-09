import sys

lines = sys.stdin.readlines()


def rotate(l, n):
    return l[n:] + l[:n]


def count(l, key='#'):
    return sum([1 for x in l if x == key])


grid = [['.'] * 50 for _ in range(6)]

for line in lines:
    if line.startswith('rect'):
        w, h = line[4:].strip().split('x')
        for j in range(int(h)):
            for i in range(int(w)):
                grid[j][i] = '#'

    elif line.startswith('rotate column x='):
        x, step = line[16:].strip().split(' by ')
        column = []
        for row in range(len(grid)):
            column.append(grid[row][int(x)])

        column = rotate(column, -int(step))

        for row in range(len(grid)):
            grid[row][int(x)] = column[row]

    elif line.startswith('rotate row y='):
        y, step = line[13:].strip().split(' by ')
        grid[int(y)] = rotate(grid[int(y)], -int(step))

for row in grid:
    print(''.join(row))

print(sum([count(row) for row in grid]))
