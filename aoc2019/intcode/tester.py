def red(text):
    return color(text, 196)


def color(text, value=0):
    return '\u001b[38;5;%im%s\u001b[0m' % (value, text)


def green(text):
    return color(text, 34)


def blue(text):
    return color(text, 69)


def yellow(text):
    return color(text, 226)


class Tester(object):

    def __init__(self, name) -> None:
        super().__init__()
        self._name = name
        self._count = 0
        self._fails = 0
        self._success = 0

    def test(self, test_state, message, success_message=''):
        self._count += 1
        if test_state:
            self._success += 1
            print(green(f'\u2705  Test #{self._count} OK! {success_message}'))
        else:
            self._fails += 1
            print(red(f'\u274C  Test #{self._count} Error! {message}'))

    def test_value(self, a, b, success_message=''):
        if '%s' in success_message:
            success_message = success_message % a
        self.test(a == b, f'{a} != {b}', success_message=yellow(success_message))

    def test_value_neq(self, a, b):
        self.test(a != b, f'{a} == {b}')

    def summary(self):
        if self._fails > 0:
            print(red(f'Error! {self._fails} of {self._count} test(s) failed!'))
        else:
            print(green(f'Success! {self._success} test(s) ran successfully!'))


if __name__ == '__main__':
    for y in range(16):
        row = []
        for x in range(16):
            i = y * 16 + x
            row.append(color('%4i', i) % i)
        print(''.join(row))

    tester = Tester('tester')
    tester.test_value(1, 1)
    tester.summary()
    tester.test_value(1, 2)
    tester.summary()
