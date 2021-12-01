#include "aoc.h"
#include <string.h>

typedef struct {
    s64 a;
    s64 b;
    s64 c;
    s64 d;
    u8 pc;
    bool halted;
    char *memory[50];
} CPU;

CPU create_cpu(char *prg) {
    CPU cpu;
    cpu.a = 0;
    cpu.b = 0;
    cpu.c = 0;
    cpu.d = 0;
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

s64 *cpu_get_register(CPU *cpu, char *operand) {
    if (strncmp("a", operand, 1) == 0) {
        return &cpu->a;
    } else if (strncmp("b", operand, 1) == 0) {
        return &cpu->b;
    } else if (strncmp("c", operand, 1) == 0) {
        return &cpu->c;
    } else if (strncmp("d", operand, 1) == 0) {
        return &cpu->d;
    } else {
        //printf("Unknown register %s\n", operand);
        return NULL;
    }
}

char* cpu_next_operand(char * operands) {
    int count = 0;
    while(*(operands + count) != ' ') {
        count++;
    }
    return operands + count + 1;
}

void cpu_clock(CPU *cpu) {
    char *instr = cpu->memory[cpu->pc];
    if (instr == NULL) {
        cpu->halted = true;
        return;
    }

    //printf("$%02D %-10s a=%6llu b=%6llu\n", cpu->pc, instr, cpu->a, cpu->b);

    if (strncmp("inc", instr, 3) == 0) {
        s64 *reg = cpu_get_register(cpu, instr + 4);
        (*(reg))++;
        cpu->pc++;
    } else if (strncmp("dec", instr, 3) == 0) {
        s64 *reg = cpu_get_register(cpu, instr + 4);
        (*(reg))--;
        cpu->pc++;
    } else if (strncmp("cpy", instr, 3) == 0) {
        s64 *src = cpu_get_register(cpu, instr + 4);
        if (src != NULL) {
            s64 *dst = cpu_get_register(cpu, instr + 6);
            *dst = *src;
        } else {
            s64 value = atoi(instr + 4);
            char* next = cpu_next_operand(instr + 4);
            s64 *dst = cpu_get_register(cpu, next);
            *dst = value;
        }

        cpu->pc++;
    } else if (strncmp("jnz", instr, 3) == 0) {
        s64 value = 0;
        s64 *reg = cpu_get_register(cpu, instr + 4);
        if (reg != NULL) {
            value = *reg;
        } else {
            value = atoi(instr + 4);
        }

        if (value != 0) {
            char* next = cpu_next_operand(instr + 4);
            int offset = atoi(next);
            cpu->pc += offset;
        } else {
            cpu->pc++;
        }
        //printf("PC %llu\n", cpu->pc);

    } else {
        printf("Unknown instruction %s\n", instr);
        cpu->halted = true;
    }
}

void cpu_run(CPU *cpu) {
    while (!cpu->halted) {
        cpu_clock(cpu);
    }
}

void test_1(Tester *tester) {
    char prg[] = "cpy 41 a\ninc a\ninc a\ndec a\njnz a 2\ndec a";
    CPU cpu = create_cpu(prg);

    cpu_run(&cpu);
    testi(tester, cpu.a, 42, "test");
}

int main() {
    Tester tester = create_tester("Leonardo's Monorail");

    test_1(&tester);

    char *prg = read_input("../aoc2016/day12/input");
    CPU cpu = create_cpu(prg);

    cpu_run(&cpu);
    testi(&tester, cpu.a, 318007, "solution to part 1");

    prg = read_input("../aoc2016/day12/input");
    cpu = create_cpu(prg);
    cpu.c = 1;

    cpu_run(&cpu);
    testi(&tester, cpu.a, 9227661, "solution to part 2");

    return test_summary(&tester);
}
