#include "aoc.h"
#include "utils.h"
#include <stdio.h>
#include <stdlib.h>

typedef struct SnailNum SnailNum;

struct SnailNum {
    SnailNum *parent;
    union {
        u32 value;
        SnailNum *pair;
    } left;

    union {
        u32 value;
        SnailNum *pair;
    } right;

    bool left_is_pair;
    bool right_is_pair;
};

typedef struct {
    char *data;
    int index;
} Parser;

void print_snail_number(SnailNum *snail, bool newline) {
    printf("[");
    if (!snail->left_is_pair) {
        printf("%d", snail->left.value);
    } else {
        print_snail_number(snail->left.pair, false);
    }

    printf(",");

    if (!snail->right_is_pair) {
        printf("%d", snail->right.value);
    } else {
        print_snail_number(snail->right.pair, false);
    }
    printf("]");
    if (newline) {
        puts("");
    }
}

u8 parsenum(Parser *parser) {
    u8 value = 0;
    char c = parser->data[parser->index];
    while ('0' <= c && c <= '9') {
        value *= 10;
        value += c - '0';
        parser->index++;
        c = parser->data[parser->index];
    }
    return value;
}

SnailNum *parse_snail_num(Parser *parser, SnailNum *parent) {
    SnailNum *snail = malloc(sizeof(SnailNum));
    snail->parent = parent;

    if (parser->data[parser->index] != '[') {
        printf("[ Unexpected '%c' at %d\n", parser->data[parser->index], parser->index);
    }

    parser->index++; // skip [

    if (parser->data[parser->index] == '[') {
        snail->left.pair = parse_snail_num(parser, snail);
        snail->left_is_pair = true;
    } else {
        snail->left.value = parsenum(parser);
        snail->left_is_pair = false;
    }

    if (parser->data[parser->index] != ',') {
        printf(", Unexpected '%c' at %d\n", parser->data[parser->index], parser->index);
    }

    parser->index++; // skip ,

    if (parser->data[parser->index] == '[') {
        snail->right.pair = parse_snail_num(parser, snail);
        snail->right_is_pair = true;
    } else {
        snail->right.value = parsenum(parser);
        snail->right_is_pair = false;
    }

    if (parser->data[parser->index] != ']') {
        printf("] Unexpected '%c' at %d\n", parser->data[parser->index], parser->index);
    }

    parser->index++; // skip ]

    return snail;
}

SnailNum *parse_snail_number(char *data) {
    Parser parser;
    parser.data = data;
    parser.index = 0;
    return parse_snail_num(&parser, NULL);
}

SnailNum *add_snailnums(SnailNum *a, SnailNum *b) {
    SnailNum *sum = malloc(sizeof(SnailNum));
    sum->parent = NULL;
    sum->left.pair = a;
    sum->left_is_pair = true;
    sum->right.pair = b;
    sum->right_is_pair = true;
    a->parent = sum;
    b->parent = sum;
    return sum;
}

bool compare_snailnum(SnailNum *a, SnailNum *b) {
    if (a->left_is_pair && b->left_is_pair) {
        if (!compare_snailnum(a->left.pair, b->left.pair)) {
            return false;
        }
    } else if (!a->left_is_pair && !b->left_is_pair) {
        if (a->left.value != b->left.value) {
            return false;
        }
    } else {
        return false;
    }

    if (a->right_is_pair && b->right_is_pair) {
        if (!compare_snailnum(a->right.pair, b->right.pair)) {
            return false;
        }
    } else if (!a->right_is_pair && !b->right_is_pair) {
        if (a->right.value != b->right.value) {
            return false;
        }
    } else {
        return false;
    }

    return true;
}

bool compare_snail_num_to_chars(SnailNum *a, char *b) {
    SnailNum *num = parse_snail_number(b);
    bool equal = compare_snailnum(a, num);
    if (!equal) {
        printf("got     ");
        print_snail_number(a, true);
        printf("expectd ");
        print_snail_number(num, true);
    }
    return equal;
}

void assign_left(SnailNum *node, u32 value) {
    while (node) {
        SnailNum *parent = node->parent;
        if (parent && parent->left_is_pair && parent->left.pair != node) {
            node = parent->left.pair;
            break;
        }

        if (parent && !parent->left_is_pair) {
            parent->left.value += value;
            return;
        }
        node = parent;
    }

    if (!node) {
        return;
    }

    // find the first regular number
    while (node->right_is_pair) {
        node = node->right.pair;
    }
    node->right.value += value;
}

