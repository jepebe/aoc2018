#include "aoc.h"
#include "dict.h"
#include "utils.h"
#include <string.h>

typedef struct {
    char a;
    char b;
    char replacement;
} Rule;

typedef struct {
    char *template;
    int rule_count;
    Rule rule[100];
    Dict *rule_map;
} Polymerization;

Value rule_key(char a, char b) {
    return UNSIGNED_VAL((a << 8) | b);
}

Polymerization parse_polymer(char *file) {
    char *data = read_input(file);
    Queue *q = read_lines(data);

    Polymerization poly = {0};
    poly.template = strdup(queue_pop_front(q).as.string);
    poly.rule_map = dict_create();

    QueueNode *node = q->head;
    while (node) {
        Rule *rule = &poly.rule[poly.rule_count++];
        char *line = node->value.as.string;

        char *pair = strdup(strtok(line, " "));
        rule->a = pair[0];
        rule->b = pair[1];
        strtok(NULL, " "); // skip arrow
        rule->replacement = *strtok(NULL, " ");

        Value pair_val = rule_key(rule->a, rule->b);
        dict_set(poly.rule_map, &pair_val, UNSIGNED_VAL(poly.rule_count - 1));

        node = node->next;
    }

    free(data);
    queue_free(q);
    return poly;
}

typedef struct {
    Polymerization *poly;
    u64 *letters;
    int destination_depth;
    Dict *memo;
} PolymerTracker;

Value depth_pair_key(int depth, char a, char b) {
    return UNSIGNED_VAL((depth << 16) | (a << 8) | b);
}

u64 *create_letters() {
    u64 *letters = malloc(sizeof(u64) * 26);
    memset(letters, 0, 26);
    return letters;
}

void add_letters(u64 const *src, u64 *dst) {
    for (int i = 0; i < 26; ++i) {
        dst[i] += src[i];
    }
}

void polymerizer(PolymerTracker *tracker, char a, char b, int depth) {
    if (depth == tracker->destination_depth) {
        tracker->letters[a - 'A']++;
        tracker->letters[b - 'A']++;
        // printf("%c%c ", a, b);
        return;
    }

    Value depth_key = depth_pair_key(depth, a, b);
    if (dict_contains(tracker->memo, &depth_key)) {
        Value val;
        dict_get(tracker->memo, &depth_key, &val);
        u64 *letters = val.as.ptr;
        add_letters(letters, tracker->letters);
        return;
    }

    Value rule_index;
    Value key = rule_key(a, b);
    dict_get(tracker->poly->rule_map, &key, &rule_index);

    u64 *current_letters = tracker->letters;
    tracker->letters = create_letters();

    Rule *rule = &tracker->poly->rule[rule_index.as.unsigned_64];
    
    polymerizer(tracker, a, rule->replacement, depth + 1);
    polymerizer(tracker, rule->replacement, b, depth + 1);
   
    tracker->letters[rule->replacement - 'A']--; // avoid double counting

    dict_set(tracker->memo, &depth_key, POINTER_VAL(tracker->letters));

    add_letters(tracker->letters, current_letters);

    tracker->letters = current_letters;
}

u64 polymerize(Polymerization *poly, char *template, int iterations) {
    PolymerTracker tracker = {0};
    tracker.poly = poly;
    tracker.destination_depth = iterations;
    tracker.memo = dict_create();
    tracker.letters = create_letters();

    int len = strlen(template);

    for (int i = 0; i < len - 1; ++i) {
        
        polymerizer(&tracker, template[i], template[i + 1], 0);
        if(i > 0) {
            int letter = (int)template[i] - 'A';
            tracker.letters[letter]--; // remove overlap
        }
    }

    // puts("");
    u64 min = UINT64_MAX;
    u64 max = 0;
    for (int i = 0; i < 26; ++i) {
        u64 n = tracker.letters[i];
        if (n > 0) {
            // printf("%c = %llu\n", (i + 'A'), n);
        }
        if (n > 0 && n < min) {
            min = n;
        }
        if (n > max) {
            max = n;
        }
    }
    // printf("max = %llu min = %llu\n", max, min);
    return max - min;
}

void test_examples(Tester *tester) {
    test_section("Examples Part 1");

    Polymerization poly = parse_polymer("../aoc2021/day14/test");
    testi(tester, poly.rule_count, 16, "poly count");

    u64 diff = polymerize(&poly, poly.template, 1);
    testi(tester, diff, 1, "step 1");

    diff = polymerize(&poly, "NCNBCHB", 1);
    testi(tester, diff, 5, "step 2");

    diff = polymerize(&poly, poly.template, 2);
    testi(tester, diff, 5, "step 2");

    diff = polymerize(&poly, "NBCCNBBBCBHCB", 1);
    testi(tester, diff, 7, "step 3");

    diff = polymerize(&poly, poly.template, 3);
    testi(tester, diff, 7, "step 3");
    
    diff = polymerize(&poly, poly.template, 4);
    testi(tester, diff, 18, "step 4");

    diff = polymerize(&poly, poly.template, 10);
    testi(tester, diff, 1588, "quantity diff");

    test_section("Examples Part 2");

    diff = polymerize(&poly, poly.template, 40);
    test_u64(tester, diff, 2188189693529, "quantity diff 40 steps");
}

int main() {
    Tester tester = create_tester("Extended Polymerization");
    test_examples(&tester);

    test_section("Solutions");

    Polymerization poly = parse_polymer("../aoc2021/day14/input");
    u64 quantity = polymerize(&poly, poly.template, 10);
    test_u64(&tester, quantity, 3408, "solution to part 1");

    quantity = polymerize(&poly, poly.template, 40);
    test_u64(&tester, quantity, 3724343376942, "solution to part 2");

    return test_summary(&tester);
}
