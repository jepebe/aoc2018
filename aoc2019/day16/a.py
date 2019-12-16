import intcode as ic


def load_input():
    with open('input') as f:
        num = f.readline().strip()
    return num


def find_fft(seq, phase_count):
    digits = len(seq)
    half = digits // 2

    seq = [int(seq[i % digits]) for i in range(digits)]
    new_seq = [0] * len(seq)
    sums = [0] * (1 + half)
    pattern = [0, 1, 0, -1]

    for _ in range(phase_count):
        for i, d in enumerate(seq[half:]):
            sums[i + 1] = d + sums[i]

        for digit in range(digits):
            dig_sum = 0
            if digit >= half:
                dig_sum += sums[-1] - sums[digit - half]
            else:
                for i in range(digit, digits):
                    p = pattern[((i + 1) // (digit + 1)) % 4]
                    dig_sum += seq[i] * p

            new_seq[digit] = abs(dig_sum) % 10
        seq, new_seq = new_seq, seq

    return ''.join(map(str, seq))


def find_fft_with_shift(seq, phase_count=100, repeat=10000):
    digits = len(seq)
    shift = int(seq[:7])

    seq = [int(seq[i % digits]) for i in range(shift, digits * repeat)]
    new_seq = [0] * len(seq)
    sums = [0] * (1 + len(seq))

    for _ in range(phase_count):
        for i, d in enumerate(seq):
            sums[i + 1] = d + sums[i]

        for digit in range(len(seq)):
            new_seq[digit] = abs(sums[-1] - sums[digit]) % 10
        seq, new_seq = new_seq, seq

    return ''.join(map(str, seq[:8]))


tester = ic.Tester('FFT')

tester.test_value(find_fft('12345678', 1), '48226158')
tester.test_value(find_fft('12345678', 2), '34040438')
tester.test_value(find_fft('12345678', 3), '03415518')
tester.test_value(find_fft('12345678', 4), '01029498')

tester.test_value(find_fft('80871224585914546619083218645595', 100)[:8], '24176176')
tester.test_value(find_fft('19617804207202209144916044189917', 100)[:8], '73745418')
tester.test_value(find_fft('69317163492948606335995924319873', 100)[:8], '52432133')

input_data = load_input()
tester.test_value(find_fft(input_data, 100)[:8], '85726502', 'Solution to part 1 %s')

tester.test_value(find_fft_with_shift('03036732577212944063491565474664'), '84462026')
tester.test_value(find_fft_with_shift('02935109699940807407585447034323'), '78725270')
tester.test_value(find_fft_with_shift('03081770884921959731165446850517'), '53553731')

tester.test_value(find_fft_with_shift(input_data), '92768399', 'Solution to part 2 %s')

tester.summary()
