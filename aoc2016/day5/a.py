import sys
import hashlib

line = sys.stdin.readline()

code = []
index = 0
for i in range(8):
    while True:
        hsh = hashlib.md5()
        idx = '%s%i' % (line, index)
        hsh.update(idx.encode('UTF8'))

        if hsh.hexdigest().startswith('00000'):
            code.append(hsh.hexdigest()[5])
            print(hsh.hexdigest())
            index += 1
            break
        index += 1

    print(index, idx, hsh.hexdigest())

print(''.join(code))
