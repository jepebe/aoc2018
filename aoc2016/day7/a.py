import sys

lines = sys.stdin.readlines()


def abba(seg):
    if len(seg) < 4:
        return False
    if seg[-1] != seg[-2] and seg[-1] == seg[-4] and seg[-2] == seg[-3]:
        return True

    return False

tls_count = 0
for line in lines:
    line = line.strip()

    is_abba = False
    danger_mode = False
    l = []
    for c in line:
        if c == '[' or c == ']':
            l = []
            danger_mode = not danger_mode
        else:
            l.append(c)

            if abba(l):
                if danger_mode:
                    is_abba = False
                    break
                is_abba = True

    if is_abba:
        print(line)
        tls_count += 1

print(tls_count)

