import sys
import hashlib

line = sys.stdin.readline()

code = ['.'] * 8
index = 0
for i in range(8):
    while True:
        hsh = hashlib.md5()
        idx = '%s%i' % (line, index)
        hsh.update(idx.encode('UTF8'))

        if hsh.hexdigest().startswith('00000'):
            code_index = int(hsh.hexdigest()[5], base=16)
            code_value = hsh.hexdigest()[6]
            if code_index < 8 and code[code_index] == '.':
                code[code_index] = code_value
                print(hsh.hexdigest())
                index += 1
                break

        index += 1

    print(index, idx, hsh.hexdigest())

print(''.join(code))
