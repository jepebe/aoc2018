import math

import aoc

tester = aoc.Tester("Full of Hot Air")


def dec_to_snafu(dec: int) -> str:
    snafu = ""
    borrow = 0
    while dec > 0 or borrow > 0:
        d = int(borrow + (dec % 5))
        borrow = 0
        dec //= 5

        match d:
            case 0 | 1 | 2:
                snafu = str(d) + snafu
            case 3:
                snafu = "=" + snafu
                borrow = 1
            case 4:
                snafu = "-" + snafu
                borrow = 1
            case 5:
                snafu = "0" + snafu
                borrow = 1
            case _:
                assert False, f"number out of range {d}"

    return snafu


def snafu_to_dec(snafu: str) -> int:
    dec = 0
    for index, c in enumerate(reversed(snafu)):
        match c:
            case "2":
                digit = 2
            case "1":
                digit = 1
            case "0":
                digit = 0
            case "-":
                digit = -1
            case "=":
                digit = -2
            case _:
                assert False, f"Unknown digit {c}"
        dec += math.pow(5, index) * digit

    return dec


def feed_bob(filename: str) -> str:
    data = aoc.read_input(filename)
    fuel = 0
    for line in data.splitlines():
        fuel += snafu_to_dec(line)
    return dec_to_snafu(fuel)


def run_tests(t: aoc.Tester):
    t.test_section("Tests")

    t.test_section("DEC to SNAFU")
    t.test_value(dec_to_snafu(1), "1")
    t.test_value(dec_to_snafu(2), "2")
    t.test_value(dec_to_snafu(3), "1=")
    t.test_value(dec_to_snafu(4), "1-")
    t.test_value(dec_to_snafu(5), "10")
    t.test_value(dec_to_snafu(6), "11")
    t.test_value(dec_to_snafu(7), "12")
    t.test_value(dec_to_snafu(8), "2=")
    t.test_value(dec_to_snafu(9), "2-")
    t.test_value(dec_to_snafu(10), "20")
    t.test_value(dec_to_snafu(15), "1=0")
    t.test_value(dec_to_snafu(20), "1-0")
    t.test_value(dec_to_snafu(2022), "1=11-2")
    t.test_value(dec_to_snafu(12345), "1-0---0")
    t.test_value(dec_to_snafu(314159265), "1121-1110-1=0")

    t.test_section("SNAFU to DEC")
    t.test_value(snafu_to_dec("1=-0-2"), 1747)
    t.test_value(snafu_to_dec("12111"), 906)
    t.test_value(snafu_to_dec("2=0="), 198)
    t.test_value(snafu_to_dec("21"), 11)
    t.test_value(snafu_to_dec("2=01"), 201)
    t.test_value(snafu_to_dec("111"), 31)
    t.test_value(snafu_to_dec("20012"), 1257)
    t.test_value(snafu_to_dec("112"), 32)
    t.test_value(snafu_to_dec("1=-1="), 353)
    t.test_value(snafu_to_dec("1-12"), 107)
    t.test_value(snafu_to_dec("12"), 7)
    t.test_value(snafu_to_dec("1="), 3)
    t.test_value(snafu_to_dec("122"), 37)

    t.test_value(feed_bob("test_input"), "2=-1=0")


run_tests(tester)

tester.test_section("Part 1")
tester.test_solution(feed_bob("input"), "2-0-0=1-0=2====20=-2")
