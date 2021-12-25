#include "aoc.h"
#include "dict.h"
#include "utils.h"
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

typedef enum {
    INP,
    ADD,
    DIV,
    MUL,
    MOD,
    EQL,
    HALT
} InstructionType;

typedef enum {
    REG_W,
    REG_X,
    REG_Y,
    REG_Z,
    VALUE
} OperandType;

typedef struct {
    InstructionType instruction_type;
    OperandType operand_1;
    OperandType operand_2;
    s64 literal;
} Instruction;

typedef struct {
    s64 w;
    s64 x;
    s64 y;
    s64 z;
    u32 pc;
    u8 input_index;
    u8 input[14];
    bool halted;
    u16 program_size;
    Instruction program[255];
} ALU;

InstructionType parse_instruction_type(char *instr) {
    switch (instr[0]) {
    case 'a':
        return ADD;
    case 'i':
        return INP;
    case 'd':
        return DIV;
    case 'e':
        return EQL;
    case 'm':
        if (instr[1] == 'u') {
            return MUL;
        } else if (instr[1] == 'o') {
            return MOD;
        }
    default:
        printf("Unknown instruction: %s\n", instr);
        return HALT;
    }
}

OperandType parse_operand_type(char *instr) {
    switch (instr[0]) {
    case 'w':
        return REG_W;
    case 'x':
        return REG_X;
    case 'y':
        return REG_Y;
    case 'z':
        return REG_Z;
    default:
        return VALUE;
    }
}

ALU *create_alu(char *file) {
    ALU *alu = malloc(sizeof(ALU));
    alu->halted = false;
    alu->program_size = 0;

    char *data = read_input(file);
    Queue *lines = read_lines(data);
    QueueNode *node = lines->head;

    while (node) {
        Instruction *instruction = &alu->program[alu->program_size++];
        char *instr = node->value.as.string;

        instruction->instruction_type = parse_instruction_type(instr);
        instruction->operand_1 = parse_operand_type(&instr[4]);
        if (instr[5] == ' ') {
            instruction->operand_2 = parse_operand_type(&instr[6]);

            if (instruction->operand_2 == VALUE) {
                instruction->literal = atoi(&instr[6]);
            }
        }

        node = node->next;
    }

    free(data);
    queue_free(lines);
    return alu;
}

void alu_halt(ALU *alu) {
    alu->halted = true;
}

void alu_inp(ALU *alu, s64 *reg) {
    if (alu->input_index >= 14) {
        printf("-->inp $%p\n", (void *)reg);
        alu_halt(alu);
    } else if (alu->input[alu->input_index] == 0) {
        alu_halt(alu);
    } else {
        *reg = alu->input[alu->input_index++];
    }
}

void alu_add(ALU *alu, s64 *reg, s64 value) {
    (void)alu;
    *reg += value;
}

void alu_mul(ALU *alu, s64 *reg, s64 value) {
    (void)alu;
    *reg *= value;
}

void alu_div(ALU *alu, s64 *reg, s64 value) {
    (void)alu;
    if (value == 0) {
        printf("-->div $%p=%llu + %llu\n", (void *)reg, *reg, value);
        alu_halt(alu);
    } else {
        *reg /= value;
    }
}

void alu_mod(ALU *alu, s64 *reg, s64 value) {
    (void)alu;
    if (*reg < 0 || value <= 0) {
        printf("-->mod $%p=%llu + %llu\n", (void *)reg, *reg, value);
        alu_halt(alu);
    } else {
        *reg = *reg % value;
    }
}

void alu_eql(ALU *alu, s64 *reg, s64 value) {
    (void)alu;
    *reg = *reg == value;
}

s64 *get_register(ALU *alu, Instruction *instr) {
    switch (instr->operand_1) {
    case REG_W:
        return &alu->w;
    case REG_X:
        return &alu->x;
    case REG_Y:
        return &alu->y;
    case REG_Z:
        return &alu->z;
    default:
        printf("Unknown register %c\n", instr->operand_1);
        return NULL;
    }
}

s64 get_value(ALU *alu, Instruction *instr) {
    switch (instr->operand_2) {
    case REG_W:
        return alu->w;
    case REG_X:
        return alu->x;
    case REG_Y:
        return alu->y;
    case REG_Z:
        return alu->z;
    case VALUE:
        return instr->literal;
    default:
        printf("Unknown value %c\n", instr->operand_2);
        return 0;
    }
}

