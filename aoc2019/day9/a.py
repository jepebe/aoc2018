from intcode import load_state_machine, run_state_machine, add_input


sm = load_state_machine('input')
sm['output_enabled'] = True
add_input(sm, 1)
run_state_machine(sm)
assert sm['output'] == [2494485073]

sm = load_state_machine('input')
sm['output_enabled'] = True
add_input(sm, 2)
run_state_machine(sm)
assert sm['output'] == [44997]
