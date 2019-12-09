from itertools import permutations

from intcode import load_state_machine, run_state_machine, add_input, Tester

_tester = Tester('amplifier')


def create_amplifier(instructions, phase_settings):
    amp_a = load_state_machine(instructions)
    add_input(amp_a, phase_settings[0])
    amp_b = load_state_machine(instructions)
    add_input(amp_b, phase_settings[1])
    amp_c = load_state_machine(instructions)
    add_input(amp_c, phase_settings[2])
    amp_d = load_state_machine(instructions)
    add_input(amp_d, phase_settings[3])
    amp_e = load_state_machine(instructions)
    add_input(amp_e, phase_settings[4])
    return amp_a, amp_b, amp_c, amp_d, amp_e


def run_straight_amplifier(amps):
    signal = 0
    for amp in amps:
        add_input(amp, signal)
        run_state_machine(amp)
        signal = amp['output'][-1]
    return signal


def test_runner(runner, instruction_file, phase_settings, output):
    amps = create_amplifier(instruction_file, phase_settings)
    max_thrust = runner(amps)

    _tester.test(max_thrust == output, f'{max_thrust} != {output}')


test_runner(run_straight_amplifier, 'test1', [4, 3, 2, 1, 0], 43210)
test_runner(run_straight_amplifier, 'test2', [0, 1, 2, 3, 4], 54321)
test_runner(run_straight_amplifier, 'test3', [1, 0, 4, 3, 2], 65210)


def find_max_thrust(runner, phase_settings):
    perm = permutations(phase_settings)

    max_max_thrust = 0
    for p in perm:
        amps = create_amplifier('input', p)
        max_thrust = runner(amps)
        if max_thrust > max_max_thrust:
            max_max_thrust = max_thrust

    print(max_max_thrust)
    return max_max_thrust


assert find_max_thrust(run_straight_amplifier, [0, 1, 2, 3, 4]) == 70597


def run_feedback_amplifier(amps):
    signal = 0
    while not amps[-1]['halt']:
        for amp in amps:
            add_input(amp, signal)
            run_state_machine(amp)
            signal = amp['output'][-1]
    return signal


test_runner(run_feedback_amplifier, 'test4', [9, 8, 7, 6, 5], 139629729)
test_runner(run_feedback_amplifier, 'test5', [9, 7, 8, 5, 6], 18216)
_tester.summary()

assert find_max_thrust(run_feedback_amplifier, [5, 6, 7, 8, 9]) == 30872528
