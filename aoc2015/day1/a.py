import intcode as ic


def find_floor(parens):
    floor = 0
    basement = None
    for i, p in enumerate(parens):
        if p == '(':
            floor += 1
        elif p == ')':
            floor -= 1
        else:
            print("What?")

        if floor == -1 and basement is None:
            basement = i + 1
    return floor, basement


tester = ic.Tester('lisp')

tester.test_value(find_floor("(())"), (0, None))
tester.test_value(find_floor("()()"), (0, None))
tester.test_value(find_floor("((("), (3, None))
tester.test_value(find_floor("(()(()("), (3, None))
tester.test_value(find_floor('))((((())))'), (-1, 1))
tester.test_value(find_floor(')))'), (-3, 1))
tester.test_value(find_floor(')())())'), (-3, 1))

with open("input") as f:
    data = f.read()

floor, basement = find_floor(data)
tester.test_value(floor, 74)
tester.test_value(basement, 1795)
print(f'Santa ends up on floor {floor} enters the basement at {basement}')

tester.summary()
