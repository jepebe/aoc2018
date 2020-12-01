import intcode as ic
import hashlib


def mine_advent_coin(secret, zeros=5):
    result = ''
    num = 0
    while not result.startswith("0" * zeros):
        chars = f'{secret}{num}'
        result = hashlib.md5(bytes(chars, 'utf-8')).hexdigest()
        num += 1
    print(result)
    return num - 1


tester = ic.Tester("adventcoins")

tester.test_value(mine_advent_coin('abcdef'), 609043)
tester.test_value(mine_advent_coin('pqrstuv'), 1048970)
tester.test_value(mine_advent_coin('ckczppom'), 117946)
tester.test_value(mine_advent_coin('ckczppom', 6), 3938038)
