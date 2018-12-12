import sys

lines = sys.stdin.readlines()


def cpy(computer, value, reg):
    if value in computer['registers']:
        value = computer['registers'][value]
    else:
        value = int(value)
    computer['registers'][reg] = value
    computer['pointer'] += 1


def inc(computer, reg):
    computer['registers'][reg] += 1
    computer['pointer'] += 1


def dec(computer, reg):
    computer['registers'][reg] -= 1
    computer['pointer'] += 1


def jnz(computer, value, jmp):
    if value in computer['registers']:
        value = computer['registers'][value]
    else:
        value = int(value)

    if value != 0:
        computer['pointer'] += int(jmp)
    else:
        computer['pointer'] += 1


computer = {
    'pointer': 0,
    'registers': {
        'a': 0,
        'b': 0,
        'c': 1,
        'd': 0
    },
    'instructions': {
        'cpy': cpy,
        'inc': inc,
        'dec': dec,
        'jnz': jnz
    },
    'program': [line.strip() for line in lines]
}

while computer['pointer'] < len(computer['program']):
    pointer = computer['pointer']
    instruction = computer['program'][pointer]

    cmd, *arg = instruction.split()

    computer['instructions'][cmd](computer, *arg)

    # print(cmd, arg)

print(computer)
print(computer['registers']['a'])
