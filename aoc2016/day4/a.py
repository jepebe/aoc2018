import sys
import re

lines = sys.stdin.readlines()

pattern = re.compile('([a-z\-]+)([0-9]+)\[([a-z]+)]')

alphabet = 'abcdefghijklmnopqrstuvwxyz'


def count_chars(group):
    count = {}
    for c in group:
        if not c in count:
            count[c] = 0
        count[c] += 1
    return count


def is_real(items, checksum):
    real = True
    for index, c in enumerate(checksum):
        x, cnt = items[index]
        if c == x:
            continue
        else:
            return False
    return real


def shift_cipher(c, shift):
    if c == '-':
        return ' '

    i = alphabet.index(c)
    i += shift
    i = i % 26
    return alphabet[i]

sum = 0

for line in lines:
    match = pattern.match(line)

    count = count_chars(match.group(1))
    id = int(match.group(2))
    checksum = match.group(3)

    del count['-']

    items = list(sorted(count.items(), key=lambda x: (-x[1], x[0])))

    real_room = is_real(items, checksum)

    sum += id if real_room else 0

    if real_room:
        decrypted = [shift_cipher(c, id) for c in match.group(1)]
        name = ''.join(decrypted)
        if name.startswith('nort'):
            print('---->')
        print(id, name)

    # print(count, items, real_room)

print('Sum', sum)
