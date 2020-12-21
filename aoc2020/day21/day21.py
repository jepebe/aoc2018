import intcode as ic

tester = ic.Tester('Allergen Assessment')


def read_file(postfix=''):
    with open(f'input{postfix}') as f:
        lines = f.read().splitlines(keepends=False)
    return lines


def parse(lines):
    ingredient_allergen = {}
    ingredient_hist = {}
    for line in lines:
        ingredients, allergens = line.split(' (contains ')
        ingredients = ingredients.split(' ')
        allergens = allergens.replace(')', '').split(', ')

        for ingredient in ingredients:
            if ingredient not in ingredient_hist:
                ingredient_hist[ingredient] = 0
            ingredient_hist[ingredient] += 1

            if ingredient not in ingredient_allergen:
                ingredient_allergen[ingredient] = {}
            for allergen in allergens:
                if allergen not in ingredient_allergen[ingredient]:
                    ingredient_allergen[ingredient][allergen] = 0
                ingredient_allergen[ingredient][allergen] += 1

    best_allergens = {}
    for ingredient, allergens in ingredient_allergen.items():
        for allergen, allergen_count in allergens.items():
            if allergen not in best_allergens:
                best_allergens[allergen] = 0
            if allergen_count > best_allergens[allergen]:
                best_allergens[allergen] = allergen_count

    candidates = {}
    for ingredient, allergens in ingredient_allergen.items():
        if ingredient not in candidates:
            candidates[ingredient] = []
        for allergen, allergen_count in allergens.items():
            if allergen_count == best_allergens[allergen]:
                candidates[ingredient].append(allergen)

    allergen_list = {}
    elimination_list = {c: list(a) for c, a in candidates.items() if a}
    while elimination_list:
        destroy_list = []
        for candidate, allergens in elimination_list.items():
            if len(allergens) == 1:
                allergen_list[candidate] = allergens[0]
                destroy_list.append(candidate)

        for allergen in allergen_list.values():
            for candidate, allergens in elimination_list.items():
                if allergen in allergens:
                    allergens.remove(allergen)

        for item in destroy_list:
            del elimination_list[item]

    danger = [k for k, v in sorted(allergen_list.items(), key=lambda item: item[1])]
    count = sum(ingredient_hist[ingr] for ingr in candidates if not candidates[ingr])
    return count, ','.join(danger)


lines = """mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)""".splitlines(keepends=False)

count, danger = parse(lines)
tester.test_value(count, 5)
tester.test_value(danger, 'mxmxvkd,sqjhc,fvjkl')

count, danger = parse(read_file())
tester.test_value(count, 2061, 'solution to part 1=%s')
expected = 'cdqvp,dglm,zhqjs,rbpg,xvtrfz,tgmzqjz,mfqgx,rffqhl'
tester.test_value(danger, expected, 'solution to part 2=%s')