void assign_right(SnailNum *node, u32 value) {
    while (node) {
        SnailNum *parent = node->parent;
        if (parent && parent->right_is_pair && parent->right.pair != node) {
            node = parent->right.pair;
            break;
        }

        if (parent && !parent->right_is_pair) {
            parent->right.value += value;
            return;
        }
        node = parent;
    }

    if (!node) {
        return;
    }

    // find the first regular number
    while (node->left_is_pair) {
        node = node->left.pair;
    }
    node->left.value += value;
}

bool snail_exploder(SnailNum *snail, int depth) {
    if (depth == 4) {
        // printf("explode [%d,%d]\n", snail->left.value, snail->right.value);
        if (!snail->parent->left_is_pair) {
            snail->parent->left.value += snail->left.value;
        } else {
            assign_left(snail, snail->left.value);
        }

        if (!snail->parent->right_is_pair) {
            snail->parent->right.value += snail->right.value;
        } else {
            assign_right(snail, snail->right.value);
        }

        SnailNum *parent = snail->parent;
        if (parent->left_is_pair && parent->left.pair == snail) {
            parent->left_is_pair = false;
            parent->left.value = 0;
        } else {
            parent->right_is_pair = false;
            parent->right.value = 0;
        }
        free(snail);

        return true;
    }
    bool exploded = false;

    if (snail->left_is_pair) {
        exploded = snail_exploder(snail->left.pair, depth + 1);
    }
    if (!exploded && snail->right_is_pair) {
        exploded = snail_exploder(snail->right.pair, depth + 1);
    }
    return exploded;
}

SnailNum *split(SnailNum *parent, u32 value) {
    SnailNum *snail = malloc(sizeof(SnailNum));
    snail->parent = parent;
    snail->left.value = value / 2;
    snail->right.value = value / 2 + (value % 2);
    snail->left_is_pair = false;
    snail->right_is_pair = false;
    return snail;
}

bool snail_splitter(SnailNum *snail) {
    if (!snail->left_is_pair && snail->left.value > 9) {
        snail->left.pair = split(snail, snail->left.value);
        snail->left_is_pair = true;
        return true;
    }

    bool splitted = false;
    if (snail->left_is_pair) {
        splitted = snail_splitter(snail->left.pair);
    }

    if (!splitted && !snail->right_is_pair && snail->right.value > 9) {
        snail->right.pair = split(snail, snail->right.value);
        snail->right_is_pair = true;
        return true;
    }

    if (!splitted && snail->right_is_pair) {
        splitted = snail_splitter(snail->right.pair);
    }

    return splitted;
}

void reduce(SnailNum *num, bool debug) {
    if (debug) {
        printf("reduce  ");
        print_snail_number(num, true);
    }

    int operations;
    do {
        operations = 0;

        while (snail_exploder(num, 0)) {
            if (debug) {
                printf("explode ");
                print_snail_number(num, true);
            }
            operations += 1;
        }

        bool split = snail_splitter(num);
        if (split && debug) {
            printf("split   ");
            print_snail_number(num, true);
        }
        operations += split;

    } while (operations > 0);
}

SnailNum *snails_from_file(char *file) {
    char *data = read_input(file);
    Queue *q = read_lines(data);
    QueueNode *node = q->head;

    SnailNum *num = parse_snail_number(node->value.as.string);
    node = node->next;
    while (node) {
        SnailNum *b = parse_snail_number(node->value.as.string);
        num = add_snailnums(num, b);
        reduce(num, false);
        node = node->next;
    }

    return num;
}

u64 magnitude(SnailNum *snail) {
    u64 left = snail->left_is_pair ? magnitude(snail->left.pair) : snail->left.value;
    u64 right = snail->right_is_pair ? magnitude(snail->right.pair) : snail->right.value;
    return 3 * left + 2 * right;
}

