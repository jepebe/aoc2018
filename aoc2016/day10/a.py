import sys
import re

lines = sys.stdin.readlines()

input = re.compile('value ([0-9]+) goes to ((bot|output) [0-9]+)')
rule = re.compile('(bot [0-9]+) gives low to ((bot|output) [0-9]+) and high to ((bot|output) [0-9]+)')


def create_bot(bots, bot):
    bots[bot] = {
        'id': bot,
        'chips': [],
        'low': None,
        'high': None
    }


def give_chip_to_bot(bots, bot, chip):
    if bot not in bots:
        create_bot(bots, bot)

    bots[bot]['chips'].append(chip)


def add_rule_to_bot(bots, bot, low_bot, high_bot):
    if bot not in bots:
        create_bot(bots, bot)

    if low_bot not in bots:
        create_bot(bots, low_bot)

    if high_bot not in bots:
        create_bot(bots, high_bot)

    bots[bot]['low'] = low_bot
    bots[bot]['high'] = high_bot


def is_bot(bot):
    # print('->', bot, bot['low'] is None and bot['high'] is None)
    return bot['low'] is not None and bot['high'] is not None


bots = {}

for line in lines:
    if line.startswith('value'):
        match = input.match(line)
        chip = match.group(1)
        bot = match.group(2)
        give_chip_to_bot(bots, bot, int(chip))
    elif line.startswith('bot'):
        match = rule.match(line)
        bot = match.group(1)
        low_bot = match.group(2)
        high_bot = match.group(4)

        add_rule_to_bot(bots, bot, low_bot, high_bot)

#print(bots)

transactions = 1

while transactions > 0:
    transactions = 0
    for bot in bots.values():
        if is_bot(bot) and len(bot['chips']) == 2:
            chips = list(sorted(bot['chips']))
            bot['chips'] = []

            if chips[0] == 2 and chips[1] == 5:
                print(bot, chips[0], chips[1])

            if chips[0] == 17 and chips[1] == 61:
                print(bot, chips[0], chips[1])

            give_chip_to_bot(bots, bot['low'], chips[0])
            give_chip_to_bot(bots, bot['high'], chips[1])
            transactions += 1

#print(bots)

print(bots['output 0']['chips'][0] * bots['output 1']['chips'][0] * bots['output 2']['chips'][0])
