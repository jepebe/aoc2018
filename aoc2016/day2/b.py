import sys

lines = sys.stdin.readlines()

DIR = {'U': (0, -1),
       'R': (1, 0),
       'D': (0, 1),
       'L': (-1, 0)}

keypad = [['.', '.', '.', '.', '.', '.', '.'],
          ['.', '.', '.', '1', '.', '.', '.'],
          ['.', '.', '2', '3', '4', '.', '.'],
          ['.', '5', '6', '7', '8', '9', '.'],
          ['.', '.', 'A', 'B', 'C', '.', '.'],
          ['.', '.', '.', 'D', '.', '.', '.'],
          ['.', '.', '.', '.', '.', '.', '.']
          ]

pos = (1, 3)
for line in lines:
    for c in line.strip():
        step = DIR[c]

        x = pos[0] + step[0]
        y = pos[1] + step[1]

        # print(x, y, keypad[y][x])

        if keypad[y][x] == '.':
            pass
        else:
            pos = x, y

    print(keypad[pos[1]][pos[0]])
