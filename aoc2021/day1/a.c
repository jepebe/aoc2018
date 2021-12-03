#include "aoc.h"
#include "queue.h"
#include "utils.h"
#include <stdlib.h>

typedef struct {
    int depth_increases;
    int depth_window_increases;
} Depths;

Depths measure_increases(char *measurements) {
    Queue *tokens = read_lines_as_ints(measurements);
    QueueNode *node = tokens->head;
    int previous_depth = node->value.as.signed_64;
    int previous_depth_window = -1;

    Depths d = {0};
    Queue *q = queue_create();

    while (node) {
        int depth = node->value.as.signed_64;
        queue_append(q, SIGNED_VAL(depth));

        if (queue_length(q) == 3) {
            int depth_window = queue_sum_signed(q);
            if (previous_depth_window != -1) {
                if (previous_depth_window < depth_window) {
                    d.depth_window_increases++;
                }
            }
            previous_depth_window = depth_window;
            queue_pop_front(q);
        }

        if (depth > previous_depth) {
            d.depth_increases++;
        }
        previous_depth = depth;
        node = node->next;
    }
    queue_free(q);
    queue_free(tokens);
    return d;
}

void test_measure_increases(Tester *tester) {
    test_section("Examples");
    char txt[] = "199\n200\n208\n210\n200\n207\n240\n269\n260\n263\n";
    Depths increases = measure_increases(txt);
    testi(tester, increases.depth_increases, 7, "test");
    testi(tester, increases.depth_window_increases, 5, "test wnd");
}

int main() {
    Tester tester = create_tester("Sonar Sweep");

    test_measure_increases(&tester);

    test_section("Solutions");

    char *depth_txt = read_input("../aoc2021/day1/input");
    Depths increases = measure_increases(depth_txt);
    testi(&tester, increases.depth_increases, 1451, "solution to part 1");
    testi(&tester, increases.depth_window_increases, 1395, "solution to part 2");
    free(depth_txt);

    return test_summary(&tester);
}
