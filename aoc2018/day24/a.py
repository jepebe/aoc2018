import sys
import re
from math import ceil

unit_pattern = re.compile('([0-9]+) units each with ([0-9]+) hit points( [(][a-z,; ]+[)])?'
                          ' with an attack that does ([0-9]+) (radiation|fire|slashing|bludgeoning|cold)'
                          ' damage at initiative ([0-9]+)')


def red(text):
    return f'\033[31m{text}\033[0m'


def green(text):
    return f'\033[92m{text}\033[0m'


def parse_armies(lines):
    armies = []
    group_type = None
    group_count = 0
    for line in lines:
        if line.startswith('Immune') or line.startswith('Infection'):
            if line.startswith('Immune'):
                group_type = 'immune'
                group_count = 1
            else:
                group_type = 'infection'
                group_count = 1
            armies.append([])
        elif line.strip() == '':
            continue
        else:
            match = unit_pattern.match(line.strip())
            unit_count = int(match.group(1))
            hit_points = int(match.group(2))
            attack = int(match.group(4))
            attack_type = match.group(5)
            initiative = int(match.group(6))

            group = Group(unit_count, hit_points, attack, attack_type, initiative)
            group.type = group_type
            group.number = group_count
            group_count += 1

            atr_grp = match.group(3)

            if atr_grp:
                attributes = atr_grp[atr_grp.index('(') + 1:atr_grp.index(')')]
                attributes = attributes.split(';')
                for attribute in attributes:
                    attribute = attribute.strip()
                    if attribute.startswith('weak to'):
                        attribute_list = group.weaknesses
                        attribute = attribute[8:]
                    elif attribute.startswith('immune to'):
                        attribute_list = group.immunities
                        attribute = attribute[10:]
                    else:
                        print('What?', attribute)

                    for atr in attribute.split(', '):
                        attribute_list.append(atr.strip())

            armies[-1].append(group)

    return armies


class Group(object):
    def __init__(self, units, hp, attack, attack_type, initiative):
        self._units = units
        self.units = units
        self._hp = hp
        self.attack_power = attack
        self.initiative = initiative
        self.attack_type = attack_type
        self.immunities = []
        self.weaknesses = []
        self.type = None
        self.number = 0
        self.boost = 0

    def reset(self):
        self.units = self._units

    @property
    def hp(self):
        return self.units * self._hp

    @property
    def effective_power(self):
        return self.units * (self.attack_power + self.boost)

    def attack_check(self, damage, attack_type):
        if attack_type in self.weaknesses:
            damage *= 2
        elif attack_type in self.immunities:
            damage = 0
        return damage

    def attack(self, damage, attack_type):
        damage = self.attack_check(damage, attack_type)
        rest = self.hp - damage
        new_units = ceil(rest / self._hp)
        loss = self.units - new_units
        self.units = new_units
        return loss

    @property
    def is_alive(self):
        return self.units > 0

    @property
    def name(self):
        return f'{self.type}#{self.number}'

    def __repr__(self):
        state = '\u2020' if not self.is_alive else '\u203b'
        return f'{self.name} ({self.units}) {state}'

    def __lt__(self, other):
        if self.effective_power == other.effective_power:
            return self.initiative < other.initiative
        return self.effective_power < other.effective_power


def alive(groups):
    return sum(1 for x in groups if x.is_alive)


def battle(immune, infection):
    total_loss = 1
    while alive(immune) > 0 and alive(infection) > 0 and total_loss > 0:
        total_loss = 0
        groups = list(reversed([grp for grp in sorted(immune + infection) if grp.is_alive]))

        attackers = {}
        picked = []
        for group in groups[:]:
            ep = group.effective_power
            at = group.attack_type
            gt = group.type
            candidates = sorted([(x.attack_check(ep, at), x) for x in groups if x.type != gt and x not in picked])

            if candidates:
                attackers[group] = candidates[-1][1]
                picked.append(candidates[-1][1])

        attack_order = sorted(attackers, key=lambda x: -x.initiative)

        for attacker in attack_order:
            defender = attackers[attacker]
            if attacker.is_alive and defender.is_alive:
                loss = defender.attack(attacker.effective_power, attacker.attack_type)
                total_loss += loss


if __name__ == '__main__':
    lines = sys.stdin.readlines()
    immune, infection = parse_armies(lines)

    immune_score = 0
    infection_score = 1
    boost = 0
    while immune_score <= 0 or infection_score > 0:
        for grp in immune:
            grp.boost = boost

        battle(immune, infection)

        immune_score = sum(x.units for x in immune if x.is_alive)
        infection_score = sum(x.units for x in infection if x.is_alive)

        if immune_score > 0 >= infection_score:
            print(green(f'Immune score {immune_score} with a boost of {boost}'))
            break
        else:
            print(red(f'Immune score {immune_score} with a boost of {boost}'))

        if boost == 0:
            print(green(f'Puzzle 1 score {infection_score} for boost = 0'))

        for grp in immune + infection:
            grp.reset()
        boost += 1

    # puzzle 1 infection_score = 22996
    # puzzle 2 immune_score = 4327
