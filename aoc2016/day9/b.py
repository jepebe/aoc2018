import sys

lines = sys.stdin.readlines()


def decompress(line, start, end):
    #print('#', line[start:end])
    length = 0
    pos = start
    while pos < end:
        if line[pos] == '(':
            marker_end = line.find(')', pos)
            data = line[pos + 1:marker_end]
            size, repeat = map(int, data.split('x'))

            length += decompress(line, marker_end + 1, marker_end + 1 + size) * repeat
            pos = marker_end + 1 + size

        else:
            # print('->', line[pos])
            length += 1
            pos += 1
    return length


for line in lines:
    line = line.strip()

    print(decompress(line, 0, len(line)))
