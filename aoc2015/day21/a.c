#include "aoc.h"

typedef struct {
    char *name;
    uint16_t cost;
    uint8_t damage;
    uint8_t armor;
} Item;

typedef struct {
    int8_t hit_points;
    uint8_t damage;
    uint8_t armor;
} Character;

void attack(Character *attacker, Character *defender) {
    int8_t damage = attacker->damage - defender->armor;
    if (damage < 1) {
        damage = 1;
    }
    defender->hit_points -= damage;
}

Item weapons[] = {
    {.name = "Dagger", .cost = 8, .damage = 4, .armor = 0},
    {.name = "Shortsword", .cost = 10, .damage = 5, .armor = 0},
    {.name = "Warhammer", .cost = 25, .damage = 6, .armor = 0},
    {.name = "Longsword", .cost = 40, .damage = 7, .armor = 0},
    {.name = "Greataxe", .cost = 74, .damage = 8, .armor = 0},
};

Item armor[] = {
    {.name = "No Armor", .cost = 0, .damage = 0, .armor = 0},
    {.name = "Leather", .cost = 13, .damage = 0, .armor = 1},
    {.name = "Chainmail", .cost = 31, .damage = 0, .armor = 2},
    {.name = "Splintmail", .cost = 53, .damage = 0, .armor = 3},
    {.name = "Bandedmail", .cost = 75, .damage = 0, .armor = 4},
    {.name = "Platemail", .cost = 102, .damage = 0, .armor = 5},
};

Item rings[] = {
    {.name = "No Ring", .cost = 0, .damage = 0, .armor = 0},
    {.name = "Damage +1", .cost = 25, .damage = 1, .armor = 0},
    {.name = "Damage +2", .cost = 50, .damage = 2, .armor = 0},
    {.name = "Damage +3", .cost = 100, .damage = 3, .armor = 0},
    {.name = "Defense +1", .cost = 20, .damage = 0, .armor = 1},
    {.name = "Defense +2", .cost = 40, .damage = 0, .armor = 2},
    {.name = "Defense +3", .cost = 80, .damage = 0, .armor = 3},
};

void test_attack(Tester *tester) {
    Character player = (Character){8, 5, 5};
    Character boss = (Character){12, 7, 2};

    attack(&player, &boss);
    test(tester, boss.hit_points == 9, "Attack");
    attack(&boss, &player);
    test(tester, player.hit_points == 6, "");
    attack(&player, &boss);
    test(tester, boss.hit_points == 6, "");
    attack(&boss, &player);
    test(tester, player.hit_points == 4, "");
    attack(&player, &boss);
    test(tester, boss.hit_points == 3, "");
    attack(&boss, &player);
    test(tester, player.hit_points == 2, "");
    attack(&player, &boss);
    test(tester, boss.hit_points == 0, "");
}

void fight(Character *player, Character *boss) {
    Character *attacker = player;
    Character *defender = boss;
    while (player->hit_points > 0 && boss->hit_points > 0) {
        attack(attacker, defender);
        Character *temp = attacker;
        attacker = defender;
        defender = temp;
    }

    // if (player->hit_points > 0) {
    //     printf("Player wins, hit points left = %d\n", player->hit_points);
    // } else {
    //     printf("Boss wins, hit points left = %d\n", boss->hit_points);
    // }
}

void test_fight(Tester *tester) {
    Character player = (Character){8, 5, 5};
    Character boss = (Character){12, 7, 2};

    fight(&player, &boss);
    test(tester, player.hit_points == 2, "Fight");
    test(tester, boss.hit_points == 0, "");
}

uint16_t add_item(Character *player, Item item) {
    player->armor += item.armor;
    player->damage += item.damage;
    return item.cost;
}

uint16_t remove_item(Character *player, Item item) {
    player->armor -= item.armor;
    player->damage -= item.damage;
    return item.cost;
}

int main() {
    Tester tester = create_tester("RPG Simulator 20XX");
    test_attack(&tester);
    test_fight(&tester);

    uint16_t lowest_cost = 0xFFFF;
    uint16_t highest_cost = 0;
    for (int w = 0; w < 5; ++w) {
        Character player = (Character){100, 0, 0};
        uint16_t cost = 0;
        cost += add_item(&player, weapons[w]);

        for (int a = 0; a < 6; ++a) {
            cost += add_item(&player, armor[a]);

            for (int r1 = 0; r1 < 7; ++r1) {
                cost += add_item(&player, rings[r1]);

                for (int r2 = 0; r2 < 7; ++r2) {
                    if (r2 == 0 || (r2 > 0 && r1 != r2)) {
                        cost += add_item(&player, rings[r2]);

                        Character boss = (Character){109, 8, 2};
                        player.hit_points = 100;
                        fight(&player, &boss);

                        if (player.hit_points > 0 && cost < lowest_cost) {
                            lowest_cost = cost;
                            //printf("lowest cost = %d\n", lowest_cost);
                            //printf("W=%d A=%d R1=%d R2=%d\n", w, a, r1, r2);
                        } else if (boss.hit_points > 0 && cost > highest_cost) {
                            highest_cost = cost;
                            //printf("highest cost = %d\n", highest_cost);
                            //printf("W=%d A=%d R1=%d R2=%d\n", w, a, r1, r2);
                        }
                        cost -= remove_item(&player, rings[r2]);
                    }
                }
                cost -= remove_item(&player, rings[r1]);
            }
            cost -= remove_item(&player, armor[a]);
        }
        cost -= remove_item(&player, weapons[w]);
    }

    test(&tester, lowest_cost == 111, "solution to part 1");
    test(&tester, highest_cost == 188, "solution to part 2");

    test_summary(&tester);
}
