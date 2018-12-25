import sys


def addr(pointer_register, line_no, reg_a, reg_b, reg_c):
    if reg_a == pointer_register:
        reg_a = line_no
    else:
        reg_a = f'reg[{reg_a}]'

    if reg_b == pointer_register:
        reg_b = line_no
    else:
        reg_b = f'reg[{reg_b}]'

    return f'reg[{reg_c}] = {reg_a} + {reg_b};'


def addi(pointer_register, line_no, reg_a, val_b, reg_c):
    if reg_a == pointer_register:
        reg_a = line_no
    else:
        reg_a = f'reg[{reg_a}]'

    return f'reg[{reg_c}] = {reg_a} + {val_b};'


def mulr(pointer_register, line_no, reg_a, reg_b, reg_c):
    if reg_a == pointer_register:
        reg_a = line_no
    else:
        reg_a = f'reg[{reg_a}]'

    if reg_b == pointer_register:
        reg_b = line_no
    else:
        reg_b = f'reg[{reg_b}]'
    return f'reg[{reg_c}] = {reg_a} * {reg_b};'


def muli(pointer_register, line_no, reg_a, val_b, reg_c):
    if reg_a == pointer_register:
        reg_a = line_no
    else:
        reg_a = f'reg[{reg_a}]'

    return f'reg[{reg_c}] = {reg_a} * {val_b};'


def banr(pointer_register, line_no, reg_a, reg_b, reg_c):
    if reg_a == pointer_register:
        reg_a = line_no
    else:
        reg_a = f'reg[{reg_a}]'

    if reg_b == pointer_register:
        reg_b = line_no
    else:
        reg_b = f'reg[{reg_b}]'
    return f'reg[{reg_c}] = {reg_a} & {reg_b};'


def bani(pointer_register, line_no, reg_a, val_b, reg_c):
    if reg_a == pointer_register:
        reg_a = line_no
    else:
        reg_a = f'reg[{reg_a}]'

    return f'reg[{reg_c}] = {reg_a} & {val_b};'


def borr(pointer_register, line_no, reg_a, reg_b, reg_c):
    if reg_a == pointer_register:
        reg_a = line_no
    else:
        reg_a = f'reg[{reg_a}]'

    if reg_b == pointer_register:
        reg_b = line_no
    else:
        reg_b = f'reg[{reg_b}]'
    return f'reg[{reg_c}] = {reg_a} | {reg_b};'


def bori(pointer_register, line_no, reg_a, val_b, reg_c):
    if reg_a == pointer_register:
        reg_a = line_no
    else:
        reg_a = f'reg[{reg_a}]'

    return f'reg[{reg_c}] = {reg_a} | {val_b};'


def setr(pointer_register, line_no, reg_a, _, reg_c):
    return f'reg[{reg_c}] = reg[{reg_a}];'


def seti(pointer_register, line_no, val_a, _, reg_c):
    return f'reg[{reg_c}] = {val_a};'


def gtir(pointer_register, line_no, val_a, reg_b, reg_c):
    if reg_b == pointer_register:
        reg_b = line_no
    else:
        reg_b = f'reg[{reg_b}]'

    return f'reg[{reg_c}] = {val_a} > {reg_b};'


def gtri(reg_a, val_b, reg_c):
    if reg_a == pointer_register:
        reg_a = line_no
    else:
        reg_a = f'reg[{reg_a}]'

    return f'reg[{reg_c}] = {reg_a} > {val_b};'


def gtrr(pointer_register, line_no, reg_a, reg_b, reg_c):
    if reg_a == pointer_register:
        reg_a = line_no
    else:
        reg_a = f'reg[{reg_a}]'

    if reg_b == pointer_register:
        reg_b = line_no
    else:
        reg_b = f'reg[{reg_b}]'

    return f'reg[{reg_c}] = {reg_a} > {reg_b};'


def eqir(pointer_register, line_no, val_a, reg_b, reg_c):
    if reg_b == pointer_register:
        reg_b = line_no
    else:
        reg_b = f'reg[{reg_b}]'

    return f'reg[{reg_c}] = {val_a} == {reg_b};'


def eqri(pointer_register, line_no, reg_a, val_b, reg_c):
    if reg_a == pointer_register:
        reg_a = line_no
    else:
        reg_a = f'reg[{reg_a}]'

    return f'reg[{reg_c}] = {reg_a} == {val_b};'


def eqrr(pointer_register, line_no, reg_a, reg_b, reg_c):
    if reg_a == pointer_register:
        reg_a = line_no
    else:
        reg_a = f'reg[{reg_a}]'

    if reg_b == pointer_register:
        reg_b = line_no
    else:
        reg_b = f'reg[{reg_b}]'
    return f'reg[{reg_c}] = {reg_a} == {reg_b};'


