#include "aoc.h"
#include "dict.h"
#include "utils.h"
#include <stdint.h>

typedef struct {
    u8 id;
    u8 x;
    u8 y;
    char type;
    u32 cost;
    u32 steps;
} Amphipod;

typedef struct {
    u8 map[7][13];
    Amphipod pods[16];
    u8 room_depth;
    u8 pods_count;
} Diagram;

void print_diagram(Diagram *diagram) {
    for (int y = 0; y < 7; ++y) {
        for (int x = 0; x < 13; ++x) {
            char pos = diagram->map[y][x];
            if (pos >= 0 && pos < diagram->pods_count) {
                pos = diagram->pods[(u8)pos].type;
            }
            printf("%c", pos);
        }
        puts("");
    }
}

Diagram setup_diagram(bool extended) {
    Diagram d = {0};
    for (int x = 0; x < 13; ++x) {
        d.map[0][x] = '#';
        d.map[1][x] = '.';
        d.map[2][x] = '.';
        d.map[3][x] = '.';

        if (extended) {
            d.map[4][x] = '.';
            d.map[5][x] = '.';
            d.map[6][x] = '#';
        } else {
            d.map[4][x] = '#';
        }

        if (x == 0 || x == 12) {
            d.map[1][x] = '#';
            d.map[2][x] = '#';
        }

        if (x == 1 || x == 11) {
            d.map[2][x] = '#';
        }

        if (x == 2 || x == 4 || x == 6 || x == 8 || x == 10) {
            d.map[2][x] = '#';
            d.map[3][x] = '#';

            if (extended) {
                d.map[4][x] = '#';
                d.map[5][x] = '#';
            }
        }

        if (x < 2 || x > 10) {
            d.map[3][x] = ' ';
            d.map[4][x] = ' ';
            if (extended) {
                d.map[5][x] = ' ';
                d.map[6][x] = ' ';
            }
        }
    }
    d.room_depth = extended ? 5 : 3;
    return d;
}

void add_amphipod(Diagram *d, char type, u8 x, u8 y) {
    Amphipod *pod = &d->pods[d->pods_count++];
    pod->id = d->pods_count - 1;
    pod->type = type;
    pod->x = x;
    pod->y = y;
    pod->cost = 0;
    switch (type) {
    case 'A':
        pod->cost = 1;
        break;
    case 'B':
        pod->cost = 10;
        break;
    case 'C':
        pod->cost = 100;
        break;
    case 'D':
        pod->cost = 1000;
        break;
    }
    pod->steps = 0;
    d->map[y][x] = d->pods_count - 1;
}

Diagram setup_test(bool extended) {
    Diagram d = setup_diagram(extended);

    if (extended) {
        add_amphipod(&d, 'B', 3, 2);
        add_amphipod(&d, 'D', 3, 3);
        add_amphipod(&d, 'D', 3, 4);
        add_amphipod(&d, 'A', 3, 5);

        add_amphipod(&d, 'C', 5, 2);
        add_amphipod(&d, 'C', 5, 3);
        add_amphipod(&d, 'B', 5, 4);
        add_amphipod(&d, 'D', 5, 5);

        add_amphipod(&d, 'B', 7, 2);
        add_amphipod(&d, 'B', 7, 3);
        add_amphipod(&d, 'A', 7, 4);
        add_amphipod(&d, 'C', 7, 5);

        add_amphipod(&d, 'D', 9, 2);
        add_amphipod(&d, 'A', 9, 3);
        add_amphipod(&d, 'C', 9, 4);
        add_amphipod(&d, 'A', 9, 5);

    } else {
        add_amphipod(&d, 'B', 3, 2);
        add_amphipod(&d, 'A', 3, 3);
        add_amphipod(&d, 'C', 5, 2);
        add_amphipod(&d, 'D', 5, 3);
        add_amphipod(&d, 'B', 7, 2);
        add_amphipod(&d, 'C', 7, 3);
        add_amphipod(&d, 'D', 9, 2);
        add_amphipod(&d, 'A', 9, 3);
    }

    return d;
}

Diagram setup_done(bool extended) {
    Diagram d = setup_diagram(extended);
    if (extended) {
        add_amphipod(&d, 'A', 3, 2);
        add_amphipod(&d, 'A', 3, 3);
        add_amphipod(&d, 'A', 3, 4);
        add_amphipod(&d, 'A', 3, 5);

        add_amphipod(&d, 'B', 5, 2);
        add_amphipod(&d, 'B', 5, 3);
        add_amphipod(&d, 'B', 5, 4);
        add_amphipod(&d, 'B', 5, 5);

        add_amphipod(&d, 'C', 7, 2);
        add_amphipod(&d, 'C', 7, 3);
        add_amphipod(&d, 'C', 7, 4);
        add_amphipod(&d, 'C', 7, 5);

        add_amphipod(&d, 'D', 9, 2);
        add_amphipod(&d, 'D', 9, 3);
        add_amphipod(&d, 'D', 9, 4);
        add_amphipod(&d, 'D', 9, 5);

    } else {
        add_amphipod(&d, 'A', 3, 2);
        add_amphipod(&d, 'A', 3, 3);

        add_amphipod(&d, 'B', 5, 2);
        add_amphipod(&d, 'B', 5, 3);

        add_amphipod(&d, 'C', 7, 2);
        add_amphipod(&d, 'C', 7, 3);

        add_amphipod(&d, 'D', 9, 2);
        add_amphipod(&d, 'D', 9, 3);
    }

    return d;
}

