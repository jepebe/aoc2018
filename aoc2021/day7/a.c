#include "aoc.h"
#include "utils.h"

typedef struct {
    u16 crabs[1000];
    u16 crab_count;
    u16 max_crab;
} Crabs;

Crabs parse_crabs(char *data) {
    Crabs crabs;
    char *token;
    crabs.crab_count = 0;
    crabs.crabs[crabs.crab_count++] = x_strtol(data, 10, &token, __LINE__);
    crabs.max_crab = crabs.crabs[crabs.crab_count - 1];

    while (*token == ',') {
        crabs.crabs[crabs.crab_count++] = x_strtol(token + 1, 10, &token, __LINE__);

        if (crabs.crabs[crabs.crab_count - 1] > crabs.max_crab) {
            crabs.max_crab = crabs.crabs[crabs.crab_count - 1];
        }
    }
    return crabs;
}

int align_crabs(Crabs *crabs, int position, bool high_cost) {
    int cost = 0;
    for (int i = 0; i < crabs->crab_count; ++i) {
        int distance = abs(crabs->crabs[i] - position);
        if (high_cost) {
            cost += distance * (distance + 1) / 2;
        } else {
            cost += distance;
        }
    }
    return cost;
}

int find_best_alignment(Crabs *crabs, bool high_cost) {
    int cost = 99999999;
    int alignment_index = -1;
    for (int i = 0; i < crabs->max_crab; ++i) {
        int alignment_cost = align_crabs(crabs, i, high_cost);
        if (alignment_cost < cost) {
            cost = alignment_cost;
            alignment_index = i;
        }
    }
    return cost;
}

void test_examples(Tester *tester) {
    test_section("Examples Part 1");
    char data[] = "16,1,2,0,4,2,7,1,2,14";
    Crabs crabs = parse_crabs(data);
    testi(tester, crabs.crab_count, 10, "count");
    testi(tester, crabs.max_crab, 16, "max");

    testi(tester, align_crabs(&crabs, 1, false), 41, "align 1");
    testi(tester, align_crabs(&crabs, 3, false), 39, "align 3");
    testi(tester, align_crabs(&crabs, 10, false), 71, "align 10");
    testi(tester, find_best_alignment(&crabs, false), 37, "align 2");

    test_section("Examples Part 2");

    testi(tester, align_crabs(&crabs, 2, true), 206, "align 2");
    testi(tester, find_best_alignment(&crabs, true), 168, "align 5");
}

int main() {
    Tester tester = create_tester("The Treachery of Whales");
    test_examples(&tester);

    test_section("Solutions");

    char *data = read_input("../aoc2021/day7/input");
    Crabs crabs = parse_crabs(data);
    testi(&tester, crabs.crab_count, 1000, "count");
    testi(&tester, crabs.max_crab, 1897, "max");

    testi(&tester, find_best_alignment(&crabs, false), 342641, "solution to part 1");

    testi(&tester, find_best_alignment(&crabs, true), 93006301, "solution to part 2");

    return test_summary(&tester);
}
