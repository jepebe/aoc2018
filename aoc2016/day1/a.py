import sys

line = sys.stdin.readline()

# DIR = ['N', 'E', 'S', 'W']
DIR = [(0, 1), (1, 0), (0, -1), (-1, 0)]


moves = line.split(', ')


dir = 0
pos = (0, 0)

for move in moves:
    turn = move[0]
    step = int(move[1:])

    if turn == 'R':
        dir += 1
    else:
        dir -= 1

    if dir == 4:
        dir = 0
    elif dir == -1:
        dir = 3

    pos = pos[0] + DIR[dir][0] * step, pos[1] + DIR[dir][1] * step

    blocks = abs(pos[0]) + abs(pos[1])
    print(move, dir, pos, blocks)


print(pos, blocks)


