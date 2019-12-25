from collections import deque

import intcode as ic


def deal_into_stack(deck):
    deck.reverse()
    # print(f'deal into new stack')
    # print(deck)
    return deck


def index_deal_into_stack(deck_size, index):
    new_index = deck_size - index - 1
    # print(f'deal into new stack {new_index}')
    return new_index


def cut_deck(deck, cut):
    mini_stack = deque()
    for i in range(abs(cut)):
        if cut > 0:
            mini_stack.append(deck.popleft())
        else:
            mini_stack.append(deck.pop())

    for card in mini_stack:
        if cut > 0:
            deck.append(card)
        else:
            deck.appendleft(card)

    # print(f'cut {cut}')
    # print(deck)
    return deck


def index_cut_deck(deck_size, index, cut):
    if cut > 0:
        if index >= deck_size - cut:
            index = index - (deck_size - cut)
        else:
            index += cut
    else:
        if index >= abs(cut):
            index += cut
        else:
            index = deck_size + cut + index
    # print(f'cut {cut} -> {index}')
    return index


def deal_with_inc(deck, inc):
    new_deck = deque(['_'] * len(deck))
    while deck:
        new_deck[0] = deck.popleft()
        new_deck.rotate(-inc)
    # print(f'deal with increment {inc}')
    # print(new_deck)
    return new_deck


def index_deal_with_inc(deck_size, index, inc):
    return modinv(inc, deck_size) * index % deck_size


def shuffle(ops, deck_size, repeat=1):
    deck = deque([i for i in range(deck_size)])
    for i in range(repeat):
        for shuffle_op in ops:
            deck = shuffle_op(deck)
    return list(deck)


def index_shuffle(iops, deck_size, index, repeat=1):
    memo = {}
    for i in range(repeat):
        d = 0
        indexes = [index]
        for shuffle_iop in reversed(iops):
            new_index = shuffle_iop(deck_size, index)
            indexes.append(index - new_index)
            d += index - new_index
            index = new_index

        if d not in memo:
            memo[d] = i
        else:
            print('repeat', d, i)

    return index


def wrap_fn(fn, value):
    def lfn(deck):
        return fn(deck, value)

    return lfn


def wrap_ifn(fn, value):
    def lfn(deck_size, index):
        return fn(deck_size, index, value)

    return lfn


def load_shuffle(filename):
    ops = []
    iops = []
    with open(filename) as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith('deal into new stack'):
                ops.append(deal_into_stack)
                iops.append(index_deal_into_stack)
            elif line.startswith('cut '):
                cut = int(line[4:].strip())
                ops.append(wrap_fn(cut_deck, cut))
                iops.append(wrap_ifn(index_cut_deck, cut))
            elif line.startswith('deal with increment '):
                inc = int(line[20:].strip())
                ops.append(wrap_fn(deal_with_inc, inc))
                iops.append(wrap_ifn(index_deal_with_inc, inc))
    return ops, iops


def egcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, y, x = egcd(b % a, a)
        return g, x - (b // a) * y, y


def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m


tester = ic.Tester('decks')

print('deal into stack')
dis = index_deal_into_stack(10, 0)
tester.test_value(dis, 9)

print('deal with inc')
dwi3 = list(deal_with_inc(deque([i for i in range(10)]), 3))
tester.test_value(dwi3, [0, 7, 4, 1, 8, 5, 2, 9, 6, 3])

dwi3 = index_deal_with_inc(19, 5, 7)
tester.test_value(dwi3, 17)
dwi3 = index_deal_with_inc(19, 12, 7)
tester.test_value(dwi3, 18)

print('cut index')
dwc = index_cut_deck(10, 7, 3)
tester.test_value(dwc, 0)
dwc = index_cut_deck(10, 8, 3)
tester.test_value(dwc, 1)
dwc = index_cut_deck(10, 0, 3)
tester.test_value(dwc, 3)
dwc = index_cut_deck(10, 1, 3)
tester.test_value(dwc, 4)

print('cut index negative')
dwc = index_cut_deck(10, 4, -4)
tester.test_value(dwc, 0)
dwc = index_cut_deck(10, 5, -4)
tester.test_value(dwc, 1)
dwc = index_cut_deck(10, 9, -4)
tester.test_value(dwc, 5)
dwc = index_cut_deck(10, 0, -4)
tester.test_value(dwc, 6)
dwc = index_cut_deck(10, 1, -4)
tester.test_value(dwc, 7)

print('shuffling')
shuffle_ops, shuffle_iops = load_shuffle('test1')
new_deck = shuffle(shuffle_ops, 10)
tester.test_value(new_deck, [0, 3, 6, 9, 2, 5, 8, 1, 4, 7])

new_index = index_shuffle(shuffle_iops, 10, 9)
tester.test_value(new_index, 7)

shuffle_ops, shuffle_iops = load_shuffle('test2')
new_deck = shuffle(shuffle_ops, 10)
tester.test_value(new_deck, [3, 0, 7, 4, 1, 8, 5, 2, 9, 6])

new_index = index_shuffle(shuffle_iops, 10, 9)
tester.test_value(new_index, 6)

shuffle_ops, shuffle_iops = load_shuffle('test3')
new_deck = shuffle(shuffle_ops, 10)
tester.test_value(new_deck, [6, 3, 0, 7, 4, 1, 8, 5, 2, 9])

new_index = index_shuffle(shuffle_iops, 10, 9)
tester.test_value(new_index, 9)

shuffle_ops, shuffle_iops = load_shuffle('test4')
new_deck = shuffle(shuffle_ops, 10)
tester.test_value(new_deck, [9, 2, 5, 8, 1, 4, 7, 0, 3, 6])

new_index = index_shuffle(shuffle_iops, 10, 9)
tester.test_value(new_index, 6)

shuffle_ops, shuffle_iops = load_shuffle('input')
new_deck = shuffle(shuffle_ops, 10007)
index_of_2019 = new_deck.index(2019)
tester.test_value_neq(index_of_2019, 4648)  # wrong answer 1
tester.test_value(index_of_2019, 4684, 'Solution to part 1 is %s')


index_of_4684 = index_shuffle(shuffle_iops, 10007, 4684, repeat=1)
tester.test_value(index_of_4684, 2019)


index_of_2020 = index_shuffle(shuffle_iops, 119_315_717_514_047, 2020, repeat=101_741_582_076_661)
tester.test_value(index_of_2020, 4684, 'Solution to part 2 is %s')
