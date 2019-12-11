from collections import deque

import intcode as ic

dirs = deque([(0, -1), (1, 0), (0, 1), (-1, 0)])
pm = ic.load_state_machine('input')
grid = {(0, 0): 1}  # 0 for part 1, 1 for part 2
pos = (0, 0)

while ic.is_running(pm):
    ic.add_input(pm, grid.get(pos, 0))
    ic.run_state_machine(pm)

    color = ic.get_output(pm)
    grid[pos] = color

    turn = ic.get_output(pm)
    dirs.rotate(1 if turn == 0 else -1)
    d = dirs[0]
    pos = pos[0] + d[0], pos[1] + d[1]


# part1: right = 2319

print(len(grid))


ic.print_map(grid, {0: ' ', 1: '#'}, missing=' ')
# ic.print_map(grid, func=lambda g, p: ' ' if g[p] == 0 else '*')
