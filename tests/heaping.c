#include "heap.h"

void test_heap_operations(Tester *tester) {
    test_section("Heap Operations");

    Heap *heap = heap_create(10);
    testi(tester, heap->capacity, 15, "pow");
    testi(tester, heap->count, 0, "empty");

    testi(tester, heap_parent_index(1), 0, "parent = root");
    testi(tester, heap_parent_index(2), 0, "parent = root");
    testi(tester, heap_parent_index(3), 1, "parent = left");
    testi(tester, heap_parent_index(4), 1, "parent = left");
    testi(tester, heap_parent_index(5), 2, "parent = right");
    testi(tester, heap_parent_index(6), 2, "parent = right");

    testi(tester, heap_index_left(0), 1, "left = from root");
    testi(tester, heap_index_right(0), 2, "right = from root");
    testi(tester, heap_index_left(1), 3, "left = from left");
    testi(tester, heap_index_right(1), 4, "right = from left");
    testi(tester, heap_index_left(2), 5, "left = from right");
    testi(tester, heap_index_right(2), 6, "right = from right");

    testi(tester, heap_parent_index(0), 0, "parent of root");
    test(tester, !heap_index_is_left(0), "root is not left");
    test(tester, !heap_index_is_right(0), "root is not right");
    test(tester, heap_index_is_left(1), "1 is left");
    test(tester, !heap_index_is_right(1), "1 is not right");
    test(tester, !heap_index_is_left(2), "2 is not left");
    test(tester, heap_index_is_right(2), "2 is right");

    heap_free(heap);
}

void test_heap_insertion(Tester *tester) {
    test_section("Heap Insertions");
    Heap *heap = heap_create(10);

    heap_insert(heap, &CHAR_VAL('A'), 10);
    testc(tester, heap->nodes[0].value.as.character, 'A', "root is A");
    testi(tester, heap->nodes[0].priority, 10, "root is priority 10");

    heap_insert(heap, &CHAR_VAL('B'), 5);
    testc(tester, heap->nodes[0].value.as.character, 'B', "root is B");
    testi(tester, heap->nodes[0].priority, 5, "root is priority 5");
    testc(tester, heap->nodes[1].value.as.character, 'A', "left is A");
    testi(tester, heap->nodes[1].priority, 10, "left is priority 10");

    heap_insert(heap, &CHAR_VAL('C'), 3);
    testc(tester, heap->nodes[0].value.as.character, 'C', "root is C");
    testi(tester, heap->nodes[0].priority, 3, "root is priority 3");
    testc(tester, heap->nodes[1].value.as.character, 'A', "left is A");
    testi(tester, heap->nodes[1].priority, 10, "left is priority 10");
    testc(tester, heap->nodes[2].value.as.character, 'B', "right is B");
    testi(tester, heap->nodes[2].priority, 5, "right is priority 5");

    heap_insert(heap, &CHAR_VAL('D'), 12);
    testc(tester, heap->nodes[0].value.as.character, 'C', "");
    testi(tester, heap->nodes[0].priority, 3, "");
    testc(tester, heap->nodes[1].value.as.character, 'A', "");
    testi(tester, heap->nodes[1].priority, 10, "");
    testc(tester, heap->nodes[2].value.as.character, 'B', "");
    testi(tester, heap->nodes[2].priority, 5, "");
    testc(tester, heap->nodes[3].value.as.character, 'D', "");
    testi(tester, heap->nodes[3].priority, 12, "");
    testi(tester, heap->count, 4, "count");

    heap_insert(heap, &CHAR_VAL('E'), 7);
    testc(tester, heap->nodes[0].value.as.character, 'C', "");
    testc(tester, heap->nodes[1].value.as.character, 'E', "");
    testc(tester, heap->nodes[2].value.as.character, 'B', "");
    testc(tester, heap->nodes[3].value.as.character, 'D', "");
    testc(tester, heap->nodes[4].value.as.character, 'A', "");
    testi(tester, heap->count, 5, "count");

    heap_insert(heap, &CHAR_VAL('F'), 2);
    testc(tester, heap->nodes[0].value.as.character, 'F', "");
    testc(tester, heap->nodes[1].value.as.character, 'E', "");
    testc(tester, heap->nodes[2].value.as.character, 'C', "");
    testc(tester, heap->nodes[3].value.as.character, 'D', "");
    testc(tester, heap->nodes[4].value.as.character, 'A', "");
    testc(tester, heap->nodes[5].value.as.character, 'B', "");

    // for(u32 i = 0; i < heap->count; ++i) {
    //     printf("node=%d priority=%lld value=%c\n", i, heap->nodes[i].priority, heap->nodes[i].value.as.character);
    // }

    heap_free(heap);
}

void test_heap_extractions(Tester *tester) {
    test_section("Heap Extractions");
    Heap *heap = heap_create(26);

    char letters[] = "abcdefghijklmnopqrstuvwxyz";

    for (int i = 0; i < 26; ++i) {
        heap_insert(heap, &CHAR_VAL(letters[i]), 26 - i);
        testc(tester, heap->nodes[0].value.as.character, letters[i], NULL);
        testi(tester, heap->count, i + 1, NULL);
    }

    for (int i = 0; i < 26; ++i) {

        // for (int i = 0; i < (int) heap->count; ++i) {
        //     printf("[%d]:%llu=%c ", i, heap->nodes[i].priority, heap->nodes[i].value.as.character);
        // }
        // puts("");

        testi(tester, heap->nodes[0].priority, i + 1, NULL);
        Value value = heap_extract(heap);
        testc(tester, value.as.character, letters[26 - i - 1], NULL);
        testi(tester, heap->count, 26 - i - 1, NULL);
    }

    testi(tester, heap->count, 0, "Empty");

    heap_free(heap);
}

int main() {
    Tester tester = create_tester("Heaping");

    test_heap_operations(&tester);
    test_heap_insertion(&tester);
    test_heap_extractions(&tester);

    return test_summary(&tester);
}
