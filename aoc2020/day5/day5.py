import intcode as ic


def read_file():
    with open('input') as f:
        lines = f.readlines()
    return lines


def parse_seat(seat):
    seat = seat.replace('B', '1').replace('F', '0').replace('R', '1').replace('L', '0')

    id = int(seat, base=2)
    row = id >> 3
    column = id & 7
    return row, column, id


def find_max_line(lines):
    max_seat = 0
    seats = {seat: True for seat in range(1024)}
    for line in lines:
        r, c, id = parse_seat(line.strip())
        if id > max_seat:
            max_seat = id
        del seats[id]

    i = 0
    while i in seats and seats[i]:
        del seats[i]
        i += 1

    i = 1023
    while i in seats and seats[i]:
        del seats[i]
        i -= 1
    return max_seat, list(seats.keys())[0]


tester = ic.Tester("Binary Boarding")

tester.test_value(parse_seat('FBFBBFFRLR'), (44, 5, 357))
tester.test_value(parse_seat('BFFFBBFRRR'), (70, 7, 567))
tester.test_value(parse_seat('FFFBBBFRRR'), (14, 7, 119))
tester.test_value(parse_seat('BBFFBBFRLL'), (102, 4, 820))

lines = read_file()
max_seat, my_seat = find_max_line(lines)
tester.test_value((max_seat, my_seat), (928, 610), 'solution to exercise 1=%s and 2=%s')

max_seat = max(int(seat.replace('B', '1').replace('F', '0').replace('R', '1').replace('L', '0'), base=2) for seat in lines)
tester.test_value(max_seat, 928, 'solution to exercise 1=%s')

max_seat = max(int(''.join(map(str, ['FBLR'.index(c) % 2 for c in s.strip()])), 2) for s in lines)
tester.test_value(max_seat, 928, 'solution to exercise 1=%s')
