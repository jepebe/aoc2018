from itertools import permutations, product

import intcode as ic


def write_ascii(sm, string):
    for c in string:
        ic.add_input(sm, ord(c))
    ic.add_input(sm, ord('\n'))


sm = ic.load_state_machine('input')
write_ascii(sm, 'NOT A J')
write_ascii(sm, 'NOT J J')
write_ascii(sm, 'AND B J')
write_ascii(sm, 'AND C J')
write_ascii(sm, 'NOT J J')
write_ascii(sm, 'AND D J')
write_ascii(sm, 'WALK')

ic.run_state_machine(sm)
ic.print_output(sm)

tester = ic.Tester('springdroid')

tester.test_value(ic.get_last_output(sm), 19358870, 'Solution for part 1 is %s')


# test = '##.###..#'
# for b in product('#.', repeat=9):
#     b = ''.join(b)
#
#     if b in test:
#         print('woohoo')
#     if b[3] == '#' and b[7] == '#':
#         print(b)
#     elif b[3] == '#' and b[4] == '#' and b[8] == '#':
#         print(b)


ic.reset_state_machine(sm)
# D & (H | E) & (~A | ~B | ~C)
write_ascii(sm, 'NOT E T')
write_ascii(sm, 'NOT T T')
write_ascii(sm, 'OR H T')
write_ascii(sm, 'OR T J')
write_ascii(sm, 'AND D J')

# De morgans law? Not A or Not B or Not C -> Not (A and B and C)
# (~A | ~B | ~C) => ~(A & B & C)
write_ascii(sm, 'NOT A T')
write_ascii(sm, 'NOT T T')
write_ascii(sm, 'AND B T')
write_ascii(sm, 'AND C T')
write_ascii(sm, 'NOT T T')

write_ascii(sm, 'AND T J')

write_ascii(sm, 'RUN')

ic.run_state_machine(sm)
ic.print_output(sm)

tester.test_value(ic.get_last_output(sm), 1143356492, 'Solution for part 2 is %s')

tester.summary()
