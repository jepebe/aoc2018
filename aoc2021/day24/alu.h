#pragma once
#include "aoc.h"
#include "queue.h"
#include "utils.h"

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

char reg_as_char(OperandType op) {
    switch (op) {
    case REG_W:
        return 'w';
    case REG_X:
        return 'x';
    case REG_Y:
        return 'y';
    case REG_Z:
        return 'z';
    default:
        return '?';
    }
}

ALU *create_alu(char *file) {
    ALU *alu = malloc(sizeof(ALU));
    alu->halted = false;
    alu->program_size = 0;
    for (int i = 0; i < 14; ++i) {
        alu->input[i] = 0;
    }

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
        alu->pc--; // so that next instruction is this one on restart wo reset
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
        printf("-->div $%p=%lld + %lld\n", (void *)reg, *reg, value);
        alu_halt(alu);
    } else {
        *reg /= value;
    }
}

void alu_mod(ALU *alu, s64 *reg, s64 value) {
    (void)alu;
    if (*reg < 0 || value <= 0) {
        printf("-->mod $%p=%lld + %lld\n", (void *)reg, *reg, value);
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

void print_instruction(ALU *alu, Instruction *instr) {
    printf("[$%02d] ", alu->pc - 1);

    switch (instr->instruction_type) {
    case ADD:
        printf("add ");
        break;
    case INP:
        printf("inp ");
        break;
    case DIV:
        printf("div ");
        break;
    case EQL:
        printf("eql ");
        break;
    case MUL:
        printf("mul ");
        break;
    case MOD:
        printf("mod ");
        break;
    default:
        printf("??? ");
    }

    printf("%c ", reg_as_char(instr->operand_1));

    if (instr->instruction_type != INP) {
        if (instr->operand_2 == VALUE) {
            printf("%-10lld   ", instr->literal);
        } else {
            printf("%c=%-10lld ", reg_as_char(instr->operand_2), get_value(alu, instr));
        }
    } else {
        printf("%13s", " ");
    }

    printf("w=%-10lld x=%-10lld y=%-10lld z=%-10lld\n", alu->w, alu->x, alu->y, alu->z);
}

void run(ALU *alu, bool reset) {
    alu->halted = false;

    if (reset) {
        alu->pc = 0;
        alu->w = 0;
        alu->x = 0;
        alu->y = 0;
        alu->z = 0;
        alu->input_index = 0;
    }

#if DEBUG
    printf("program size = %d\n", alu->program_size);
    printf("input = ");
    for (int i = 0; i < 14; ++i) {
        printf("%d ", alu->input[i]);
    }
    puts("");
#endif

    while (!alu->halted) {
        Instruction *instr = &alu->program[alu->pc++];

#if DEBUG
        print_instruction(alu, instr);
#endif

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
            printf("Unknown instruction on line $%d\n", alu->pc - 1);
        }

        if (alu->pc >= alu->program_size) {
            alu_halt(alu);
        }
    }

#if DEBUG
    printf("MONAD halted at $%03d\n", alu->pc);
#endif
}
