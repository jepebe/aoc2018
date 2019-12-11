def red(text):
    return f'\033[31m{text}\033[0m'


def green(text):
    return f'\033[32m{text}\033[0m'


def blue(text):
    return f'\033[34m{text}\033[0m'


class Tester(object):

    def __init__(self, name) -> None:
        super().__init__()
        self._name = name
        self._count = 0
        self._fails = 0
        self._success = 0

    def test(self, test_state, message):
        self._count += 1
        if test_state:
            self._success += 1
            print(green(f'Test #{self._count} OK!'))
        else:
            self._fails += 1
            print(red(f'Test #{self._count} Error! {message}'))

    def test_value(self, a, b):
        self.test(a == b, f'{a} != {b}')

    def summary(self):
        if self._fails > 0:
            print(red(f'Error! {self._fails} test(s) failed!'))
        else:
            print(green(f'Success! {self._success} test(s) ran successfully!'))