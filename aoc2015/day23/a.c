#include "aoc.h"
#include <stdint.h>
#include <string.h>

typedef struct {
    uint64_t a;
    uint64_t b;
    uint8_t pc;
    bool halted;
    char *memory[50];
} CPU;

CPU create_cpu(char *prg) {
    CPU cpu;
    cpu.a = 0;
    cpu.b = 0;
    cpu.pc = 0;
    cpu.halted = false;
    memset(cpu.memory, 0, sizeof(cpu.memory));

    size_t i = 0;
    char *token = strtok(prg, "\n");
    while (token) {
        cpu.memory[i] = token;
        token = strtok(NULL, "\n");
        i++;
    }
    return cpu;
}

char get_register(char *operand) {
    if (strncmp("a", operand, 1) == 0) {
        return 'a';
    } else if (strncmp("b", operand, 1) == 0) {
        return 'b';
    } else {
        printf("Unknown register %s\n", operand);
        return 'x';
    }
}

int get_offset(char *operand) {
    //printf("%s == %d\n", operand, atoi(operand));
    return atoi(operand);
}

void clock_cpu(CPU *cpu) {
    char *instr = cpu->memory[cpu->pc];
    if (instr == NULL) {
        cpu->halted = true;
        return;
    }

    // printf("$%02D %-10s a=%6llu b=%6llu\n", cpu->pc, instr, cpu->a, cpu->b);

    if (strncmp("inc", instr, 3) == 0) {
        char reg = get_register(instr + 4);
        if (reg == 'a') {
            cpu->a++;
        } else if (reg == 'b') {
            cpu->b++;
        }
        cpu->pc++;
    } else if (strncmp("jio", instr, 3) == 0) {
        char reg = get_register(instr + 4);
        if (reg == 'a') {
            if (cpu->a == 1) {
                cpu->pc += get_offset(instr + 6);
            } else {
                cpu->pc++;
            }
        } else if (reg == 'b') {
            if (cpu->b == 1) {
                cpu->pc += get_offset(instr + 6);
            } else {
                cpu->pc++;
            }
        }
    } else if (strncmp("jie", instr, 3) == 0) {
        char reg = get_register(instr + 4);
        if (reg == 'a') {
            if (cpu->a % 2 == 0) {
                cpu->pc += get_offset(instr + 6);
            } else {
                cpu->pc++;
            }
        } else if (reg == 'b') {
            if (cpu->b % 2 == 0) {
                cpu->pc += get_offset(instr + 6);
            } else {
                cpu->pc++;
            }
        }
    } else if (strncmp("jmp", instr, 3) == 0) {
        cpu->pc += get_offset(instr + 4);
    } else if (strncmp("tpl", instr, 3) == 0) {
        char reg = get_register(instr + 4);
        if (reg == 'a') {
            cpu->a *= 3;
        } else if (reg == 'b') {
            cpu->b *= 3;
        }
        cpu->pc++;
    } else if (strncmp("hlf", instr, 3) == 0) {
        char reg = get_register(instr + 4);
        if (reg == 'a') {
            cpu->a /= 2;
        } else if (reg == 'b') {
            cpu->b /= 2;
        }
        cpu->pc++;
    } else {
        printf("Unknown instruction %s\n", instr);
        cpu->halted = true;
    }
}

void run(CPU *cpu) {
    while (!cpu->halted) {
        clock_cpu(cpu);
    }
}

void test_1(Tester *tester) {
    char prg[] = "inc a\njio a, +2\ntpl a\ninc a";

    CPU cpu = create_cpu(prg);
    run(&cpu);
    testi(tester, cpu.a, 2, "Test 1");
}

int main() {
    Tester tester = create_tester("Opening the Turing Lock");

    test_1(&tester);

    char *prg = read_input("../aoc2015/day23/input");
    CPU cpu = create_cpu(prg);
    run(&cpu);
    testi(&tester, cpu.b, 170, "solution to part 1");

    prg = read_input("../aoc2015/day23/input");
    cpu = create_cpu(prg);
    cpu.a = 1;
    run(&cpu);
    testi(&tester, cpu.b, 247, "solution to part 2");

    return test_summary(&tester);
}
