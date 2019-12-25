from itertools import product

import intcode as ic


def prepare(sm):
    steps = [
        'east',
        'take antenna',
        'west',
        'north',
        'take weather machine',
        'north',
        'take klein bottle',
        'east',
        'take spool of cat6',
        'east',
        'south',
        'take mug',
        'north',
        'north',
        'west',
        'north',
        'take cake',
        'south',
        'east',
        'east',
        'north',
        'north',
        'take tambourine',
        'south',
        'south',
        'south',
        'take shell',
        'north',
        'west',
        'south',
        'west',
        'south',
        'south',
        'inv'
    ]

    for step in steps:
        for c in step:
            ic.add_input(sm, ord(c))
        ic.add_input(sm, ord('\n'))
        ic.run_state_machine(sm)
    # ic.print_output(sm)
    ic.flush_output(sm)


def take(sm, item):
    action = f'take {item}'
    for c in action:
        ic.add_input(sm, ord(c))
    ic.add_input(sm, ord('\n'))
    ic.run_state_machine(sm)


def drop(sm, item):
    action = f'drop {item}'
    for c in action:
        ic.add_input(sm, ord(c))
    ic.add_input(sm, ord('\n'))
    ic.run_state_machine(sm)


def go(sm, direction):
    for c in direction:
        ic.add_input(sm, ord(c))
    ic.add_input(sm, ord('\n'))
    ic.run_state_machine(sm)


def try_inventory(sm, items, inventory):
    pick_up_later = []
    for item in items:
        if item not in inventory:
            pick_up_later.append(item)
            drop(sm, item)

    go(sm, 'east')

    for item in pick_up_later:
        take(sm, item)


def find_correct_inventory(sm):
    items = [
        'shell',
        'klein bottle',
        'tambourine',
        'weather machine',
        'antenna',
        'spool of cat6',
        'mug',
        'cake',
    ]

    for combo in product([True, False], repeat=8):
        inventory = [i for i, s in zip(items, combo) if s]
        try_inventory(sm, items, inventory)

        if not ic.is_running(sm):
            print(inventory)
            ic.print_output(sm)
            break
        ic.flush_output(sm)


sm = ic.load_state_machine('input')
prepare(sm)
find_correct_inventory(sm)


ic.print_output(sm)
# ic.terminal(sm)

# weather machine
# antenna
# spool of cat6
# mug

# 805307408
