#pragma once
#include "aoc.h"
#include "queue.h"

typedef Value (*LineFormatter)(char *);

Queue *read_lines(char *content) {
    Queue *q = queue_create();

    char *token = strtok(content, "\n");
    while (token) {
        queue_append(q, STRING_VAL(token));

        token = strtok(NULL, "\n");
    }
    return q;
}

Queue *read_lines_fmt(char *content, LineFormatter fmt) {
    Queue *q = queue_create();

    char *token = strtok(content, "\n");
    while (token) {
        Value value = fmt(token);
        queue_append(q, value);

        token = strtok(NULL, "\n");
    }
    return q;
}

static Value int_line_fmt(char *line) {
    return SIGNED_VAL(atoi(line));
}

Queue *read_lines_as_ints(char *content) {
    return read_lines_fmt(content, int_line_fmt);
}
