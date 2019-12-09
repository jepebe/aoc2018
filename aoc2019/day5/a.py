from intcode import load_state_machine, run_state_machine, add_input

sm = load_state_machine('test')
add_input(sm, 1)
run_state_machine(sm)
assert sm['output'] == [0, 0, 0, 0, 0, 0, 0, 0, 0, 3122865]


sm = load_state_machine('test')
add_input(sm, 5)
run_state_machine(sm)
assert sm['output'] == [773660]
