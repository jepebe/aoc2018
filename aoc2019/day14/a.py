from collections import defaultdict

from intcode import Tester


class Chemical(object):
    def __init__(self, amount, name):
        self.amount = amount
        self.name = name
        self.ingredients = {}

    def add_ingredient(self, name, amount):
        self.ingredients[name] = amount

    def _calculate_multiplier(self, amount):
        if amount <= self.amount:
            multiplier = 1
        else:
            multiplier = amount // self.amount
            if amount % self.amount > 0:
                multiplier += 1
        return multiplier

    def is_ore_based(self):
        return 'ORE' in self.ingredients

    def ore_cost(self):
        return self.ingredients['ORE']

    def get_ore_cost(self, reactions, surplus, costs, amount):
        if amount >= surplus[self.name]:
            amount -= surplus[self.name]
            surplus[self.name] = 0
        elif surplus[self.name] > amount:
            surplus[self.name] -= amount
            return 0

        multiplier = self._calculate_multiplier(amount)

        if self.is_ore_based():
            cost = self.ore_cost() * multiplier
            costs[self.name] = cost
        else:
            cost = 0
            for n, a in self.ingredients.items():
                cost += reactions[n].get_ore_cost(reactions, surplus, costs, a * multiplier)
            costs[self.name] = cost

        surplus[self.name] += self.amount * multiplier - amount
        return cost

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        ing = ' '.join([f'{n} {a}' for n, a in self.ingredients.items()])
        return f'{ing} => {self.name} {self.amount}'

    def __repr__(self):
        return str(self)


def load_reactions(filename):
    with open(filename) as f:
        lines = f.readlines()

    graph = {}
    for line in lines:
        ingredients, result = line.strip().split('=>')
        amount, name = result.strip().split(' ')
        result = Chemical(int(amount), name)

        graph[name] = result

        for ingredient in ingredients.split(','):
            amount, name = ingredient.strip().split(' ')
            result.add_ingredient(name, int(amount))

    return graph


def calculate_total_ore_cost(reactions, name='FUEL'):
    surplus = defaultdict(int)
    costs = defaultdict(int)

    cost = reactions[name].get_ore_cost(reactions, surplus, costs, 1)

    return cost


def find_ore_production(reactions, limit):
    cost = 0
    i = 1
    while cost < limit:
        i *= 2
        cost = reactions['FUEL'].get_ore_cost(reactions, defaultdict(int), defaultdict(int), int(i))

    max_i = i
    min_i = 0
    i = max_i
    while cost != limit:
        if cost > limit:
            max_i = i
        elif cost < limit:
            min_i = i

        i = int(min_i + (max_i - min_i) / 2)
        cost = reactions['FUEL'].get_ore_cost(reactions, defaultdict(int), defaultdict(int), int(i))

        if max_i - min_i == 1:
            return i


tester = Tester('fuel')

reactions = load_reactions('test0')
tester.test_value(calculate_total_ore_cost(reactions), 36)

reactions = load_reactions('test1')
tester.test_value(calculate_total_ore_cost(reactions), 31)

reactions = load_reactions('test2')
tester.test_value(calculate_total_ore_cost(reactions), 165)

reactions = load_reactions('test3')
tester.test_value(calculate_total_ore_cost(reactions), 13312)

reactions = load_reactions('test4')
tester.test_value(calculate_total_ore_cost(reactions), 180697)

reactions = load_reactions('test5')
tester.test_value(calculate_total_ore_cost(reactions), 2210736)

reactions = load_reactions('input')
tester.test_value(calculate_total_ore_cost(reactions), 907302)

reactions = load_reactions('test3')
tester.test_value(find_ore_production(reactions, 1000000000000), 82892753)

reactions = load_reactions('test4')
tester.test_value(find_ore_production(reactions, 1000000000000), 5586022)

reactions = load_reactions('test5')
tester.test_value(find_ore_production(reactions, 1000000000000), 460664)

reactions = load_reactions('input')
tester.test_value(find_ore_production(reactions, 1000000000000), 1670299)

tester.summary()
