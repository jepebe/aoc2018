import time

TROPHY = "\U0001f3c6"  # 🏆
GREEN_CHECK = "\u2705"  # ✅
RED_CROSS = "\u274C"  # ❌
DELTA = "\u0394"  # Δ
HOUR_GLASS = "\u23f3"  # ⌛
STOPWATCH = "\u23f1"  # ⏱
STAR = "\u2b50"  # ⭐
FROWN = "\u2639\ufe0f"  # ☹️


def red(text):
    return color(text, 196)


def color(text, value=0):
    return "\033[38;5;%im%s\033[0m" % (value, text)


def green(text):
    return color(text, 34)


def blue(text):
    return color(text, 69)


def yellow(text):
    return color(text, 226)


def grey(text):
    return color(text, 240)


class Tester(object):
    def __init__(self, name) -> None:
        if not name:
            raise RuntimeError("Missing test name!")
        print(yellow(f"--== {name} ==--"))

        self._name = name
        self._count = 0
        self._fails = 0
        self._success = 0
        self.now = time.time()
        self.delta = self.now
        self.part = 1
        self._exception_occurred = False

        import atexit

        atexit.register(self.summary)

        import sys

        def except_hook(exctype, value, traceback):
            self._exception_occurred = True
            sys.__excepthook__(exctype, value, traceback)

        sys.excepthook = except_hook

    def test(self, test_state, message="", success_message=""):
        self._count += 1
        delta = self.delta_time()
        print(f"{delta} ", end="")
        count = f"#{self._count}"
        if test_state:
            self._success += 1
            success_message = grey(success_message)
            print(green(F"{GREEN_CHECK}  Test {count:>3} OK! {success_message}"))
        else:
            self._fails += 1
            print(red(f"{RED_CROSS}  Test {count:>3} Error! {message}"))

    def test_value(self, a, b, success_message=""):
        if "%s" in success_message:
            success_message = success_message % a
        elif success_message == "":
            success_message = f"{a} == {b}"

        self.test(a == b, f"{a} == {b}", success_message=success_message)

    def test_solution(self, a, b):
        msg = f"Solution to part {self.part} = {a} {STAR}"
        self.test(a == b, f"{a} != {b} {FROWN}", success_message=green(msg))
        self.part += 1

    def test_value_neq(self, a, b, message=""):
        self.test(a != b, f"{a} != {b} {message}", f"{a} != {b}")

    def test_less_or_equal(self, a, b, message=""):
        self.test(a <= b, f"{a} <= {b} {message}", f"{a} <= {b}")

    def test_greater_or_equal(self, a, b, message=""):
        self.test(a >= b, f"{a} >= {b} {message}", f"{a} >= {b}")

    def test_greater_than(self, a, b, message=""):
        self.test(a > b, f"{a} > {b} {message}", f"{a} > {b}")

    def test_less_than(self, a, b, message=""):
        self.test(a < b, f"{a} < {b} {message}", f"{a} < {b}")

    def test_section(self, section_name):
        print()
        print(yellow(f"[{section_name}]"))

    def summary(self):
        trophy = ""
        running_time = time.time() - self.now

        print()
        if self._exception_occurred:
            print(red(f"Error! Exception occurred after running {self._count} test(s)!"))
        elif self._fails > 0:
            print(red(f"Error! {self._fails} of {self._count} test(s) failed!"))
        else:
            print(green(f"Success! {self._success} test(s) ran successfully!"))
            trophy = TROPHY if running_time < 1 else ""

        print(yellow(f"Running time: {running_time :0.04f} s. {trophy}"))

    def delta_time(self):
        msg = blue(f"[{STOPWATCH} {time.time() - self.delta:0.04f} s.]")
        self.delta = time.time()
        return msg

    def peek_delta_time(self, message=""):
        timing = blue(f"[{STOPWATCH} {time.time() - self.delta:0.04f} s.]")
        print(f"    {yellow(message)} {timing}")


if __name__ == "__main__":
    for y in range(16):
        row = []
        for x in range(16):
            i = y * 16 + x
            row.append(color("%4i", i) % i)
        print("".join(row))

    tester = Tester("tester")
    tester.test_value(1, 1)
    tester.summary()
    tester.test_value(1, 2)
    tester.summary()

    tester.test_section("<")
    tester.test_less_than(1, 2)
    tester.test_less_than(1, 1)
    tester.test_less_than(2, 1)

    tester.test_section("<=")
    tester.test_less_or_equal(1, 2)
    tester.test_less_or_equal(1, 1)
    tester.test_less_or_equal(2, 1)

    tester.test_section(">")
    tester.test_greater_than(1, 2)
    tester.test_greater_than(1, 1)
    tester.test_greater_than(2, 1)

    tester.test_section(">=")
    tester.test_greater_or_equal(1, 2)
    tester.test_greater_or_equal(1, 1)
    tester.test_greater_or_equal(2, 1)

    tester.test_section("!=")
    tester.test_value_neq(1, 2)
    tester.test_value_neq(1, 1)
    tester.test_value_neq(2, 1)

    tester.test_section("==")
    tester.test_value(1, 2)
    tester.test_value(1, 1)
    tester.test_value(2, 1)

    tester.test_section("check")
    tester.test(1 == 1, "failure", "success")
    tester.test(1 == 2, "failure", "success")

    tester.test_section("Solution")
    tester.test_solution(1, 1)
    tester.test_solution(1, 2)
