import intcode as ic


def run_game(sm):
    ic.run_state_machine(sm)

    grid = {}
    ball_pos = None
    paddle_pos = None
    score = 0
    for i in range(len(sm['output']) // 3):
        x = sm['output'][i * 3]
        y = sm['output'][i * 3 + 1]
        tid = sm['output'][i * 3 + 2]

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
grid, blocks, *_ = run_game(sm)

ic.print_map(grid, {0: '.', 1: '#', 2: '=', 3: '-', 4: '@'})
print(f'blockcount {blocks} == 226')  # 226


def play_game(sm):
    sm['instructions'][0] = 2
    while ic.is_running(sm):
        grid, blocks, ball, paddle, score = run_game(sm)

        if ball[0] < paddle[0]:
            ic.add_input(sm, -1)
        elif ball[0] > paddle[0]:
            ic.add_input(sm, 1)
        else:
            ic.add_input(sm, 0)

    return grid, score


sm = ic.load_state_machine('input')
grid, score = play_game(sm)
ic.print_map(grid, {0: '.', 1: '#', 2: '=', 3: '-', 4: '@'})
print(f'score {score} == 10800')  # 10800
print(f'instruction count {sm["instruction_count"]}')
