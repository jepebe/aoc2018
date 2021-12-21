#include "aoc.h"
#include "utils.h"

typedef struct {
    u64 die;
    u64 die_rolls;
} Dice;

typedef struct {
    u64 position;
    u64 score;
    u64 wins;
} Player;

typedef struct {
    Player p1;
    Player p2;
    u64 score;
} Players;

u64 roll(Dice *dice) {
    u64 a = (++dice->die - 1) % 100 + 1;
    u64 b = (++dice->die - 1) % 100 + 1;
    u64 c = (++dice->die - 1) % 100 + 1;
    dice->die_rolls += 3;
    return a + b + c;
}

void adjust_player_position(Player *p, s64 n) {
    p->position = ((n + p->position - 1) % 10) + 1;
}

Players play(u64 start_1, u64 start_2) {
    Players p = {0};
    Dice dice = {0};
    p.p1.position = start_1;
    p.p2.position = start_2;

    while (true) {
        adjust_player_position(&p.p1, roll(&dice));
        p.p1.score += p.p1.position;
        if (p.p1.score >= 1000) {
            p.score = p.p2.score * dice.die_rolls;
            break;
        }
        adjust_player_position(&p.p2, roll(&dice));
        p.p2.score += p.p2.position;
        if (p.p2.score >= 1000) {
            p.score = p.p1.score * dice.die_rolls;
            break;
        }
    }
    return p;
}

typedef struct {
    u64 p1[11][11][21][21];
    u64 p2[11][11][21][21];
} Memo;

bool has_cached_value(Memo *memo, Players *p) {
    bool p1 = memo->p1[p->p1.position][p->p2.position][p->p1.score][p->p2.score] == 0;
    bool p2 = memo->p2[p->p1.position][p->p2.position][p->p1.score][p->p2.score] == 0;
    return !(p1 && p2);
}

u64 cached_p1_wins(Memo *memo, Players *p) {
    return memo->p1[p->p1.position][p->p2.position][p->p1.score][p->p2.score];
}

u64 cached_p2_wins(Memo *memo, Players *p) {
    return memo->p2[p->p1.position][p->p2.position][p->p1.score][p->p2.score];
}

void memoize(Memo *memo, Players *p, u64 p1_wins, u64 p2_wins) {
    memo->p1[p->p1.position][p->p2.position][p->p1.score][p->p2.score] = p1_wins;
    memo->p2[p->p1.position][p->p2.position][p->p1.score][p->p2.score] = p2_wins;
}

void dirac(Players *p, Memo *memo, u8 target) {
    int win_multiplier[] = {0, 0, 0, 1, 3, 6, 7, 6, 3, 1};

    u64 p1_wins = 0;
    u64 p2_wins = 0;

    if (has_cached_value(memo, p)) {
        p1_wins = cached_p1_wins(memo, p);
        p2_wins = cached_p2_wins(memo, p);
    } else {
        for (int p1 = 3; p1 <= 9; ++p1) {
            u64 old_p1 = p->p1.position;
            adjust_player_position(&p->p1, p1);
            p->p1.score += p->p1.position;

            if (p->p1.score >= target) {
                p1_wins += win_multiplier[p1];
            } else {
                for (int p2 = 3; p2 <= 9; ++p2) {
                    u64 old_p2 = p->p2.position;
                    adjust_player_position(&p->p2, p2);
                    p->p2.score += p->p2.position;

                    u64 multiplier = win_multiplier[p1] * win_multiplier[p2];

                    if (p->p2.score >= target) {
                        p2_wins += multiplier;
                    } else {
                        dirac(p, memo, target);
                        p1_wins += p->p1.wins * multiplier;
                        p2_wins += p->p2.wins * multiplier;
                    }

                    p->p2.score -= p->p2.position;
                    p->p2.position = old_p2;
                }
            }

            p->p1.score -= p->p1.position;
            p->p1.position = old_p1;
        }
        memoize(memo, p, p1_wins, p2_wins);
    }
    p->p1.wins = p1_wins;
    p->p2.wins = p2_wins;
}

Players play_dirac(u64 start_1, u64 start_2) {
    Memo *memo = malloc(sizeof(Memo));
    memset(memo, 0, sizeof(Memo));

    u8 target = 21;
    Players p = {0};
    p.p1.position = start_1;
    p.p2.position = start_2;
    dirac(&p, memo, target);
    p.score = p.p1.wins > p.p2.wins ? p.p1.wins : p.p2.wins;

    free(memo);
    return p;
}

void test_examples(Tester *tester) {
    test_section("Examples Part 1");

    Players p = play(4, 8);
    testi(tester, p.p1.score, 1000, "");
    testi(tester, p.p2.score, 745, "");
    testi(tester, p.score, 739785, "");

    test_section("Examples Part 2");

    p = play_dirac(4, 8);

    test_u64(tester, p.p1.wins, 444356092776315, "");
    test_u64(tester, p.p2.wins, 341960390180808, "");
    test_u64(tester, p.score, 444356092776315, "");
}

int main() {
    Tester tester = create_tester("Dirac Dice");
    test_examples(&tester);

    test_section("Solutions");

    Players p = play(10, 1);

    testi(&tester, p.score, 920079, "solution to part 1");

    p = play_dirac(10, 1);
    test_u64(&tester, p.score, 56852759190649, "solution to part 2");

    return test_summary(&tester);
}
