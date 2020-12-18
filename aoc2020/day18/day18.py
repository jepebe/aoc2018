import intcode as ic

tester = ic.Tester('Operation Order')


def read_file(postfix=''):
    with open(f'input{postfix}') as f:
        lines = f.readlines()
    return lines


class Evaluator:
    def __init__(self):
        self.num = []
        self.stack = []

    def add_digit(self, c):
        self.num.append(c)

    def complete_number(self):
        if len(self.num) > 0:
            n = int(''.join(self.num))
            self.num.clear()
            self.push(n)

    def operate(self):
        stack = self.stack
        if len(stack) > 2 and isinstance(stack[0], int) and stack[1] != '(':
            if stack[1] in ('*', '+'):
                a = stack.pop(0)
                op = stack.pop(0)
                b = stack.pop(0)
                if op == '*':
                    self.push(a * b)
                elif op == '+':
                    self.push(a + b)

    def push(self, op):
        self.stack.insert(0, op)

    def complete_group(self, add_prec=False):
        if self.stack[1] == '(':
            a = self.stack.pop(0)
            self.stack.pop(0)
            self.stack.insert(0, a)
        elif add_prec and self.stack[1] == '?':
            while self.stack[1] == '?':
                self.stack[1] = '*'
                self.operate()
            a = self.stack.pop(0)
            self.stack.pop(0)
            self.stack.insert(0, a)

    def result(self):
        return self.stack[0]


def evaluate(expr, add_prec=False):
    evaluator = Evaluator()

    for i, c in enumerate(expr):
        if c.isdigit():
            evaluator.add_digit(c)
        elif c == ' ':
            evaluator.complete_number()
            evaluator.operate()
        elif c == '*':
            if add_prec:
                evaluator.push('?')
            else:
                evaluator.push('*')
        elif c == '+':
            evaluator.push('+')
        elif c == '(':
            evaluator.push('(')
        elif c == ')':
            evaluator.complete_number()
            evaluator.operate()
            evaluator.complete_group(add_prec=add_prec)

    evaluator.complete_number()
    evaluator.operate()
    if add_prec:
        new_expr = ' '.join(map(str, reversed(evaluator.stack)))
        new_expr = new_expr.replace('?', '*')
        return evaluate(new_expr)
    return evaluator.result()


tester.test_value(evaluate('1 + 2 * 3 + 4 * 5 + 6'), 71)
tester.test_value(evaluate('1 + (2 * 3) + (4 * (5 + 6))'), 51)
tester.test_value(evaluate('2 * 3 + (4 * 5)'), 26)
tester.test_value(evaluate('5 + (8 * 3 + 9 + 3 * 4 * 3)'), 437)
tester.test_value(evaluate('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))'), 12240)
tester.test_value(evaluate('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2'), 13632)


def evaluate_expressions(add_prec=False):
    lines = read_file()
    result = 0
    for line in lines:
        result += evaluate(line, add_prec)
    return result


result = evaluate_expressions()
tester.test_value(result, 1408133923393, 'solution to part 1=%s')

tester.test_value(evaluate('1 + 2 * 3 + 4 * 5 + 6', True), 231)
tester.test_value(evaluate('1 + (2 * 3) + (4 * (5 + 6))', True), 51)
tester.test_value(evaluate('2 * 3 + (4 * 5)', True), 46)
tester.test_value(evaluate('5 + (8 * 3 + 9 + 3 * 4 * 3)', True), 1445)
tester.test_value(evaluate('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))', True), 669060)
tester.test_value(evaluate('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2', True), 23340)

result = evaluate_expressions(add_prec=True)
tester.test_value(result, 314455761823725, 'solution to part 2=%s')