Diagram setup_input(bool extended) {
    Diagram d = setup_diagram(extended);

    if (extended) {
        add_amphipod(&d, 'A', 3, 2);
        add_amphipod(&d, 'D', 3, 3);
        add_amphipod(&d, 'D', 3, 4);
        add_amphipod(&d, 'C', 3, 5);

        add_amphipod(&d, 'D', 5, 2);
        add_amphipod(&d, 'C', 5, 3);
        add_amphipod(&d, 'B', 5, 4);
        add_amphipod(&d, 'D', 5, 5);

        add_amphipod(&d, 'A', 7, 2);
        add_amphipod(&d, 'B', 7, 3);
        add_amphipod(&d, 'A', 7, 4);
        add_amphipod(&d, 'B', 7, 5);

        add_amphipod(&d, 'C', 9, 2);
        add_amphipod(&d, 'A', 9, 3);
        add_amphipod(&d, 'C', 9, 4);
        add_amphipod(&d, 'B', 9, 5);

    } else {
        add_amphipod(&d, 'A', 3, 2);
        add_amphipod(&d, 'C', 3, 3);

        add_amphipod(&d, 'D', 5, 2);
        add_amphipod(&d, 'D', 5, 3);

        add_amphipod(&d, 'A', 7, 2);
        add_amphipod(&d, 'B', 7, 3);

        add_amphipod(&d, 'C', 9, 2);
        add_amphipod(&d, 'B', 9, 3);
    }

    return d;
}

Amphipod *pod_at(Diagram *d, u8 x, u8 y) {
    u8 pod_index = d->map[y][x];
    if (pod_index >= 0 && pod_index < d->pods_count) {
        return &d->pods[pod_index];
    }
    return NULL;
}

bool is_route_free(Diagram *d, Amphipod *pod, u8 x, u8 y) {
    // walk from start to finish to see if there are pods inbetween
    u8 from = pod->x < x ? pod->x : x;
    u8 to = pod->x < x ? x : pod->x;

    // along the hallway
    for (int i = from; i <= to; ++i) {
        Amphipod *stranger = pod_at(d, i, 1);
        if (stranger != NULL && stranger != pod) {
            return false;
        }
    }

    // down the sideroom
    to = pod->y < y ? y : pod->y;
    u8 room_x = y == 1 ? pod->x : x;
    for (int i = 2; i <= to; ++i) {
        Amphipod *stranger = pod_at(d, room_x, i);
        if (stranger != NULL && stranger != pod) {
            return false;
        }
    }
    return true;
}

bool room_has_strangers(Diagram *d, char type) {
    u8 dst_room = (type - 'A') * 2 + 3;
    for (int i = d->room_depth; i > 1; --i) {
        Amphipod *other = pod_at(d, dst_room, i);
        if (other == NULL) {
            return false;
        }

        if (other->type != type) {
            return true;
        }
    }
    return false;
}

typedef struct {
    u8 x[7];
    u8 y[7];
    u8 steps[7];
    int count;
} Moves;

void add_move(Moves *moves, Amphipod *pod, u8 x, u8 y) {
    moves->x[moves->count] = x;
    moves->y[moves->count] = y;
    moves->steps[moves->count] = abs(pod->x - x) + abs(pod->y - y);
    moves->count++;
}

Moves valid_moves(Diagram *d, Amphipod *pod) {
    Moves moves = {0};
    u8 dst_room = (pod->type - 'A') * 2 + 3;

    if (pod->y == 1) {
        // can only move into a room -> 3, 5, 7, 9
        // check availability from innermost position first
        if (!room_has_strangers(d, pod->type)) {
            for (int i = d->room_depth; i > 1; --i) {
                if (is_route_free(d, pod, dst_room, i)) {
                    add_move(&moves, pod, dst_room, i);
                    break;
                }
            }
        }
    } else {
        // if room has no strangers and is right room -> stay!
        if (pod->x != dst_room || room_has_strangers(d, pod->type)) {
            if (is_route_free(d, pod, 1, 1)) {
                add_move(&moves, pod, 1, 1);
            }
            if (is_route_free(d, pod, 2, 1)) {
                add_move(&moves, pod, 2, 1);
            }
            if (is_route_free(d, pod, 4, 1)) {
                add_move(&moves, pod, 4, 1);
            }
            if (is_route_free(d, pod, 6, 1)) {
                add_move(&moves, pod, 6, 1);
            }
            if (is_route_free(d, pod, 8, 1)) {
                add_move(&moves, pod, 8, 1);
            }
            if (is_route_free(d, pod, 10, 1)) {
                add_move(&moves, pod, 10, 1);
            }
            if (is_route_free(d, pod, 11, 1)) {
                add_move(&moves, pod, 11, 1);
            }
        }
    }
    return moves;
}

