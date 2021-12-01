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

Value queue_pop_front(Queue *queue) {
    if (queue->head == NULL) {
        return NIL_VAL;
    }

    QueueNode *node = queue->head;
    queue->head = node->next;

    if (queue->head == NULL) {
        queue->tail = NULL;
    }

    Value v = node->value;
    free(node);
    return v;
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

s64 queue_sum_signed(Queue *queue) {
    QueueNode *node = queue->head;
    s64 sum = 0;
    while (node) {
        sum += node->value.as.signed_64;
        node = node->next;
    }
    return sum;
}
