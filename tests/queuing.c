#include "aoc.h"
#include "queue.h"

void test_queuing(Tester *tester) {
    Queue *q = queue_create();

    testi(tester, queue_length(q), 0, "queue length");
    test(tester, queue_empty(q), "empty");

    queue_append(q, UNSIGNED_VAL(1337));

    QueueNode *qn1 = q->head;
    testi(tester, queue_length(q), 1, "queue length");
    test(tester, qn1->next == NULL, "next");
    test(tester, qn1->previous == NULL, "previous");
    test(tester, !queue_empty(q), "not empty");

    queue_append(q, UNSIGNED_VAL(0xA5A5));
    QueueNode *qn2 = q->tail;

    testi(tester, queue_length(q), 2, "queue length");
    test(tester, qn1->next == qn2, "next");
    test(tester, qn1->previous == NULL, "previous");
    test(tester, qn2->previous == qn1, "previous");
    test(tester, qn2->next == NULL, "next");

    queue_append(q, UNSIGNED_VAL(0xB00B));
    QueueNode *qn3 = q->tail;

    testi(tester, queue_length(q), 3, "queue length");
    test(tester, qn1->next == qn2, "next");
    test(tester, qn1->previous == NULL, "previous");
    test(tester, qn2->previous == qn1, "previous");
    test(tester, qn2->next == qn3, "next");
    test(tester, qn3->previous == qn2, "previous");
    test(tester, qn3->next == NULL, "next");

    testi(tester, queue_sum_signed(q), 88809, "queue sum 3");

    Value v = queue_pop_front(q);
    test(tester, is_value_equal(&v, &UNSIGNED_VAL(1337)), "first element");
    testi(tester, queue_length(q), 2, "queue length");
    testi(tester, queue_sum_signed(q), 87472, "queue sum 2");

    v = queue_pop_front(q);
    test(tester, is_value_equal(&v, &UNSIGNED_VAL(0xA5A5)), "second element");
    testi(tester, queue_length(q), 1, "queue length");
    testi(tester, queue_sum_signed(q), 45067, "queue sum 1");

    v = queue_pop_front(q);
    test(tester, is_value_equal(&v, &UNSIGNED_VAL(0xB00B)), "third element");
    testi(tester, queue_length(q), 0, "queue length");
    testi(tester, queue_sum_signed(q), 0, "queue sum 0");

    v = queue_pop_front(q);
    test(tester, is_value_equal(&v, &NIL_VAL), "empty queue");
    testi(tester, queue_length(q), 0, "queue length");
    testi(tester, queue_sum_signed(q), 0, "queue sum 0");

    test(tester, queue_empty(q), "empty");

    queue_free(q);
}

int main() {
    Tester tester = create_tester("Queuing");

    test_queuing(&tester);

    return test_summary(&tester);
}
