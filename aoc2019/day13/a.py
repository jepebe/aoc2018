import intcode as ic


def run_game(sm, grid, ball_pos=None, paddle_pos=None):
    ic.run_state_machine(sm)
    score = 0
    while ic.has_output(sm):
        x = ic.get_output(sm)
        y = ic.get_output(sm)
        tid = ic.get_output(sm)

        if x == -1:
            score = tid
            continue

        grid[(x, y)] = tid
        if tid == 4:
            ball_pos = (x, y)
        if tid == 3:
            paddle_pos = (x, y)

    blocks = len([t for t in grid.values() if t == 2])
    return grid, blocks, ball_pos, paddle_pos, score


sm = ic.load_state_machine('input')
grid, blocks, *_ = run_game(sm, {})
look_up = {
    0: ' ',
    1: ic.color('\u2588', 250),  # wall
    2: ic.color('\u2592', 105),  # blocks
    3: ic.color('\u2594', 214),  # paddle
    4: ic.color('\u25CF', 118)  # ball
}
ic.print_map(grid, look_up)
print(f'blockcount {blocks} == 226')  # 226


def play_game(sm):
    sm['instructions'][0] = 2
    grid = {}
    score = 0
    ball = None
    paddle = None
    while ic.is_running(sm):
        grid, blocks, ball, paddle, score = run_game(sm, grid, ball, paddle)

        if ball[0] < paddle[0]:
            ic.add_input(sm, -1)
        elif ball[0] > paddle[0]:
            ic.add_input(sm, 1)
        else:
            ic.add_input(sm, 0)

    return grid, score


sm = ic.load_state_machine('input')
grid, score = play_game(sm)

print(f'score {score} == 10800')  # 10800
print(f'instruction count {sm["instruction_count"]}')
