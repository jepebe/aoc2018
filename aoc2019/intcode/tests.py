from intcode.state_machine import create_state_machine, run_state_machine, add_input
from intcode.tester import Tester

_tester = Tester('state_machine')


def test_state_machine(instructions, result):
    sm = create_state_machine(instructions)
    add_input(sm, 1)
    run_state_machine(sm)

    _tester.test(sm['instructions'] == result, f'{sm["instructions"]} != {result}')


def test_state_machine_output(instructions, input, output):
    sm = create_state_machine(instructions)
    sm['input'] = [input]
    run_state_machine(sm)

    _tester.test(sm['output'] == output, f'{sm["output"]} != {output}')


def test_state_machines():
    test_state_machine([1, 0, 0, 0, 99], [2, 0, 0, 0, 99])
    test_state_machine([2, 3, 0, 3, 99], [2, 3, 0, 6, 99])
    test_state_machine([2, 4, 4, 5, 99, 0], [2, 4, 4, 5, 99, 9801])
    test_state_machine([1, 1, 1, 4, 99, 5, 6, 0, 99], [30, 1, 1, 4, 2, 5, 6, 0, 99])
    test_state_machine([1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50],
                       [3500, 9, 10, 70, 2, 3, 11, 0, 99, 30, 40, 50])

    test_state_machine_output([3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], 7, [0])
    test_state_machine_output([3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], 8, [1])

    test_state_machine_output([3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8], 7, [1])
    test_state_machine_output([3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8], 8, [0])

    test_state_machine_output([3, 3, 1108, -1, 8, 3, 4, 3, 99], 8, [1])
    test_state_machine_output([3, 3, 1108, -1, 8, 3, 4, 3, 99], 7, [0])

    test_state_machine_output([3, 3, 1107, -1, 8, 3, 4, 3, 99], 7, [1])
    test_state_machine_output([3, 3, 1107, -1, 8, 3, 4, 3, 99], 8, [0])

    test_state_machine_output([3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9], 0, [0])
    test_state_machine_output([3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9], 1, [1])

    test_state_machine_output([3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1], 0, [0])
    test_state_machine_output([3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1], 1, [1])

    inst = [3, 21, 1008, 21, 8, 20, 1005, 20, 22, 107, 8, 21, 20, 1006, 20, 31,
            1106, 0, 36, 98, 0, 0, 1002, 21, 125, 20, 4, 20, 1105, 1, 46, 104,
            999, 1105, 1, 46, 1101, 1000, 1, 20, 4, 20, 1105, 1, 46, 98, 99]

    test_state_machine_output(inst, 7, [999])
    test_state_machine_output(inst, 8, [1000])
    test_state_machine_output(inst, 9, [1001])

    code = [109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99]
    test_state_machine_output(code, 0, code)

    code = [1102, 34915192, 34915192, 7, 4, 7, 99, 0]
    test_state_machine_output(code, 0, [1219070632396864])

    code = [104, 1125899906842624, 99]
    test_state_machine_output(code, 0, [1125899906842624])

    _tester.summary()


if __name__ == '__main__':
    test_state_machines()
