#include "aoc.h"
#include "utils.h"

typedef struct {
    u8 seg[10];
    u8 disp[4];
    u8 digits[10];
} Segments;

typedef struct {
    Segments combination[201];
    u8 count;
} Signals;

// set bits where a,b,c,d,e,f,g = bit 0,1,2,3,4,5,6
u8 set_bits(char *txt) {
    u8 val = 0;
    int n = strlen(txt);
    for (int j = 0; j < n; ++j) {
        char c = txt[j];
        val |= 0x1 << (c - 97); // 97 = a
    }
    return val;
}

Signals parse_data(char *data) {
    Queue *q = read_lines(data);

    Signals signals;
    signals.count = 0;

    QueueNode *node = q->head;
    while (node) {
        char *seg = strtok(node->value.as.string, "|");
        char *disp = strtok(NULL, "|");

        Segments segments = {0};
        char *token = strtok(seg, " ");
        for (int i = 0; i < 10; ++i) {
            segments.seg[i] = set_bits(token);
            token = strtok(NULL, " ");
        }

        token = strtok(disp, " ");
        for (int i = 0; i < 4; ++i) {
            segments.disp[i] = set_bits(token);
            token = strtok(NULL, " ");
        }
        node = node->next;
        signals.combination[signals.count++] = segments;
    }
    queue_free(q);

    return signals;
}

int count_unique(Signals *signals) {
    int unique = 0;
    for (int i = 0; i < signals->count; ++i) {
        Segments *segments = &signals->combination[i];
        for (int j = 0; j < 4; j++) {
            int len = count_set_bits(segments->disp[j]);

            if (len == 2 || len == 4 || len == 3 || len == 7) {
                unique++;
            }
        }
    }
    return unique;
}

int decode_combination(Segments *seg) {
    for (int j = 0; j < 10; j++) {
        u8 digit = seg->seg[j];
        if (count_set_bits(digit) == 2) {
            seg->digits[1] = digit;
        } else if (count_set_bits(digit) == 4) {
            seg->digits[4] = digit;
        } else if (count_set_bits(digit) == 3) {
            seg->digits[7] = digit;
        } else if (count_set_bits(digit) == 7) {
            seg->digits[8] = digit;
        }
    }

    u8 ul_c = seg->digits[4] ^ seg->digits[1]; // upper left and center
    u8 c = 0;                                  // center
    u8 ll = 0;                                 // lower left
    u8 ur = 0;                                 // upper right

    for (int j = 0; j < 10; j++) {
        u8 digit = seg->seg[j];

        if (count_set_bits(digit) == 6) {
            // 6, 9, 0
            u8 zero = ul_c ^ (digit & ul_c);         // 6 and 9 will XOR away center
            u8 six_or_nine = seg->digits[8] ^ digit; // XOR will leave ur or ll

            if (zero) {
                c = zero;
                seg->digits[0] = digit;
            } else if (six_or_nine) {
                // if six_or_nine overlaps with 1 we have upper right
                if (six_or_nine & seg->digits[1]) {
                    ur = six_or_nine;
                    seg->digits[6] = digit;
                } else {
                    ll = six_or_nine; // lower left since we have 9
                    seg->digits[9] = digit;
                }
            }
        }
    }

    for (int j = 0; j < 10; j++) {
        u8 digit = seg->seg[j];

        if (count_set_bits(digit) == 5) {
            // 2, 3, 5
            u8 two_or_three = digit & ur;// upper right is only in 2 or 3
            
            if (two_or_three) { 
                if (digit & ll) { // only 2 has lower left
                    seg->digits[2] = digit;
                } else {
                    seg->digits[3] = digit;
                }
            } else { 
                seg->digits[5] = digit;
            }
        }
    }

    int result = 0;
    for (int i = 0; i < 4; ++i) {
        result *= 10;
        u8 curd = seg->disp[i];
        for (int j = 0; j < 10; ++j) {
            if (curd == seg->digits[j]) {
                result += j;
                break;
            }
        }
    }
    return result;
}

u64 totality(Signals *signals) {
    u64 total = 0;

    for (int i = 0; i < signals->count; ++i) {
        total += decode_combination(&signals->combination[i]);
    }
    return total;
}

void test_examples(Tester *tester) {
    test_section("Examples Part 1");

    char *data = read_input("../aoc2021/day8/test");
    Signals signals = parse_data(data);

    testi(tester, count_unique(&signals), 26, "unique");

    test_section("Examples Part 2");

    int value = decode_combination(&signals.combination[0]);

    testi(tester, value, 8394, "0");

    testi(tester, totality(&signals), 61229, "total");
}

int main() {
    Tester tester = create_tester("Seven Segment Search");
    test_examples(&tester);

    test_section("Solutions");

    char *data = read_input("../aoc2021/day8/input");
    Signals signals = parse_data(data);

    testi(&tester, count_unique(&signals), 278, "solution to part 1");
    testi(&tester, totality(&signals), 986179, "solution to part 2");

    return test_summary(&tester);
}
