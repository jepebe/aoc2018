import intcode as ic


# north (1), south (2), west (3), and east (4)
# 0: The repair droid hit a wall. Its position has not changed.
# 1: The repair droid has moved one step in the requested direction.
# 2: The repair droid has moved one step in the requested direction;
#    its new position is the location of the oxygen system


def make_grid(sm, grid, start=(0, 0)):
    dirs = {(0, -1): 1, (0, 1): 2, (-1, 0): 3, (1, 0): 4}
    backtrack = {1: 2, 2: 1, 3: 4, 4: 3}
    x, y = start
    oxygen = None
    for d in ((0, -1), (-1, 0), (1, 0), (0, 1)):
        if (x + d[0], y + d[1]) not in grid:
            ic.add_input(sm, dirs[d])
            ic.run_state_machine(sm)
            status = ic.get_output(sm)
            grid[(x + d[0], y + d[1])] = status

            if status in (1, 2):
                if status == 2:
                    oxygen = (x + d[0], y + d[1])

                oxygen = make_grid(sm, grid, (x + d[0], y + d[1])) or oxygen
                ic.add_input(sm, backtrack[dirs[d]])
                ic.run_state_machine(sm)
                ic.get_output(sm)

    return oxygen


tester = ic.Tester('oxygen')
sm = ic.load_state_machine('input')
grid = {(0, 0): 3}

oxygen = make_grid(sm, grid)
ic.print_map(grid, look_up={0: '#', 1: ' ', 2: 'O', 3: 'D'})
tester.test_value(oxygen, (12, 14))

dist = ic.bfs(grid, (0, 0), walkable=[1, 2])
tester.test_value(dist[oxygen], 230, 'Solution for part 1 is %s')

dist = ic.bfs(grid, oxygen, walkable=[1, 2])
tester.test_value(max(dist.values()), 288, 'Solution for part 2 is %s')

tester.summary()
