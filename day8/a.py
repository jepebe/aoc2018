import sys

line = sys.stdin.readline()

data = list(map(int, line.split()))


def tree(data, pos):
    child_count = data[pos]
    metadata_count = data[pos + 1]

    metadata = []
    values = []
    pos += 2
    for child in range(child_count):
        pos, md, value = tree(data, pos)
        values.append(value)
        metadata.extend(md)

    local_metadata = data[pos:pos + metadata_count]
    metadata.extend(local_metadata)

    if child_count == 0:
        value = sum(local_metadata)
    else:
        value = 0

        for i in local_metadata:
            if 0 < i <= child_count:
                value += values[i - 1]
    return pos + metadata_count, metadata, value


pos, metadata, value = tree(data, 0)

print(pos, sum(metadata), value)
