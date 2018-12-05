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


stats = {}


for r in removeries:
    line = [c for c in original_line if not remove(c, r)]

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

    stats[r] = {'r': r, 'len': len(new_line)}

print(stats)
print(dict_min(stats, 'len'))