u64 find_max_magnitude(char *file) {
    char *data = read_input(file);
    Queue *q = read_lines(data);

    int count = 0;
    char *num_string[queue_length(q)];
    QueueNode *node = q->head;
    while (node) {
        num_string[count++] = node->value.as.string;
        node = node->next;
    }

    u64 max_magnitude = 0;
    for(int j = 0; j < count; ++j) {
        for(int i = 0; i < count; ++i) {
            if(i == j) {
                continue;
            }
            SnailNum *a = parse_snail_number(num_string[i]);
            SnailNum *b = parse_snail_number(num_string[j]);
            SnailNum *sum = add_snailnums(a, b);
            reduce(sum, false);
            u64 m = magnitude(sum);
            if(m > max_magnitude) {
                max_magnitude = m;
            }
        }
    }

    return max_magnitude;

}

void test_explode(Tester *tester, char *a, char *b) {
    SnailNum *exploded = parse_snail_number(a);
    SnailNum *expected = parse_snail_number(b);
    //print_snail_number(exploded, true);
    snail_exploder(exploded, 0);
    bool equal = compare_snailnum(exploded, expected);
    if (!equal) {
        printf("got      ");
        print_snail_number(exploded, true);
        printf("expected ");
        print_snail_number(expected, true);
    }
    test(tester, equal, "");
}

