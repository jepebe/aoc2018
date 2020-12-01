import intcode as ic


def sumify(string):
    number = ''
    parens = []
    stack = [0]
    nullify = [False]
    word = ''
    for c in string:
        if c.isnumeric():
            number += c
        elif not number and c == '-':
            number += '-'
        elif len(number) > 0 and number != '-':
            stack[0] += int(number)
            number = ''

        if c in '[{':
            parens.insert(0, c)
            stack.insert(0, 0)
            nullify.insert(0, False)

        elif c in ']}':
            is_array = parens.pop(0) == '['
            value = stack.pop(0)
            nullified = nullify.pop(0)
            if is_array or not nullified:
                stack[0] += value
            word = ''
        elif len(word) > 0 and c == '"':
            if word == 'red':
                nullify[0] = True
            word = ''
        elif c == '"':
            word = ''
        elif c.isalpha():
            word += c

    return stack[0]


tester = ic.Tester("JSAbacusFramework.io")

tester.test_value(sumify('[1,2,3]'), 6)
tester.test_value(sumify('[1,{"c":"red","b":2},3]'), 4)
tester.test_value(sumify('{"d":"red","e":[1,2,3,4],"f":5}'), 0)
tester.test_value(sumify('[1,"red",5]'), 6)

with open('input') as f:
    data = f.read()

tester.test_value(sumify(data), 68466, 'solution to exercise 2 = %s')
