import intcode as ic


def test_coords(state_machine, x, y):
    ic.reset_state_machine(state_machine)
    ic.add_input(state_machine, x)
    ic.add_input(state_machine, y)
    ic.run_state_machine(state_machine)
    return ic.get_output(state_machine)


def count_beam(w=50, h=50):
    sm = ic.load_state_machine('input')
    count = 0
    for y in range(h):
        for x in range(w):
            count += test_coords(sm, x, y)
    return count


def find_position_of_square(y_hint=1700):
    sm = ic.load_state_machine('input')
    grid = {}
    first_x = 0
    y = y_hint
    while True:
        found_x = False
        x = first_x - 1
        while True:
            val = test_coords(sm, x, y)

            if not found_x and val == 1:
                found_x = True
                first_x = x

            if found_x and val == 0:
                grid[y] = (first_x, x - 1)
                break

            x += 1

        y0 = y - 99
        if y0 in grid:
            x1 = grid[y][0]
            x2 = grid[y0][1]
            if x2 - x1 == 99:
                return x1, y0, x1 * 10000 + y0
        y += 1


tester = ic.Tester('tractor')

tester.test_value(count_beam(), 114, 'Solution to part 1 %s')
tester.test_value(find_position_of_square()[2], 10671712, 'Solution to part 2 %s')

tester.summary()