void run(ALU *alu, bool debug) {
    alu->halted = false;
    alu->pc = 0;
    alu->w = 0;
    alu->x = 0;
    alu->y = 0;
    alu->z = 0;
    alu->input_index = 0;

    if (debug) {
        printf("program size = %d\n", alu->program_size);
        printf("input = ");
        for (int i = 0; i < 14; ++i) {
            printf("%d ", alu->input[i]);
        }
        puts("");
    }
    while (!alu->halted) {
        Instruction *instr = &alu->program[alu->pc++];

        switch (instr->instruction_type) {
        case ADD:
            alu_add(alu, get_register(alu, instr), get_value(alu, instr));
            break;
        case INP:
            alu_inp(alu, get_register(alu, instr));
            break;
        case DIV:
            alu_div(alu, get_register(alu, instr), get_value(alu, instr));
            break;
        case EQL:
            alu_eql(alu, get_register(alu, instr), get_value(alu, instr));
            break;
        case MUL:
            alu_mul(alu, get_register(alu, instr), get_value(alu, instr));
            break;
        case MOD:
            alu_mod(alu, get_register(alu, instr), get_value(alu, instr));
            break;
        default:
            printf("Unknown instruction: %d\n", instr->instruction_type);
        }

        if (alu->pc >= alu->program_size) {
            alu_halt(alu);
        }
    }
    if (debug) {
        printf("MONAD halted at $%03d\n", alu->pc);
    }
}

bool set_input(ALU *alu, u64 n) {
    bool valid = true;
    for (int i = 0; i < 14; ++i) {
        u8 digit = n % 10;
        if (digit == 0) {
            valid = false;
        }
        alu->input[13 - i] = digit;
        n /= 10;
    }
    alu->input_index = 0;
    return valid;
}

void test_examples(Tester *tester) {
    test_section("Examples Part 1");
    ALU *alu = create_alu("../aoc2021/day24/test");
    set_input(alu, 91111111111111);
    run(alu, false);

    testi(tester, alu->z, 1, "");
    testi(tester, alu->y, 0, "");
    testi(tester, alu->x, 0, "");
    testi(tester, alu->w, 1, "");

    set_input(alu, 81111111111111);
    run(alu, false);

    testi(tester, alu->z, 0, "");
    testi(tester, alu->y, 0, "");
    testi(tester, alu->x, 0, "");
    testi(tester, alu->w, 1, "");

    alu = create_alu("../aoc2021/day24/input");
    set_input(alu, 13579246899999);
    run(alu, false);
    test_u64(tester, alu->z, 134689198, "");

    set_input(alu, 99995969919326);
    run(alu, false);
    test_u64(tester, alu->z, 0, "");

    test_section("Examples Part 2");
    testi(tester, 0, 0, "");
}

u64 recurse(ALU *alu, Dict *memo, int depth, bool find_max) {
    if (depth == 14) {
        if (alu->z == 0) {
            u64 result = 0;
            for (int i = 0; i < 14; ++i) {
                result *= 10;
                result += alu->input[i];
            }
            return result;
        } else {
            return 0;
        }
    }

    for (int i = 1; i < 10; ++i) {
        alu->input[depth] = find_max ? 10 - i : i;
        run(alu, false);

        Value key = UNSIGNED_VAL((alu->z << 8) | (depth & 0xF));
        if (!dict_contains(memo, &key)) {
            dict_set(memo, &key, NIL_VAL);
            u64 result = recurse(alu, memo, depth + 1, find_max);
            if (result > 0) {
                return result;
            }
        }
    }
    alu->input[depth] = 0;
    return 0;
}

u64 find_max_monad(ALU *alu) {
    Dict *memo = dict_create();
    u64 result = recurse(alu, memo, 0, true);
    dict_free(memo);
    return result;
}

u64 find_min_monad(ALU *alu) {
    Dict *memo = dict_create();
    u64 result = recurse(alu, memo, 0, false);
    dict_free(memo);
    return result;
}

int main() {
    Tester tester = create_tester("Arithmetic Logic Unit");
    test_examples(&tester);

    test_section("Solutions");

    ALU *alu = create_alu("../aoc2021/day24/input");

    u64 result = find_max_monad(alu);
    test_u64(&tester, result, 99995969919326, "solution to part 1");

    alu = create_alu("../aoc2021/day24/input");
    result = find_min_monad(alu);
    test_u64(&tester, result, 48111514719111, "solution to part 2");

    return test_summary(&tester);
}
