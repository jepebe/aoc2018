from dataclasses import dataclass
from typing import List

import intcode as ic


@dataclass
class Ingredient:
    capacity: int
    durability: int
    flavor: int
    texture: int
    calories: int


def mix(ingredients: List[Ingredient], ratio):
    product = Ingredient(0, 0, 0, 0, 0)
    for i, ingredient in enumerate(ingredients):
        product.capacity += ratio[i] * ingredient.capacity
        product.durability += ratio[i] * ingredient.durability
        product.flavor += ratio[i] * ingredient.flavor
        product.texture += ratio[i] * ingredient.texture
        product.calories += ratio[i] * ingredient.calories

    if product.capacity < 0:
        product.capacity = 0
    if product.durability < 0:
        product.durability = 0
    if product.flavor < 0:
        product.flavor = 0
    if product.texture < 0:
        product.texture = 0

    prod = product.capacity * product.durability * product.flavor * product.texture
    return prod, product.calories


def ratio(length=4, total_sum=100):
    if length == 1:
        yield total_sum,
    else:
        for value in range(total_sum + 1):
            for permutation in ratio(length - 1, total_sum - value):
                yield (value,) + permutation


def find_max_product(ingredients, calorie_goal=500):
    max_product = 0
    max_calorie_product = 0
    for r in ratio():
        p, cal = mix(ingredients, r)
        if p > max_product:
            max_product = p
        if cal == calorie_goal and p > max_calorie_product:
            max_calorie_product = p

    return max_product, max_calorie_product


tester = ic.Tester("Science for Hungry People")

butterscotch = Ingredient(-1, -2, 6, 3, 8)
cinnamon = Ingredient(2, 3, -2, -1, 3)

ingredients = [butterscotch, cinnamon]

tester.test_value(mix(ingredients, [44, 56])[0], 62842880)

"""
Sprinkles: capacity 2, durability 0, flavor -2, texture 0, calories 3
Butterscotch: capacity 0, durability 5, flavor -3, texture 0, calories 3
Chocolate: capacity 0, durability 0, flavor 5, texture -1, calories 8
Candy: capacity 0, durability -1, flavor 0, texture 5, calories 8
"""

sprinkles = Ingredient(2, 0, -2, 0, 3)
butterscotch = Ingredient(0, 5, -3, 0, 3)
chocolate = Ingredient(0, 0, 5, -1, 8)
candy = Ingredient(0, -1, 0, 5, 8)

ingredients = [sprinkles, butterscotch, chocolate, candy]
max_product, max_calorie_product = find_max_product(ingredients)
tester.test_value(max_product, 21367368, 'solution to exercise 1 = %s')
tester.test_value(max_calorie_product, 1766400, 'solution to exercise 2 = %s')
