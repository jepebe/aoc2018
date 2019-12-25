def inv_mod(n, m):
    return pow(n, m-2, m)


def load_shuffle(filename, num_cards):
    a = 1
    b = 0
    with open(filename) as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith('deal into new stack'):
                b -= a
                a *= -1
            elif line.startswith('cut '):
                cut = int(line[4:].strip())
                b += cut * a
            elif line.startswith('deal with increment '):
                inc = int(line[20:].strip())
                a *= inv_mod(inc, num_cards)
    return a, b


num_cards = 119315717514047
reps = 101741582076661
a, b = load_shuffle('input', num_cards)
a_n = pow(a, reps, num_cards)
b_n = b * (1 - a_n) * inv_mod(1 - a, num_cards)
print((2020 * a_n + b_n) % num_cards)