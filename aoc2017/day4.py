import itertools


def passphrase_is_valid(line):
    words = line.split()
    valid_words = []
    for word in words:
        if word in valid_words:
            return False
        else:
            valid_words.append(word)
    return True


def passphrase_is_valid_wo_anagram(line):
    words = line.split()
    used_words = []
    for word in words:
        if word in used_words:
            return False
        else:
            perm = itertools.permutations(word, len(word))
            perm = [''.join(p) for p in perm]
            used_words.extend(perm)
    return True


def count(exp):
    return len(list(exp))


if __name__ == '__main__':

    assert passphrase_is_valid('aa bb cc dd ee')
    assert not passphrase_is_valid('aa bb cc dd aa')
    assert passphrase_is_valid('aa bb cc dd aaa')

    assert passphrase_is_valid_wo_anagram('abcde fghij')
    assert not passphrase_is_valid_wo_anagram('abcde xyz ecdab')
    assert passphrase_is_valid_wo_anagram('a ab abc abd abf abj')
    assert passphrase_is_valid_wo_anagram('iiii oiii ooii oooi oooo')
    assert not passphrase_is_valid_wo_anagram('oiii ioii iioi iiio')

    with open('day4.txt', 'r') as f:
        data = f.read()

    lines = data.splitlines()

    print(count(line for line in lines if passphrase_is_valid(line)))
    print(count(line for line in lines if passphrase_is_valid_wo_anagram(line)))
