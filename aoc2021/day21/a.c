#include "aoc.h"
#include "dict.h"
#include "utils.h"
#include <stdlib.h>

typedef struct {
    u64 p1;
    u64 p1_score;
    u64 p1_wins;
    u64 p2;
    u64 p2_score;
    u64 p2_wins;
    u64 die;
    u64 die_rolls;
    u64 score;
} Players;

u64 roll(Players *p) {
    u64 a = (++p->die - 1) % 100 + 1;
    u64 b = (++p->die - 1) % 100 + 1;
    u64 c = (++p->die - 1) % 100 + 1;
    p->die_rolls += 3;
    return a + b + c;
}

Players play(u64 start_1, u64 start_2) {
    Players p = {0};
    p.p1 = start_1;
    p.p2 = start_2;

    while (true) {
        p.p1 += roll(&p);
        p.p1_score += ((p.p1 - 1) % 10) + 1;
        if (p.p1_score >= 1000) {
            p.score = p.p2_score * p.die_rolls;
            break;
        }
        p.p2 += roll(&p);
        p.p2_score += ((p.p2 - 1) % 10) + 1;
        if (p.p2_score >= 1000) {
            p.score = p.p1_score * p.die_rolls;
            break;
        }
    }
    return p;
}

typedef struct {
    u64 p1[11][11][21][21];
    u64 p2[11][11][21][21];
} Memo;

// void clear(Memo *memo) {
//     for (int i = 0; i < 11; ++i) {
//         for (int j = 0; j < 11; ++j) {
//             for (int k = 0; k < 21; ++k) {
//                 for (int m = 0; m < 21; ++m) {
//                     memo->p1[i][j][k][m] = 0;
//                     memo->p1[i][j][k][m] = 0;
//                 }
//             }
//         }
//     }
// }

u64 indexify(u64 p) {
    return ((p - 1) % 10) + 1;
}

bool has_cached_value(Memo *memo, Players *p) {
    int p1i = indexify(p->p1);
    int p2i = indexify(p->p2);
    bool p1 = memo->p1[p1i][p2i][p->p1_score][p->p2_score] > 0;
    bool p2 = memo->p2[p1i][p2i][p->p1_score][p->p2_score] > 0;
    return p1 && p2;
}

u64 cached_p1_wins(Memo *memo, Players *p) {
    int p1i = indexify(p->p1);
    int p2i = indexify(p->p2);
    return memo->p1[p1i][p2i][p->p1_score][p->p2_score];
}

u64 cached_p2_wins(Memo *memo, Players *p) {
    int p1i = indexify(p->p1);
    int p2i = indexify(p->p2);
    return memo->p2[p1i][p2i][p->p1_score][p->p2_score];
}

void memoize(Memo *memo, Players *p, u64 p1_wins, u64 p2_wins) {
    int p1i = indexify(p->p1);
    int p2i = indexify(p->p2);
    memo->p1[p1i][p2i][p->p1_score][p->p2_score] = p1_wins;
    memo->p2[p1i][p2i][p->p1_score][p->p2_score] = p2_wins;
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
            p->p1 += p1;
            p->p1_score += indexify(p->p1);

            if (p->p1_score >= target) {
                p1_wins += win_multiplier[p1];
            } else {
                for (int p2 = 3; p2 <= 9; ++p2) {
                    p->p2 += p2;
                    p->p2_score += indexify(p->p2);

                    u64 multiplier = win_multiplier[p1] * win_multiplier[p2];

                    if (p->p2_score >= target) {
                        p2_wins += multiplier;
                    } else {
                        dirac(p, memo, target);
                        p1_wins += p->p1_wins * multiplier;
                        p2_wins += p->p2_wins * multiplier;
                    }

                    p->p2_score -= indexify(p->p2);
                    p->p2 -= p2;
                }
            }

            p->p1_score -= indexify(p->p1);
            p->p1 -= p1;
        }
        memoize(memo, p, p1_wins, p2_wins);
    }
    p->p1_wins = p1_wins;
    p->p2_wins = p2_wins;
}

Players play_dirac(u64 start_1, u64 start_2) {
    Memo *memo = malloc(sizeof(Memo));
    memset(memo, 0, sizeof(Memo));

    u8 target = 21;
    Players p = {0};
    p.p1 = start_1;
    p.p2 = start_2;
    dirac(&p, memo, target);
    p.score = p.p1_wins > p.p2_wins ? p.p1_wins : p.p2_wins;

    free(memo);
    return p;
}

void test_examples(Tester *tester) {
    test_section("Examples Part 1");

    Players p = play(4, 8);
    testi(tester, p.p1_score, 1000, "");
    testi(tester, p.p2_score, 745, "");
    testi(tester, p.die_rolls, 993, "");
    testi(tester, p.score, 739785, "");

    test_section("Examples Part 2");

    p = play_dirac(4, 8);

    test_u64(tester, p.p1_wins, 444356092776315, "");
    test_u64(tester, p.p2_wins, 341960390180808, "");
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
