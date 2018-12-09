import sys

lines = sys.stdin.readlines()


def aba(seg):
    if len(seg) < 3:
        return False
    if seg[-1] != seg[-2] and seg[-1] == seg[-3]:
        return True
    return False


def switch(seq):
    return seq[1] + seq[0] + seq[1]


ssl_count = 0
for line in lines:
    line = line.strip()

    supernet_abas = []
    hypernet_abas = []
    hypernet = False
    l = []
    for c in line:
        if c == '[' or c == ']':
            l = []
            hypernet = not hypernet
        else:
            l.append(c)

        if aba(l):
            if hypernet:
                hypernet_abas.append(''.join(l[-1:-4:-1]))
            else:
                supernet_abas.append(''.join(l[-1:-4:-1]))

    for seq in supernet_abas:
        seq = switch(seq)
        if seq in hypernet_abas:
            print(line)
            print(supernet_abas, hypernet_abas)
            ssl_count += 1
            break


print(ssl_count)
#    if is_abba:
#        print(line)
#        tls_count += 1
#
# print(tls_count)
