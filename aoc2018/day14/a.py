def find_score(recipe_count, match):
    machine = {
        'scores': [3, 7],
        'elves': [0, 1],
    }

    for i in range(recipe_count - 2 + 10):
        elv_pos_1 = machine['elves'][0]
        elv_pos_2 = machine['elves'][1]
        elv_1 = machine['scores'][elv_pos_1]
        elv_2 = machine['scores'][elv_pos_2]
        score = elv_1 + elv_2

        if score >= 10:
            sc1, sc2 = map(int, str(score)[0:2])
            machine['scores'].append(sc1)
            machine['scores'].append(sc2)
        else:
            machine['scores'].append(score)

        score_count = len(machine['scores'])
        machine['elves'][0] = (elv_pos_1 + 1 + elv_1) % score_count
        machine['elves'][1] = (elv_pos_2 + 1 + elv_2) % score_count

    index = ''.join(map(str, machine['scores'])).index(match)
    values = map(str, machine['scores'][recipe_count:recipe_count + 10])

    return ''.join(values), index


print(find_score(recipe_count=9, match='51589'), '5158916779')
print(find_score(recipe_count=5, match='01245'), '0124515891')
print(find_score(recipe_count=18, match='92510'), '9251071085')
print(find_score(recipe_count=2018, match='59414'), '5941429882')
print(find_score(recipe_count=540391, match='1474315445'), '1474315445')
print(find_score(recipe_count=20278132, match='540391'), '1474315445')

