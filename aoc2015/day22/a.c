#include "aoc.h"
#include <stdint.h>

typedef struct {
    uint8_t shield;
    uint8_t poison;
    uint8_t recharge;
} Effects;

typedef struct {
    int8_t hit_points;
    int16_t mana;
    uint8_t damage;
    uint8_t armor;
    int16_t mana_spent;
} Character;

typedef struct {
    Character player;
    Character boss;
    Effects effects;
    bool hard_mode;
} Game;

void apply_effects(Game *game) {
    game->player.armor = 0;

    if (game->effects.poison > 0) {
        game->boss.hit_points -= 3;
        game->effects.poison--;
    }

    if (game->effects.shield > 0) {
        game->player.armor = 7;
        game->effects.shield--;
    }

    if (game->effects.recharge > 0) {
        game->player.mana += 101;
        game->effects.recharge--;
    }
}

void boss_attack(Game *game) {
    int8_t damage = game->boss.damage - game->player.armor;
    if (damage < 1) {
        damage = 1;
    }
    game->player.hit_points -= damage;
}

void cast_poison(Game *game) {
    game->player.mana -= 173;
    game->player.mana_spent += 173;
    game->effects.poison = 6;
}

void cast_magic_missile(Game *game) {
    game->player.mana -= 53;
    game->player.mana_spent += 53;
    game->boss.hit_points -= 4;
}

void cast_drain(Game *game) {
    game->player.mana -= 73;
    game->player.mana_spent += 73;
    game->player.hit_points += 2;
    game->boss.hit_points -= 2;
}

void cast_recharge(Game *game) {
    game->player.mana -= 229;
    game->player.mana_spent += 229;
    game->effects.recharge = 5;
}

void cast_shield(Game *game) {
    game->player.mana -= 113;
    game->player.mana_spent += 113;
    game->effects.shield = 6;
}

void test_attack_1(Tester *tester) {
    Game game;
    game.player = (Character){10, 250, 0, 0, 0};
    game.boss = (Character){13, 0, 8, 0, 0};
    game.effects = (Effects){0, 0, 0};
    game.hard_mode = false;

    cast_poison(&game);

    apply_effects(&game);
    boss_attack(&game);
    test(tester, game.boss.hit_points == 10, "Attack 1");
    test(tester, game.effects.poison == 5, "");
    test(tester, game.player.mana == 77, "");
    test(tester, game.player.hit_points == 2, "");

    apply_effects(&game);
    cast_magic_missile(&game);
    test(tester, game.boss.hit_points == 3, "");
    test(tester, game.effects.poison == 4, "");
    test(tester, game.player.mana == 24, "");
    test(tester, game.player.hit_points == 2, "");

    apply_effects(&game);
    test(tester, game.boss.hit_points == 0, "");
    test(tester, game.player.mana_spent == 226, "");
}

void test_attack_2(Tester *tester) {
    Game game;
    game.player = (Character){10, 250, 0, 0, 0};
    game.boss = (Character){14, 0, 8, 0, 0};
    game.effects = (Effects){0, 0, 0};
    game.hard_mode = false;

    cast_recharge(&game);
    test(tester, game.player.mana == 21, "");

    apply_effects(&game);
    boss_attack(&game);
    test(tester, game.boss.hit_points == 14, "Attack 2");
    test(tester, game.effects.recharge == 4, "");
    test(tester, game.player.mana == 122, "");
    test(tester, game.player.hit_points == 2, "");

    apply_effects(&game);
    cast_shield(&game);

    apply_effects(&game);
    boss_attack(&game);
    testi(tester, game.boss.hit_points, 14, "Boss HP");
    testi(tester, game.effects.recharge, 2, "Recharge timer");
    testi(tester, game.effects.shield, 5, "Shield timer");
    testi(tester, game.effects.poison, 0, "Poison timer");
    testi(tester, game.player.mana, 211, "Mana");
    testi(tester, game.player.hit_points, 1, "Player HP");
    testi(tester, game.player.armor, 7, "Player Armor");

    apply_effects(&game);
    cast_drain(&game);

    apply_effects(&game);
    boss_attack(&game);
    testi(tester, game.boss.hit_points, 12, "Boss HP");
    testi(tester, game.effects.recharge, 0, "Recharge timer");
    testi(tester, game.effects.shield, 3, "Shield timer");
    testi(tester, game.effects.poison, 0, "Poison timer");
    testi(tester, game.player.mana, 340, "Mana");
    testi(tester, game.player.hit_points, 2, "Player HP");
    testi(tester, game.player.armor, 7, "Player Armor");

    apply_effects(&game);
    cast_poison(&game);

    apply_effects(&game);
    boss_attack(&game);
    testi(tester, game.boss.hit_points, 9, "Boss HP");
    testi(tester, game.effects.recharge, 0, "Recharge timer");
    testi(tester, game.effects.shield, 1, "Shield timer");
    testi(tester, game.effects.poison, 5, "Poison timer");
    testi(tester, game.player.mana, 167, "Mana");
    testi(tester, game.player.hit_points, 1, "Player HP");
    testi(tester, game.player.armor, 7, "Player Armor");

    apply_effects(&game);
    cast_magic_missile(&game);
    testi(tester, game.boss.hit_points, 2, "Boss HP");
    testi(tester, game.effects.shield, 0, "Shield timer");

    apply_effects(&game);
    // boss is dead
    testi(tester, game.boss.hit_points, -1, "Boss HP");
    testi(tester, game.effects.recharge, 0, "Recharge timer");
    testi(tester, game.effects.shield, 0, "Shield timer");
    testi(tester, game.effects.poison, 3, "Poison timer");
    testi(tester, game.player.mana, 114, "Mana");
    testi(tester, game.player.hit_points, 1, "Player HP");
    testi(tester, game.player.armor, 0, "Player Armor");
    testi(tester, game.player.mana_spent, 641, "Mana spent");
}

