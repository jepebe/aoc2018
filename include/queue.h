#pragma once
#include "aoc.h"
#include "values.h"
#include <stdlib.h>

typedef struct QueueNode {
    struct QueueNode *previous;
    struct QueueNode *next;
    Value value;
} QueueNode;

typedef struct {
    QueueNode *head;
    QueueNode *tail;
} Queue;

typedef void (*QueueVisitorFunc)(Value *, void *);

Queue *queue_create() {
    Queue *q = (Queue *)malloc(sizeof(Queue));
    q->head = NULL;
    q->tail = NULL;
    return q;
}

void queue_append(Queue *queue, Value value) {
    QueueNode *q = (QueueNode *)malloc(sizeof(QueueNode));

    q->previous = queue->tail;
    q->next = NULL;
    q->value = value;

    if (queue->head == NULL) {
        queue->head = q;
    } else {
        queue->tail->next = q;
    }

    queue->tail = q;
}

int queue_length(Queue *queue) {
    QueueNode *node = queue->head;
    int count = 0;
    while (node) {
        node = node->next;
        count++;
    }
    return count;
}

bool queue_empty(Queue *queue) {
    return queue->head == NULL;
}

void queue_insert_before(Queue *queue, QueueNode *node, Value value) {
    if (node == queue->head) {
        queue_append(queue, value);
    } else {
        QueueNode *q = (QueueNode *)malloc(sizeof(QueueNode));

        q->previous = node->previous;
        q->next = node;
        q->value = value;

        node->previous = q;
        q->previous->next = q;
    }
}

Value queue_pop_front(Queue *queue) {
    if (queue->head == NULL) {
        return NIL_VAL;
    }

    QueueNode *node = queue->head;
    queue->head = node->next;

    if (queue->head == NULL) {
        queue->tail = NULL;
    } else {
        queue->head->previous = NULL;
    }

    Value v = node->value;
    free(node);
    return v;
}

Value queue_pop_back(Queue *queue) {
    if (queue->tail == NULL) {
        return NIL_VAL;
    }

    QueueNode *node = queue->tail;
    queue->tail = node->previous;

    if (queue->tail == NULL) {
        queue->head = NULL;
    } else {
        queue->tail->next = NULL;
    }

    Value v = node->value;
    free(node);
    return v;
}

void queue_remove_node(Queue *queue, QueueNode *node) {
    if (node->next == NULL) {
        queue->tail = node->previous;

        if (node->previous != NULL) {
            node->previous->next = NULL;
        }
    }

    if (node->previous == NULL) {
        queue->head = node->next;

        if (node->next != NULL) {
            node->next->previous = NULL;
        }
    }

    if (node->next != NULL && node->previous != NULL) {
        node->previous->next = node->next;
        node->next->previous = node->previous;
    }
    free(node);
}

void queue_add_all(Queue *q, Queue *from) {
    QueueNode *node = from->head;
    while (node) {
        queue_append(q, node->value);
        node = node->next;
    }
}

void queue_free(Queue *queue) {
    QueueNode *node = queue->head;
    while (node) {
        QueueNode *free_node = node;
        node = node->next;
        free(free_node);
    }
    free(queue);
}

void queue_visit(Queue *queue, QueueVisitorFunc vf, void *ctx) {
    QueueNode *node = queue->head;
    while (node) {
        vf(&node->value, ctx);
        node = node->next;
    }
}

static void signed_sum(Value *value, void *sum_ptr) {
    (*((s64 *)sum_ptr)) += value->as.signed_64;
}

s64 queue_sum_signed(Queue *queue) {
    s64 sum = 0;
    queue_visit(queue, signed_sum, &sum);
    return sum;
}

// allocates a string from the queue interpreting all values as char
char *queue_as_string(Queue *queue) {
    char *word = malloc(sizeof(char) * queue_length(queue) + 1);

    int n = 0;
    QueueNode *node = queue->head;
    while (node) {
        word[n++] = node->value.as.character;
        node = node->next;
    }
    word[n] = '\0';
    return word;
}
