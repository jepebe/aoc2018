import sys

original_line = sys.stdin.readline().strip()

print('Original line', len(original_line))

removeries = {c.lower() for c in original_line}

print(removeries)


def dict_min(dct, key):
    min_id = 0
    min_value = sys.maxsize
    for id, value in dct.items():
        if value[key] < min_value:
            min_id = id
            min_value = value[key]
    return dct[min_id]


def remove(c, k):
    return c == k or c == k.upper()


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


stats = {}


for r in removeries:
    line = [c for c in original_line if not remove(c, r)]

    new_line = optimize(line)

    stats[r] = {'r': r, 'len': len(new_line)}

print(stats)
print(dict_min(stats, 'len'))