def addi_goto(pointer_register, line_no, reg_a, val_b, reg_c):
    if reg_a == pointer_register:
        return f'goto LINE{line_no + val_b + 1}; goto JUMP;'
    else:
        return f'reg[{reg_c}] = reg[{reg_a}] + {val_b} + 1; goto JUMP;'


def addr_goto(pointer_register, line_no, reg_a, reg_b, reg_c):
    if reg_a == pointer_register:
        reg_a = line_no
    else:
        reg_a = f'reg[{reg_a}]'

    if reg_b == pointer_register:
        reg_b = line_no
    else:
        reg_b = f'reg[{reg_b}]'

    return f'reg[{reg_c}] = {reg_a} + {reg_b} + 1; goto JUMP;'


def setr_goto(pointer_register, line_no, reg_a, _, reg_c):
    if reg_a == pointer_register:
        reg_a = line_no
    else:
        reg_a = f'reg[{reg_a}]'

    return f'reg[{reg_c}] = {reg_a} + 1; goto JUMP;'


def seti_goto(pointer_register, line_no, val_a, _, reg_c):
    return f'goto LINE{val_a + 1};'
    #return f'reg[{reg_c}] = {val_a} + 1; goto JUMP;'


def oprr_goto(pointer_register, line_no, reg_a, reg_b, reg_c, op):
    if reg_a == pointer_register:
        reg_a = line_no
    else:
        reg_a = f'reg[{reg_a}]'

    if reg_b == pointer_register:
        reg_b = line_no
    else:
        reg_b = f'reg[{reg_b}]'

    return f'reg[{reg_c}] = ({reg_a} {op} {reg_b}) + 1; goto JUMP;'


def opri_goto(pointer_register, line_no, reg_a, val_b, reg_c, op):
    if reg_a == pointer_register:
        reg_a = line_no
    else:
        reg_a = f'reg[{reg_a}]'


    return f'reg[{reg_c}] = ({reg_a} {op} {val_b}) + 1; goto JUMP;'


opcodes = {
    'addi': addi,
    'addr': addr,
    'seti': seti,
    'setr': setr,
    'muli': muli,
    'mulr': mulr,
    'bani': bani,
    'banr': banr,
    'bori': bori,
    'borr': borr,
    'gtir': gtir,
    'gtri': gtri,
    'gtrr': gtrr,
    'eqir': eqir,
    'eqri': eqri,
    'eqrr': eqrr
}


def create_jump_table(line_count, pointer_register, prefix='\t'):
    jump = f'{prefix}JUMP:\n'
    for i in range(line_count):
        jump += f'{prefix}if (reg[{pointer_register}] == {i})\n'
        jump += f'{prefix}\tgoto LINE{i};\n'
    jump += f'{prefix}goto END;\n'
    return jump


def build_instruction_list(lines):
    pointer_register = None
    instructions = []
    line_no = 0
    for line in lines:
        if line.startswith('#ip'):
            pointer_register = int(line[4:])
        elif line.startswith('#'):
            continue
        else:
            opc, *abc = line.strip().split()
            a, b, c = map(int, abc)

            opcode = opcodes[opc]

            if c == pointer_register:
                if opc == 'addi':
                    instruction = addi_goto(pointer_register, line_no, a, b, c)
                elif opc in ('addr', 'mulr'):
                    ops = {'addr': '+', 'mulr': '*'}
                    instruction = oprr_goto(pointer_register, line_no, a, b, c, ops[opc])
                elif opc == 'setr':
                    instruction = setr_goto(pointer_register, line_no, a, b, c)
                elif opc == 'seti':
                    instruction = seti_goto(pointer_register, line_no, a, b, c)
                else:
                    print(f'Unhandled pointer update {opc}')
                instructions.append(instruction)
            else:
                instructions.append(opcode(pointer_register, line_no, a, b, c))
            line_no += 1
    return instructions, pointer_register


if __name__ == '__main__':
    lines = sys.stdin.readlines()

    with open('program.c', 'w') as f:
        f.write('#include <stdio.h>\n')
        f.write('int main(int argc, char ** argv) {\n')
        f.write('\tlong long reg[6] = {0, 0, 0, 0, 0, 0};\n')

        instructions, pointer_register = build_instruction_list(lines)
        jump = create_jump_table(len(instructions), pointer_register)
        f.write('\tgoto LINE0;\n')
        f.write(jump)
        f.write('\n')

        for line_no, instruction in enumerate(instructions):
            f.write(f'\tLINE{line_no}: ' + instruction + '\n')

        f.write(f'\tEND:\n')
        f.write('\tprintf("[%lld, %lld, %lld, %lld, %lld, %lld]\\n", '
                'reg[0], reg[1], reg[2], reg[3], reg[4], reg[5]);\n')
        f.write('\treturn 0;\n')
        f.write('}\n')
