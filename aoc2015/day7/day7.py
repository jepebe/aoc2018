from dataclasses import dataclass, field

import intcode as ic


def AND(a, b):
    return (a & b) & 0xFFFF


def OR(a, b):
    return (a | b) & 0xFFFF


def NOT(a, _):
    return ~a & 0xFFFF


def LSHIFT(a, n):
    return (a << n) & 0xFFFF


def RSHIFT(a, n):
    return (a >> n) & 0xFFFF


def NOP(a, _):
    return a


lookup = {
    "AND": AND,
    "OR": OR,
    "LSHIFT": LSHIFT,
    "RSHIFT": RSHIFT
}


@dataclass
class Circuit:
    circuit: dict = field(default_factory=dict)
    wires: dict = field(default_factory=dict)


def create_circuit(lines):
    circuit = Circuit()
    for line in lines:
        inst, result = list(map(str.strip, line.split('->')))

        if result in circuit.circuit:
            print(f"overwrite? {result}")

        if inst.isnumeric():
            circuit.wires[result] = int(inst)
        else:
            operands = inst.split(' ')
            if operands[0] == 'NOT':
                circuit.circuit[result] = NOT, operands[1], 'dummy'
            elif len(operands) == 1:
                circuit.circuit[result] = NOP, operands[0], 'dummy'
            else:
                circuit.circuit[result] = lookup[operands[1]], operands[0], operands[2]
    return circuit


def simulate(circuit):
    while len(circuit.circuit) > 0:
        delete = []
        for result, operation in circuit.circuit.items():
            a = None
            b = None

            if operation[1] in circuit.wires:
                a = circuit.wires[operation[1]]
            elif operation[1].isnumeric():
                a = int(operation[1])

            if operation[2] in circuit.wires:
                b = circuit.wires[operation[2]]
            elif operation[2].isnumeric():
                b = int(operation[2])
            elif operation[2] == 'dummy':
                b = operation[2]

            op = operation[0]

            if a is not None and b is not None:
                circuit.wires[result] = op(a, b)
                delete.append(result)

        for d in delete:
            del circuit.circuit[d]


tester = ic.Tester('assembly required')

test_circuit = create_circuit("""123 -> x
456 -> y
x AND y -> d
x OR y -> e
x LSHIFT 2 -> f
y RSHIFT 2 -> g
NOT x -> h
NOT y -> i
""".splitlines())

expected_result = {
    'd': 72,
    'e': 507,
    'f': 492,
    'g': 114,
    'h': 65412,
    'i': 65079,
    'x': 123,
    'y': 456,
}

simulate(test_circuit)
tester.test_value(test_circuit.wires, expected_result)

with open('input') as f:
    circuit_def = f.readlines()

circuit = create_circuit(circuit_def)
simulate(circuit)
tester.test_value(circuit.wires['a'], 16076)

circuit = create_circuit(circuit_def)
circuit.wires['b'] = 16076
simulate(circuit)
tester.test_value(circuit.wires['a'], 2797)
