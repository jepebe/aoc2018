#include "aoc.h"
#include "utils.h"
#include <string.h>

typedef struct {
    s64 horizontal;
    s64 depth;
    s64 aim;
    u64 pc;
    bool halted;
    bool use_aim;
    char *commands[1001];
} Sub;

Sub create_sub(char *cmds) {
    Sub s;
    s.horizontal = 0;
    s.depth = 0;
    s.aim = 0;
    s.pc = 0;
    s.halted = false;
    s.use_aim = false;
    Queue *q = read_lines(cmds);
    int i = 0;
    while (!queue_empty(q)) {
        s.commands[i] = queue_pop_front(q).as.string;
        i++;
    }
    for (; i < 1001; ++i) {
        s.commands[i] = NULL;
    }
    queue_free(q);
    return s;
}

bool string_has_prefix(char *prefix, char *str) {
    return strncmp(prefix, str, strlen(prefix)) == 0;
}

void dive_step(Sub *sub) {
    char *instr = sub->commands[sub->pc];

    if (instr == NULL) {
        sub->halted = true;
        return;
    }

    if (string_has_prefix("up", instr)) {
        s64 value = atoi(instr + 2);
        if (sub->use_aim) {
            sub->aim -= value;
        } else {
            sub->depth -= value;
        }
    } else if (string_has_prefix("down", instr)) {
        s64 value = atoi(instr + 4);
        if (sub->use_aim) {
            sub->aim += value;
        } else {
            sub->depth += value;
        }
    } else if (string_has_prefix("forward", instr)) {
        s64 value = atoi(instr + 7);
        sub->horizontal += value;
        if (sub->use_aim) {
            sub->depth += sub->aim * value;
        }
    }
    sub->pc++;
}

void dive(Sub *sub) {
    while (!sub->halted) {
        // printf("d=%lld h=%lld aim=%lld\n", sub->depth, sub->horizontal, sub->aim);
        dive_step(sub);
    }
}

void test_dive(Tester *tester) {
    test_section("Examples");
    char cmds[] = "forward 5\ndown 5\nforward 8\nup 3\ndown 8\nforward 2\n";
    Sub sub = create_sub(cmds);
    dive(&sub);
    testi(tester, sub.depth * sub.horizontal, 150, "test");

    char cmds2[] = "forward 5\ndown 5\nforward 8\nup 3\ndown 8\nforward 2\n";
    sub = create_sub(cmds2);
    sub.use_aim = true;
    dive(&sub);
    testi(tester, sub.depth * sub.horizontal, 900, "test");
}

int main() {
    Tester tester = create_tester("Dive!");
    test_dive(&tester);

    test_section("Solutions");

    char *commands = read_input("../aoc2021/day2/input");
    Sub sub = create_sub(commands);
    dive(&sub);
    testi(&tester, sub.depth * sub.horizontal, 1654760, "solution to part 1");
    free(commands);

    commands = read_input("../aoc2021/day2/input");
    sub = create_sub(commands);
    sub.use_aim = true;
    dive(&sub);
    testi(&tester, sub.depth * sub.horizontal, 1956047400, "solution to part 2");
    free(commands);

    return test_summary(&tester);
}
