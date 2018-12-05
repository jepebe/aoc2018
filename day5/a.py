import sys

original_line = sys.stdin.readline().strip()
print('Original line', len(original_line))
line = list(original_line)


pops = 1
while pops > 0:
    new_line = []
    pops = 0
    for b in line:
        if new_line:
            a = new_line[-1]
            if a.lower() == b.lower() and a.islower() != b.islower():
                new_line.pop()
                pops += 1
                continue
        new_line.append(b)
    line = new_line

print(len(new_line))