void test_examples(Tester *tester) {
    test_section("Examples Part 1");

    SnailNum *a = parse_snail_number("[1,2]");
    test(tester, !a->left_is_pair, "");
    testi(tester, a->left.value, 1, "");
    test(tester, !a->right_is_pair, "");
    testi(tester, a->right.value, 2, "");
    test(tester, a->parent == NULL, "");

    SnailNum *b = parse_snail_number("[[1,2],3]");
    test(tester, b->left_is_pair, "");
    test(tester, b->left.pair->parent == b, "");
    testi(tester, b->left.pair->left.value, 1, "");
    testi(tester, b->left.pair->right.value, 2, "");
    test(tester, !b->right_is_pair, "");
    testi(tester, b->right.value, 3, "");

    SnailNum *c = parse_snail_number("[[3,4],5]");
    SnailNum *e = add_snailnums(a, c);
    test(tester, compare_snail_num_to_chars(e, "[[1,2],[[3,4],5]]"), "");

    SnailNum *s = split(NULL, 10);
    testi(tester, s->left.value, 5, "split 10");
    testi(tester, s->right.value, 5, "");
    s = split(NULL, 11);
    testi(tester, s->left.value, 5, "split 11");
    testi(tester, s->right.value, 6, "");
    s = split(NULL, 12);
    testi(tester, s->left.value, 6, "split 12");
    testi(tester, s->right.value, 6, "");

    test_section("Examples Part 1 Explosions");
    test_explode(tester, "[[[[[9,8],1],2],3],4]", "[[[[0,9],2],3],4]");
    test_explode(tester, "[7,[6,[5,[4,[3,2]]]]]", "[7,[6,[5,[7,0]]]]");
    test_explode(tester, "[[6,[5,[4,[3,2]]]],1]", "[[6,[5,[7,0]]],3]");
    test_explode(tester, "[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]", "[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]");
    test_explode(tester, "[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]", "[[3,[2,[8,0]]],[9,[5,[7,0]]]]");

    test_section("Examples Part 1 Operations");
    a = parse_snail_number("[[[[4,3],4],4],[7,[[8,4],9]]]");
    b = parse_snail_number("[1,1]");
    c = add_snailnums(a, b);
    test(tester, compare_snail_num_to_chars(c, "[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]"), "after add");
    snail_exploder(c, 0);
    test(tester, compare_snail_num_to_chars(c, "[[[[0,7],4],[7,[[8,4],9]]],[1,1]]"), "after explode");
    snail_exploder(c, 0);
    test(tester, compare_snail_num_to_chars(c, "[[[[0,7],4],[15,[0,13]]],[1,1]]"), "after explode");
    snail_splitter(c);
    test(tester, compare_snail_num_to_chars(c, "[[[[0,7],4],[[7,8],[0,13]]],[1,1]]"), "after split");
    snail_splitter(c);
    test(tester, compare_snail_num_to_chars(c, "[[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]"), "after split");
    snail_exploder(c, 0);
    test(tester, compare_snail_num_to_chars(c, "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]"), "after explode");

    SnailNum *result = snails_from_file("../aoc2021/day18/test1");
    test(tester, compare_snail_num_to_chars(result, "[[[[1,1],[2,2]],[3,3]],[4,4]]"), "test 1");

    result = snails_from_file("../aoc2021/day18/test2");
    test(tester, compare_snail_num_to_chars(result, "[[[[3,0],[5,3]],[4,4]],[5,5]]"), "test 2");

    result = snails_from_file("../aoc2021/day18/test3");
    test(tester, compare_snail_num_to_chars(result, "[[[[5,0],[7,4]],[5,5]],[6,6]]"), "test 3");

    a = parse_snail_number("[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]");
    b = parse_snail_number("[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]");
    c = add_snailnums(a, b);
    reduce(c, false);
    char *expected = "[[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]";
    test(tester, compare_snail_num_to_chars(c, expected), "test step 1");

    a = parse_snail_number(expected);
    b = parse_snail_number("[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]");
    c = add_snailnums(a, b);
    reduce(c, false);
    expected = "[[[[6,7],[6,7]],[[7,7],[0,7]]],[[[8,7],[7,7]],[[8,8],[8,0]]]]";
    test(tester, compare_snail_num_to_chars(c, expected), "test step 2");

    a = parse_snail_number(expected);
    b = parse_snail_number("[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]");
    c = add_snailnums(a, b);
    reduce(c, false);
    expected = "[[[[7,0],[7,7]],[[7,7],[7,8]]],[[[7,7],[8,8]],[[7,7],[8,7]]]]";
    test(tester, compare_snail_num_to_chars(c, expected), "test step 3");

    a = parse_snail_number(expected);
    b = parse_snail_number("[7,[5,[[3,8],[1,4]]]]");
    c = add_snailnums(a, b);
    reduce(c, false);
    expected = "[[[[7,7],[7,8]],[[9,5],[8,7]]],[[[6,8],[0,8]],[[9,9],[9,0]]]]";
    test(tester, compare_snail_num_to_chars(c, expected), "test step 4");

    a = parse_snail_number(expected);
    b = parse_snail_number("[[2,[2,2]],[8,[8,1]]]");
    c = add_snailnums(a, b);
    reduce(c, false);
    expected = "[[[[6,6],[6,6]],[[6,0],[6,7]]],[[[7,7],[8,9]],[8,[8,1]]]]";
    test(tester, compare_snail_num_to_chars(c, expected), "test step 5");

    a = parse_snail_number(expected);
    b = parse_snail_number("[2,9]");
    c = add_snailnums(a, b);
    reduce(c, false);
    expected = "[[[[6,6],[7,7]],[[0,7],[7,7]]],[[[5,5],[5,6]],9]]";
    test(tester, compare_snail_num_to_chars(c, expected), "test step 6");

    result = snails_from_file("../aoc2021/day18/test");
    expected = "[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]";
    test(tester, compare_snail_num_to_chars(result, expected), "test");

    test_section("Examples Part 1 Magnitude");
    SnailNum *m1 = parse_snail_number("[[1,2],[[3,4],5]]");
    SnailNum *m2 = parse_snail_number("[[[[0,7],4],[[7,8],[6,0]]],[8,1]]");
    SnailNum *m3 = parse_snail_number(expected);
    test_u64(tester, magnitude(m1), 143, "");
    test_u64(tester, magnitude(m2), 1384, "");
    test_u64(tester, magnitude(m3), 3488, "");

    result = snails_from_file("../aoc2021/day18/test_final");
    expected = "[[[[6,6],[7,6]],[[7,7],[7,0]]],[[[7,7],[7,7]],[[7,8],[9,9]]]]";
    test(tester, compare_snail_num_to_chars(result, expected), "test final");
    test_u64(tester, magnitude(result), 4140, "");

    test_section("Examples Part 2");

    testi(tester, find_max_magnitude("../aoc2021/day18/test_final"), 3993, "");
}

int main() {
    Tester tester = create_tester("Snailfish");
    test_examples(&tester);

    test_section("Solutions");

    char *input = "../aoc2021/day18/input";
    SnailNum *result = snails_from_file(input);

    testi(&tester, magnitude(result), 4457, "solution to part 1");
    testi(&tester, find_max_magnitude(input), 4784, "solution to part 2");

    return test_summary(&tester);
}
