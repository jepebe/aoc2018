#include "aoc.h"
#include "utils.h"
#include <stdlib.h>

typedef struct {
    bool incomplete;
    bool corrupt;
    u8 round_brackets;
    u8 square_brackets;
    u8 curly_brackets;
    u8 angle_brackets;
} SyntaxError;

SyntaxError check_syntax(char *line) {
    SyntaxError se = {0};
    Queue *stack = queue_create();
    char *cur = line;
    while (*cur) {
        char next = *cur;

        if (is_opening_bracket(next)) {
            queue_append(stack, CHAR_VAL(next));
        }

        if (is_closing_bracket(next)) {
            char top = queue_pop_back(stack).as.character;
            if (!paired_brackets(top, next)) {
                se.corrupt = true;

                if (next == ')') {
                    se.round_brackets++;
                } else if (next == ']') {
                    se.square_brackets++;
                } else if (next == '}') {
                    se.curly_brackets++;
                } else if (next == '>') {
                    se.angle_brackets++;
                }
                break;
            }
        }

        cur++;
    }

    if (!se.corrupt && queue_length(stack) > 0) {
        se.incomplete = true;
    }

    queue_free(stack);
    return se;
}

// Scores the syntax errors but also removes corrputed lines from input queue
int score_syntax_errors(Queue *lines) {
    int score = 0;
    QueueNode *node = lines->head;
    while (node) {
        char *line = node->value.as.string;
        SyntaxError error = check_syntax(line);
        if (error.corrupt) {
            score += error.round_brackets * 3;
            score += error.square_brackets * 57;
            score += error.curly_brackets * 1197;
            score += error.angle_brackets * 25137;

            QueueNode *temp = node;
            node = node->next;
            queue_remove_node(lines, temp);
        } else {
            node = node->next;
        }
    }
    return score;
}

u64 autocomplete(char *line) {
    Queue *stack = queue_create();
    char *cur = line;
    while (*cur) {
        char next = *cur;
        if (is_opening_bracket(next)) {
            queue_append(stack, CHAR_VAL(next));
        }

        if (is_closing_bracket(next)) {
            char top = queue_pop_back(stack).as.character;
            if (!paired_brackets(top, next)) {
                printf("unexpected corruption\n");
            }
        }

        cur++;
    }
    u64 score = 0;
    while (queue_length(stack) > 0) {
        char top = queue_pop_back(stack).as.character;
        if (top == '(') {
            score *= 5;
            score += 1;
        } else if (top == '[') {
            score *= 5;
            score += 2;
        } else if (top == '{') {
            score *= 5;
            score += 3;
        } else if (top == '<') {
            score *= 5;
            score += 4;
        } else {
            printf("skipping %c\n", top);
        }
    }

    queue_free(stack);
    return score;
}

int compare_function(const void *a, const void *b) {
    u64 arg1 = *(const u64 *)a;
    u64 arg2 = *(const u64 *)b;

    if (arg1 < arg2)
        return -1;
    if (arg1 > arg2)
        return 1;
    return 0;
}

typedef struct {
    u64 *data;
    int count;
} ArrayU64;

void scoring(Value *value, void *ctx) {
    ArrayU64 *array = (ArrayU64 *)ctx;
    u64 score = autocomplete(value->as.string);
    array->data[array->count++] = score;
}

u64 score_autocomplete(Queue *lines) {
    ArrayU64 array;
    array.count = 0;
    array.data = (u64 *)malloc(sizeof(u64) * queue_length(lines));

    queue_map(lines, scoring, &array);

    qsort(array.data, array.count, sizeof(u64), compare_function);

    u64 score = array.data[array.count / 2];
    free(array.data);
    return score;
}

void test_examples(Tester *tester) {
    test_section("Examples Part 1");

    SyntaxError se = check_syntax("{([(<{}[<>[]}>{[]{[(<()>");
    test(tester, se.corrupt, "corrupt");
    testi(tester, se.curly_brackets, 1, "curly brackets");

    char *data = read_input("../aoc2021/day10/test");
    Queue *lines = read_lines(data);
    int score = score_syntax_errors(lines);
    testi(tester, score, 26397, "score");

    test_section("Examples Part 2");

    score = autocomplete("[({(<(())[]>[[{[]{<()<>>");
    testi(tester, score, 288957, "score");

    score = autocomplete("[(()[<>])]({[<{<<[]>>(");
    testi(tester, score, 5566, "score");

    score = score_autocomplete(lines);
    testi(tester, score, 288957, "total score");
}

int main() {
    Tester tester = create_tester("Syntax Scoring");
    test_examples(&tester);

    test_section("Solutions");

    char *data = read_input("../aoc2021/day10/input");
    Queue *lines = read_lines(data);
    int score = score_syntax_errors(lines);

    testi(&tester, score, 366027, "solution to part 1");

    score = score_autocomplete(lines);
    testi(&tester, score, 1118645287, "solution to part 2");

    return test_summary(&tester);
}
