import sys

lines = sys.stdin.readlines()

for line in lines:
    line = line.strip()

    result = []
    pos = 0
    while pos < len(line):
        if line[pos] == '(':
            marker_end = line.find(')', pos)
            data = line[pos + 1:marker_end]
            size, repeat = map(int, data.split('x'))
            result.append(line[marker_end + 1:marker_end + 1 + size] * repeat)
            pos = marker_end + 1 + size
        else:
            result.append(line[pos])
            pos += 1

    result = ''.join(result)
    print(result, len(result))
