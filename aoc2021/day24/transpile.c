#include "alu.h"

void print_operator(Instruction *instruction, char *op) {
    char var = reg_as_char(instruction->operand_1);
    if (instruction->operand_2 == VALUE) {
        printf("\t%c = %c %s %lld;\n", var, var, op, instruction->literal);
    } else {
        char var2 = reg_as_char(instruction->operand_2);
        printf("\t%c = %c %s %c;\n", var, var, op, var2);
    }
}

void transpile(char *file) {
    char *data = read_input(file);
    Queue *lines = read_lines(data);
    QueueNode *node = lines->head;
    printf("u64 run_program(u8 input[14]) {\n");
    printf("\tu8 index = 0;\n");
    printf("\ts64 w = 0;\n");
    printf("\ts64 x = 0;\n");
    printf("\ts64 y = 0;\n");
    printf("\ts64 z = 0;\n");

    while (node) {
        Instruction instruction = {0};
        char *instr = node->value.as.string;

        instruction.instruction_type = parse_instruction_type(instr);
        instruction.operand_1 = parse_operand_type(&instr[4]);
        if (instr[5] == ' ') {
            instruction.operand_2 = parse_operand_type(&instr[6]);

            if (instruction.operand_2 == VALUE) {
                instruction.literal = atoi(&instr[6]);
            }
        }

        if (instruction.instruction_type == INP) {
            char var = reg_as_char(instruction.operand_1);
            puts("");
            printf("\tif(input[index] == 0) {\n");
            printf("\t\treturn z;\n");
            printf("\t}\n");
            puts("");
            printf("\t%c = input[index++];\n", var);

        }
        if (instruction.instruction_type == ADD) {
            print_operator(&instruction, "+");
        }
        if (instruction.instruction_type == DIV) {
            print_operator(&instruction, "/");
        }
        if (instruction.instruction_type == MUL) {
            print_operator(&instruction, "*");
        }
        if (instruction.instruction_type == MOD) {
            print_operator(&instruction, "%");
        }
        if (instruction.instruction_type == EQL) {
            print_operator(&instruction, "==");
        }

        node = node->next;
    }

    printf("\treturn z;\n");
    printf("}\n");

    free(data);
    queue_free(lines);
}

int main() {
    transpile("../aoc2021/day24/input");
}
