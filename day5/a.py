import sys

original_line = sys.stdin.readline().strip()
print('Original line', len(original_line))
line = list(original_line)


def optimize(line):
    new_line = []
    for b in line:
        if new_line:
            a = new_line[-1]
            if a.lower() == b.lower() and a.islower() != b.islower():
                new_line.pop()
                continue
        new_line.append(b)
    return new_line


print(len(optimize(line)))
