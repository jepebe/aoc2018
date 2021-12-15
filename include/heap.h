#pragma once
#include "aoc.h"
#include "utils.h"
#include "values.h"
#include <stdint.h>
#include <stdlib.h>

typedef struct {
    s64 priority;
    Value value;
} HeapNode;

typedef struct {
    u32 capacity;
    u32 count;
    u32 last_element;
    HeapNode *nodes;
} Heap;

u32 heap_parent_index(u32 index) {
    if (index == 0) {
        return 0;
    }
    return (index - 1) / 2;
}

bool heap_index_is_root(u32 index) {
    return index == 0;
}

u32 heap_index_left(u32 index) {
    return index * 2 + 1;
}

u32 heap_index_right(u32 index) {
    return index * 2 + 2;
}

bool heap_index_is_left(u32 index) {
    return heap_index_left(heap_parent_index(index)) == index;
}

bool heap_index_is_right(u32 index) {
    return heap_index_right(heap_parent_index(index)) == index;
}

static void heap_swap(Heap *heap, u32 a, u32 b) {
    HeapNode temp_node = heap->nodes[a];
    heap->nodes[a] = heap->nodes[b];
    heap->nodes[b] = temp_node;
}

Heap *heap_create(u32 capacity) {
    Heap *heap = malloc(sizeof(Heap));
    heap->capacity = next_pow2(capacity) - 1;
    heap->count = 0;
    heap->last_element = 0;
    heap->nodes = malloc(sizeof(HeapNode) * heap->capacity);
    for (u32 i = 0; i < heap->capacity; ++i) {
        heap->nodes[i] = (HeapNode){.priority = INT32_MAX, .value = NIL_VAL};
    }
    return heap;
}

void heap_insert(Heap *heap, Value *value, u32 priority) {
    if (heap->count + 1 >= heap->capacity) {
        printf("Heap is at capacity %d\n", heap->capacity);
        return;
    }
    u32 index = heap->last_element++;
    heap->count++;

    HeapNode *node = &heap->nodes[index];
    node->priority = priority;
    node->value = *value;

    while (!heap_index_is_root(index)) {
        u32 parent = heap_parent_index(index);

        if ((&heap->nodes[parent])->priority > (&heap->nodes[index])->priority) {
            heap_swap(heap, parent, index);
        } else {
            // can't move further up -> break
            break;
        }
        index = parent;
    }
}

static bool heap_can_sieve_left(Heap *heap, u32 index) {
    u32 left = heap_index_left(index);
    if (left >= heap->last_element) {
        return false;
    }

    if (heap->nodes[left].priority > heap->nodes[index].priority) {
        return false;
    }
    return true;
}

static bool heap_can_sieve_right(Heap *heap, u32 index) {
    u32 right = heap_index_right(index);
    if (right >= heap->last_element) {
        return false;
    }

    if (heap->nodes[right].priority > heap->nodes[index].priority) {
        return false;
    }
    return true;
}

Value heap_extract(Heap *heap) {
    if (heap->count == 0) {
        printf("Heap is at empty!\n");
        return NIL_VAL;
    }

    Value result = heap->nodes[0].value;
    heap->count--;

    heap->nodes[0] = heap->nodes[--heap->last_element];
    heap->nodes[heap->last_element].priority = INT32_MAX;
    heap->nodes[heap->last_element].value = NIL_VAL;

    int index = 0;
    while (true) {
        bool can_left = heap_can_sieve_left(heap, index);
        bool can_right = heap_can_sieve_right(heap, index);
        if (can_left && can_right) {
            u32 left = heap_index_left(index);
            u32 right = heap_index_right(index);

            // the smallest value
            can_left = heap->nodes[left].priority < heap->nodes[right].priority;
        }

        if (can_left) {
            u32 left = heap_index_left(index);
            heap_swap(heap, index, left);
            index = left;
        } else if (can_right) {
            u32 right = heap_index_right(index);
            heap_swap(heap, index, right);
            index = right;
        } else {
            // we are where we are supposed to be
            break;
        }
    }

    return result;
}

bool heap_empty(Heap *heap) {
    return heap->count == 0;
}

void heap_free(Heap *heap) {
    free(heap->nodes);
}
