#include "aoc.h"
#include "utils.h"
#include <stdlib.h>
#include <string.h>

typedef struct {
    u64 gamma;
    u64 epsilon;
    u64 equal_bits;
} Power;

typedef struct {
    u64 oxygen;
    u64 co2;
} Life;

Value to_binary(char *bin) {
    return SIGNED_VAL(strtol(bin, NULL, 2));
}

Power find_common_bits(Queue *queue, u8 bits) {
    int count = queue_length(queue);

    Power p = {0};
    for (int i = bits - 1; i >= 0; --i) {
        u16 ones = 0;
        QueueNode *node = queue->head;
        while (node) {
            u64 n = node->value.as.unsigned_64;
            if ((n >> i) & 0x1) {
                ones++;
            }
            node = node->next;
        }
        if (ones > count / 2) {
            p.gamma |= 0x1 << i;
        } else {
            p.epsilon |= 0x1 << i;
        }

        if ((count & 0x1) == 0 && ones == count / 2) {
            p.equal_bits |= 0x1 << i;
        }
    }
    return p;
}

Power power_diagnostic(char *data, u8 bits) {
    char *buffer = (char *)malloc(sizeof(char) * strlen(data));
    strcpy(buffer, data);
    Queue *q = read_lines_fmt(buffer, to_binary);

    Power p = find_common_bits(q, bits);

    free(q);
    free(buffer);
    return p;
}

void filter_diagnostics(Queue *queue, u8 bits, bool most_common) {
    for (int i = bits - 1; i >= 0; --i) {
        Power p = find_common_bits(queue, bits);
        bool keep_bit;

        if (most_common) {
            // most common bit value
            keep_bit = ((p.equal_bits >> i) & 0x1) || ((p.gamma >> i) & 0x1);
        } else {
            // least common bit value
            keep_bit = !((p.gamma >> i) & 0x1);
            if ((p.equal_bits >> i) & 0x1) {
                keep_bit = 0;
            }
        }
        QueueNode *node = queue->head;
        while (node) {
            QueueNode *temp = node;
            node = node->next;

            bool set_bit = (temp->value.as.unsigned_64 >> i) & 0x1;
            if (keep_bit != set_bit) {
                queue_remove_node(queue, temp);
            }
        }

        if (queue_length(queue) == 1) {
            break;
        }
    }
}

Life life_support_diagnostic(char *data, u8 bits) {
    char *buffer = (char *)malloc(sizeof(char) * strlen(data));
    strcpy(buffer, data);
    Queue *oxygen_queue = read_lines_fmt(buffer, to_binary);
    Queue *co2_queue = queue_create();
    queue_add_all(co2_queue, oxygen_queue);

    filter_diagnostics(oxygen_queue, bits, true);
    filter_diagnostics(co2_queue, bits, false);

    Life life = {.oxygen = oxygen_queue->head->value.as.unsigned_64,
                 .co2 = co2_queue->head->value.as.unsigned_64};

    free(oxygen_queue);
    free(co2_queue);
    free(buffer);
    return life;
}

void test_examples(Tester *tester) {
    test_section("Examples Power");
    char data[] = "00100\n11110\n10110\n10111\n10101\n01111\n00111\n11100\n10000\n11001\n00010\n01010\n";

    Power p = power_diagnostic(data, 5);

    testi(tester, p.gamma, 22, "gamma");
    testi(tester, p.epsilon, 9, "epsilon");
    testi(tester, p.equal_bits, 0, "equal");

    testi(tester, p.gamma * p.epsilon, 198, "test");

    test_section("Examples Life Support");
    Life l = life_support_diagnostic(data, 5);
    testi(tester, l.oxygen, 23, "oxygen");
    testi(tester, l.co2, 10, "co2");
}

int main() {
    Tester tester = create_tester("Binary Diagnostic");
    test_examples(&tester);

    test_section("Solutions");
    char *data = read_input("../aoc2021/day3/input");
    Power p = power_diagnostic(data, 12);
    Life l = life_support_diagnostic(data, 12);

    testi(&tester, ~p.gamma & 0xFFF, p.epsilon, "assert");
    testi(&tester, p.gamma, ~p.epsilon & 0xFFF, "assert");
    testi(&tester, p.gamma * p.epsilon, 4001724, "solution to part 1");
    testi(&tester, l.oxygen * l.co2, 587895, "solution to part 2");

    return test_summary(&tester);
}
