from dataclasses import dataclass

import intcode as ic


@dataclass
class SantaPos:
    x = 0
    y = 0

    def tuple(self):
        return self.x, self.y


def visit(ptrn, santas=1):
    grid = {}
    santa_pos = [SantaPos() for _ in range(santas)]

    cur_santa = santa_pos[0]
    grid[cur_santa.tuple()] = 1
    for i, p in enumerate(ptrn):
        cur_santa = santa_pos[i % santas]
        if p == '^':
            cur_santa.y -= 1
        elif p == 'v':
            cur_santa.y += 1
        elif p == '<':
            cur_santa.x -= 1
        elif p == '>':
            cur_santa.x += 1

        if cur_santa.tuple() in grid:
            grid[cur_santa.tuple()] += 1
        else:
            grid[cur_santa.tuple()] = 1

    return len(grid.keys())


tester = ic.Tester('visitation')

tester.test_value(visit(">"), 2)
tester.test_value(visit("^>v<"), 4)
tester.test_value(visit("^v^v^v^v^v"), 2)

tester.test_value(visit("^v", 2), 3)
tester.test_value(visit("^>v<", 2), 3)
tester.test_value(visit("^v^v^v^v^v", 2), 11)

with open("input") as f:
    data = f.read()

houses = visit(data)
tester.test_value(houses, 2565)
print(f'Santa visits {houses} houses')

houses = visit(data, 2)
tester.test_value(houses, 2639)
print(f'Santa and Robo-Santa visits {houses} houses')

tester.summary()
