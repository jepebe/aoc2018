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

bool is_opening_bracket(char c) {
    return (c == '(' || c == '[' || c == '{' || c == '<');
}

bool is_closing_bracket(char c) {
    return (c == ')' || c == ']' || c == '}' || c == '>');
}

bool paired_brackets(char a, char b) {
    if (a == '(' & b == ')') {
        return true;
    } else if (a == '[' && b == ']') {
        return true;
    } else if (a == '{' && b == '}') {
        return true;
    } else if (a == '<' && b == '>') {
        return true;
    }
    return false;
}

static u64 next_pow2m1(u64 x) {
    x |= x >> 1;
    x |= x >> 2;
    x |= x >> 4;
    x |= x >> 8;
    x |= x >> 16;
    x |= x >> 32;
    return x;
}

u64 next_pow2(u64 x) {
    return next_pow2m1(x - 1) + 1;
}