bool is_solved(Diagram *d) {
    for (int i = 0; i < d->pods_count; ++i) {
        Amphipod *pod = &d->pods[i];
        int room_x = (pod->type - 'A') * 2 + 3;
        if (pod->x != room_x) {
            return false;
        }
    }
    return true;
}

u32 calculate_energy(Diagram *d) {
    u32 energy = 0;
    for (int i = 0; i < d->pods_count; ++i) {
        energy += d->pods[i].steps * d->pods[i].cost;
    }
    return energy;
}

typedef union {
    struct {
        u16 type : 2;  // 0..3 <- (type - 'A')
        u16 x : 4;     // 0..15
        u16 y : 4;     // 0..15
        u16 steps : 6; // 0..64?
    };
    u16 value;

} HashablePod;

HashablePod hash_pod(Amphipod *pod) {
    HashablePod hp = {0};
    hp.type = pod->type - 'A';
    hp.x = pod->x;
    hp.y = pod->y;
    hp.steps = pod->steps;
    return hp;
}

u64 hash_pods(Diagram *d) {
    u64 hash = 59604644783353249u;

    for (int i = 0; i < d->pods_count; i++) {
        Amphipod *pod = &d->pods[i];
        hash ^= (u16)hash_pod(pod).value;
        hash *= 16777619u;
    }

    return hash;
}

void move_amphipod(Diagram *d, Amphipod *pod, u8 x, u8 y, s8 steps) {
    d->map[pod->y][pod->x] = '.';
    pod->x = x;
    pod->y = y;
    pod->steps += steps;
    d->map[pod->y][pod->x] = pod->id;
}

typedef struct {
    u8 depth;
    u8 solution_depth;
    u8 max_depth;
    u32 min_score;
    Dict *memo;
} RecurseMonitor;

u64 solver(Diagram *d, RecurseMonitor *mon) {
    if (calculate_energy(d) >= mon->min_score) {
        return UINT64_MAX;
    }

    

    Value key = UNSIGNED_VAL(hash_pods(d));
    if (dict_contains(mon->memo, &key)) {
        Value val;
        dict_get(mon->memo, &key, &val);
        return val.as.unsigned_64;
    }

    u64 energy = UINT64_MAX;
    mon->depth++;
    if (is_solved(d)) {
        energy = calculate_energy(d);
        if (mon->min_score > energy) {
            mon->min_score = energy;
            mon->solution_depth = mon->depth;
            //printf("Energy=%llu\n", energy);
        }
        if (mon->max_depth < mon->depth) {
            mon->max_depth = mon->depth;
            // printf("Level=%d\n", mon->depth);
        }

    } else {

        for (int i = 0; i < d->pods_count; ++i) {
            Amphipod *pod = &d->pods[i];
            Moves moves = valid_moves(d, pod);

            for (int j = 0; j < moves.count; ++j) {
                u8 ox = pod->x;
                u8 oy = pod->y;

                move_amphipod(d, pod, moves.x[j], moves.y[j], moves.steps[j]);

                u64 nrg = solver(d, mon);
                if (nrg < energy) {
                    energy = nrg;
                }

                move_amphipod(d, pod, ox, oy, -moves.steps[j]);
            }
        }
        dict_set(mon->memo, &key, UNSIGNED_VAL(energy));
    }
    mon->depth--;
    return energy;
}

u64 solve(Diagram *d) {
    RecurseMonitor mon;
    mon.depth = 0;
    mon.max_depth = 0;
    mon.min_score = UINT32_MAX;
    mon.memo = dict_create();
    u64 result = solver(d, &mon);
    printf("number of turns = %d\n", mon.solution_depth);
    printf("memoized items = %d\n", mon.memo->count);
    dict_free(mon.memo);
    return result;
}

void test_examples(Tester *tester) {
    test_section("Examples Part 1");

    Diagram ext = setup_test(true);
    test(tester, !is_solved(&ext), "");

    Diagram done = setup_done(false);
    test(tester, is_solved(&done), "");
    Diagram done_ext = setup_done(true);
    test(tester, is_solved(&done_ext), "extended");

    Diagram d = setup_test(false);
    test(tester, !is_solved(&d), "");
    testi(tester, solve(&d), 12521, "");

    test_section("Examples Part 2");

    Diagram d_ext = setup_test(true);
    testi(tester, solve(&d_ext), 44169, "");
}

int main() {
    Tester tester = create_tester("Amphipod");
    test_examples(&tester);

    test_section("Solutions");

    Diagram d = setup_input(false);
    testi(&tester, solve(&d), 15385, "solution to part 1");

    Diagram d_ext = setup_input(true);
    testi(&tester, solve(&d_ext), 49803, "solution to part 2");

    return test_summary(&tester);
}
