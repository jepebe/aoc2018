#include "aoc.h"
#include "dict.h"
#include "utils.h"
#include <math.h>
#include <stdint.h>
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

Value pair_key(char a, char b) {
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

        Value pair_val = pair_key(rule->a, rule->b);
        dict_set(poly.rule_map, &pair_val, UNSIGNED_VAL(poly.rule_count - 1));

        node = node->next;
    }

    free(data);
    queue_free(q);
    return poly;
}

void increment_pair(Dict *dict, char a, char b, u64 increment) {
    Value key = pair_key(a, b);
    if (!dict_contains(dict, &key)) {
        dict_set(dict, &key, UNSIGNED_VAL(0));
    }
    Value val;
    dict_get(dict, &key, &val);
    val.as.unsigned_64 += increment;
    dict_set(dict, &key, val);
}

u64 polymerize(Polymerization *poly, char *template, int iterations) {
    Dict *pairs = dict_create();

    int len = strlen(template);
    for (int i = 0; i < len - 1; ++i) {
        char a = template[i];
        char b = template[i + 1];
        increment_pair(pairs, a, b, 1);
    }

    for (int i = 0; i < iterations; ++i) {
        Dict *next = dict_create();
        
        Queue *keys = dict_keys(pairs);
        QueueNode *node = keys->head;
        while (node) {
            Value *key = &node->value;
            Value pair_count;
            dict_get(pairs, key, &pair_count);

            Value rule_index;
            dict_get(poly->rule_map, key, &rule_index);
            Rule *rule = &poly->rule[rule_index.as.unsigned_64];

            char a = (key->as.unsigned_64 >> 8) & 0xFF;
            char b = key->as.unsigned_64 & 0xFF;
            u64 n = pair_count.as.unsigned_64;
            increment_pair(next, a, rule->replacement, n);
            increment_pair(next, rule->replacement, b, n);

            node = node->next;
        }
        
        dict_free(pairs);
        pairs = next;
    }

    u64 letters[26];
    for (int i = 0; i < 26; ++i) {
        letters[i] = 0;
    }

    // Ensure that the endpoints are counted once
    letters[template[0] - 'A'] += 1;
    letters[template[len - 1] - 'A'] += 1;

    Queue *keys = dict_keys(pairs);
    QueueNode *node = keys->head;
    while (node) {
        Value *key = &node->value;
        Value pair_count;
        dict_get(pairs, key, &pair_count);

        char a = (key->as.unsigned_64 >> 8) & 0xFF;
        char b = key->as.unsigned_64 & 0xFF;
        u64 n = pair_count.as.unsigned_64;

        letters[a - 'A'] += n;
        letters[b - 'A'] += n;

        node = node->next;
    }

    u64 min = INT64_MAX;
    u64 max = 0;
    for (int i = 0; i < 26; ++i) {
        u64 n = letters[i] / 2; // divide by 2 since we count everything twice
        
        if (n > 0 && n < min) {
            min = n;
        }
        if (n > max) {
            max = n;
        }
    }
    
    dict_free(pairs);
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
