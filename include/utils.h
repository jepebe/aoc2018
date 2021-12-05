#pragma once
#include "aoc.h"
#include "queue.h"
#include <stdlib.h>

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

char *replace_char(char *str, char find, char replace) {
    char *current_pos = strchr(str, find);
    while (current_pos) {
        *current_pos = replace;
        current_pos = strchr(current_pos, find);
    }
    return str;
}

char *x_strchr(char *data, char find, int line) {
    char *found = strchr(data, find);
    if (!found) {
        printf("[%d] Did not find '%c' in '%s'\n", line, find, data);
        exit(EXIT_FAILURE);
    }
    return found;
}

long x_strtol(char *data, int base, char **end, int line) {
    long value = strtol(data, end, base);

    // || *end != '\0'
    if (*end == data || errno == ERANGE) {
        printf("[%d] Did not find an integer at '%s'\n", line, data);
        exit(EXIT_FAILURE);
    }
    return value;
}
