import intcode as ic

tester = ic.Tester('Handy Haversacks')


def read_file():
    with open('input') as f:
        lines = f.read()
    return lines.split('\n')


def parse_lines(lines):
    bags = {}
    for line in lines:
        line = line.replace('.', '')
        name, content = line.split(' bags contain ')
        if name in bags:
            print('What?')
        bags[name] = {}
        inner_bags = content.split(',')
        for bag in inner_bags:
            bag = bag.strip()
            if bag.startswith('no'):
                break
            else:
                i = bag.find(' ')
                count = int(bag[:i])
                bag_name = bag[i:bag.find('bag')].strip()
                bags[name][bag_name] = count
    return bags


def is_golden(bags, bag, prefix='-'):
    if bag == 'shiny gold':
        return True
    elif len(bags[bag]) == 0:
        return False
    else:
        return any(is_golden(bags, b, prefix + '-') for b in bags[bag])


def count_golden(bags):
    count = 0

    for bag in bags.keys():
        if bag != 'shiny gold':
            count += 1 if is_golden(bags, bag) else 0

    return count


def bag_size(bags, bag, prefix='-'):
    count = 1 if bag != 'shiny gold' else 0
    for name, size in bags[bag].items():
        count += size * bag_size(bags, name, prefix + '-')

    return count


lines = """light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.""".split("\n")

bags = parse_lines(lines)
tester.test_value(count_golden(bags), 4)
tester.test_value(bag_size(bags, 'shiny gold'), 32)

lines = """shiny gold bags contain 2 dark red bags.
dark red bags contain 2 dark orange bags.
dark orange bags contain 2 dark yellow bags.
dark yellow bags contain 2 dark green bags.
dark green bags contain 2 dark blue bags.
dark blue bags contain 2 dark violet bags.
dark violet bags contain no other bags.""".split("\n")

bags = parse_lines(lines)
tester.test_value(count_golden(bags), 0)
tester.test_value(bag_size(bags, 'shiny gold'), 126)

lines = read_file()
bags = parse_lines(lines)
tester.test_value(count_golden(bags), 259, 'solution to exercise 1=%s')
tester.test_value(bag_size(bags, 'shiny gold'), 45018, 'solution to exercise 2=%s')
