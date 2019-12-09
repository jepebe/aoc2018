from intcode import load_state_machine, run_state_machine


def intcode(state_machine, noun=None, verb=None):
    opcodes = state_machine['instructions']
    if noun is not None:
        opcodes[1] = noun
    if verb is not None:
        opcodes[2] = verb
    run_state_machine(state_machine)
    return opcodes[0]


def find_noun_and_verb():
    for noun in range(0, 100):
        for verb in range(0, 100):
            sm = load_state_machine('test')
            if intcode(sm, noun, verb) == 19690720:
                return 100 * noun + verb
    return None


sm = load_state_machine('test')
assert intcode(sm) == 655695

sm = load_state_machine('test')
assert intcode(sm, 12, 2) == 3085697

assert find_noun_and_verb() == 9425