bool can_cast_magic_missile(Game *game) {
    return game->player.mana >= 53;
}

bool can_cast_drain(Game *game) {
    return game->player.mana >= 73;
}

bool can_cast_shield(Game *game) {
    return game->player.mana >= 113 && (game->effects.shield == 0);
}

bool can_cast_poison(Game *game) {
    return game->player.mana >= 173 && (game->effects.poison == 0);
}

bool can_cast_recharge(Game *game) {
    return game->player.mana >= 229 && (game->effects.recharge == 0);
}

bool cannot_cast(Game *game) {
    return game->player.mana < 53;
}

int fight(Game game, int min_spent);

int boss_fight(Game *game, int min_spent) {
    apply_effects(game);

    int spent = game->player.mana_spent;
    if (game->boss.hit_points > 0) {
        boss_attack(game);
        spent = fight(*game, min_spent);
    }

    if (spent < min_spent) {
        min_spent = spent;
    }
    return min_spent;
}

int fight(Game game, int min_spent) {
    if (game.hard_mode) {
        game.player.hit_points--;
    }

    if (game.player.mana_spent >= min_spent) {
        return 0xFFFF;
    }

    if (game.player.hit_points <= 0) {
        return 0xFFFF;
    }

    if (cannot_cast(&game)) {
        return 0xFFFF;
    }

    apply_effects(&game);

    if (game.boss.hit_points <= 0) {
        return game.player.mana_spent;
    }

    if (can_cast_magic_missile(&game)) {
        // copy
        Game gc = game;
        cast_magic_missile(&gc);
        min_spent = boss_fight(&gc, min_spent);
    }

    if (can_cast_drain(&game)) {
        // copy
        Game gc = game;
        cast_drain(&gc);
        min_spent = boss_fight(&gc, min_spent);
    }

    if (can_cast_shield(&game)) {
        // copy
        Game gc = game;
        cast_shield(&gc);
        min_spent = boss_fight(&gc, min_spent);
    }

    if (can_cast_poison(&game)) {
        // copy
        Game gc = game;
        cast_poison(&gc);
        min_spent = boss_fight(&gc, min_spent);
    }

    if (can_cast_recharge(&game)) {
        // copy
        Game gc = game;
        cast_recharge(&gc);
        min_spent = boss_fight(&gc, min_spent);
    }

    return min_spent;
}

void test_fight_1(Tester *tester) {
    Game game;
    game.player = (Character){10, 250, 0, 0, 0};
    game.boss = (Character){13, 0, 8, 0, 0};
    game.effects = (Effects){0, 0, 0};
    game.hard_mode = false;

    int min_mana = fight(game, 0xFFFF);
    testi(tester, min_mana, 226, "min mana spent");
}

void test_fight_2(Tester *tester) {
    Game game;
    game.player = (Character){10, 250, 0, 0, 0};
    game.boss = (Character){14, 0, 8, 0, 0};
    game.effects = (Effects){0, 0, 0};
    game.hard_mode = false;

    int min_mana = fight(game, 0xFFFF);
    testi(tester, min_mana, 641, "min mana spent");
}

int main() {
    Tester tester = create_tester("Wizard Simulator 20XX");
    test_attack_1(&tester);
    test_attack_2(&tester);
    test_fight_1(&tester);
    test_fight_2(&tester);

    Game game;
    game.player = (Character){50, 500, 0, 0, 0};
    game.boss = (Character){51, 0, 9, 0, 0};
    game.effects = (Effects){0, 0, 0};
    game.hard_mode = false;

    int min_mana = fight(game, 0xFFFF);
    testi(&tester, min_mana, 900, "solution to part 1");

    game.hard_mode = true;
    min_mana = fight(game, 0xFFFF);
    testi(&tester, min_mana, 1216, "solution to part 2");

    test_summary(&tester);
}
