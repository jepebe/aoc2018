#include "aoc.h"
#include "alu.h"
#include "dict.h"
#include "utils.h"
#include <stdint.h>
#include <stdlib.h>

#define DEBUG 0

bool set_input(ALU *alu, u64 n) {
    bool valid = true;
    for (int i = 0; i < 14; ++i) {
        u8 digit = n % 10;
        if (digit == 0) {
            valid = false;
        }
        alu->input[13 - i] = digit;
        n /= 10;
    }
    alu->input_index = 0;
    return valid;
}

u64 recurse(ALU *alu, Dict *memo, int depth, bool find_max) {
    if (depth == 14) {
        if (alu->z == 0) {
            u64 result = 0;
            for (int i = 0; i < 14; ++i) {
                result *= 10;
                result += alu->input[i];
            }
            return result;
        } else {
            return 0;
        }
    }

    u32 pc = alu->pc;
    s64 w = alu->w;
    s64 x = alu->x;
    s64 y = alu->y;
    s64 z = alu->z;
    u8 input_index = alu->input_index;

    for (int i = 1; i < 10; ++i) {
        alu->input[depth] = find_max ? 10 - i : i;
        run(alu, false);

        Value key = UNSIGNED_VAL((alu->z << 8) | (depth & 0xF));
        if (!dict_contains(memo, &key)) {
            dict_set(memo, &key, NIL_VAL);
            u64 result = recurse(alu, memo, depth + 1, find_max);
            if (result > 0) {
                return result;
            }
        }

        alu->pc = pc;
        alu->w = w;
        alu->x = x;
        alu->y = y;
        alu->z = z;
        alu->input_index = input_index;
    }
    alu->input[depth] = 0;
    return 0;
}

u64 find_max_monad(ALU *alu) {
    Dict *memo = dict_create();
    u64 result = recurse(alu, memo, 0, true);
    dict_free(memo);
    return result;
}

u64 find_min_monad(ALU *alu) {
    Dict *memo = dict_create();
    u64 result = recurse(alu, memo, 0, false);
    dict_free(memo);
    return result;
}

void test_examples(Tester *tester) {
    test_section("Examples Part 1");
    ALU *alu = create_alu("../aoc2021/day24/test");
    set_input(alu, 91111111111111);
    run(alu, true);

    testi(tester, alu->z, 1, "");
    testi(tester, alu->y, 0, "");
    testi(tester, alu->x, 0, "");
    testi(tester, alu->w, 1, "");

    set_input(alu, 81111111111111);
    run(alu, true);

    testi(tester, alu->z, 0, "");
    testi(tester, alu->y, 0, "");
    testi(tester, alu->x, 0, "");
    testi(tester, alu->w, 1, "");

    alu = create_alu("../aoc2021/day24/input");
    set_input(alu, 13579246899999);
    run(alu, true);
    test_u64(tester, alu->z, 134689198, "");

    set_input(alu, 99995969919326);
    run(alu, true);
    test_u64(tester, alu->z, 0, "");
}

int main() {
    Tester tester = create_tester("Arithmetic Logic Unit");
    test_examples(&tester);

    test_section("Solutions");

    ALU *alu = create_alu("../aoc2021/day24/input");
    u64 result = find_max_monad(alu);
    test_u64(&tester, result, 99995969919326, "solution to part 1");

    ALU *alu2 = create_alu("../aoc2021/day24/input");
    u64 result2 = find_min_monad(alu2);
    test_u64(&tester, result2, 48111514719111, "solution to part 2");

    return test_summary(&tester);
}
