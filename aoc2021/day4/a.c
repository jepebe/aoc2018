#include "aoc.h"
#include "utils.h"

typedef struct {
    s8 grid[25];
} Board;

typedef struct {
    u8 num_count;
    u8 board_count;
    s8 numbers[150];
    Board board[150];
    s8 win_order[150];
    s8 win_number[150];
} Bingo;

void parse_numbers(Bingo *bingo, char *line) {
    char *token = strtok(line, ",");
    bingo->num_count = 0;
    while (token) {
        bingo->numbers[bingo->num_count++] = atoi(token);
        token = strtok(NULL, ",");
    }
}

QueueNode *parse_board(Bingo *b, QueueNode *node) {
    Board *board = &(b->board[b->board_count++]);

    int index = 0;
    for (int i = 0; i < 5; ++i) {
        char *line = node->value.as.string;

        char *token = strtok(line, " ");
        while (token) {
            board->grid[index++] = (u8)atoi(token);
            token = strtok(NULL, " ");
        }
        node = node->next;
    }

    return node;
}

Bingo *parse_data(char *file) {
    char *data = read_input(file);
    Queue *lines = read_lines(data);

    Bingo *b = (Bingo *)malloc(sizeof(Bingo));
    for (int i = 0; i < 150; ++i) {
        b->win_number[i] = -1;
        b->win_order[i] = -1;
    }

    QueueNode *node = lines->head;
    parse_numbers(b, node->value.as.string);

    b->board_count = 0;
    node = node->next;
    while (node) {
        node = parse_board(b, node);
    }
    return b;
}

void mark_boards(Bingo *bingo, u8 n) {
    for (int i = 0; i < bingo->board_count; ++i) {
        Board *board = &bingo->board[i];
        if (bingo->win_order[i] >= 0) {
            continue;
        }
        for (int j = 0; j < 25; ++j) {
            if (board->grid[j] == n) {
                board->grid[j] = -board->grid[j];
            }
        }
    }
}

s8 check_for_bingo(Bingo *bingo, u8 n, u8 round) {
    s8 winner = -1;
    for (int i = 0; i < bingo->board_count; ++i) {
        Board *board = &bingo->board[i];
        if (bingo->win_order[i] >= 0) {
            // already marked with bingo
            continue;
        }

        for (int j = 0; j < 5; ++j) {
            bool row = true;
            bool column = true;
            for (int k = 0; k < 5; ++k) {
                u8 row_index = j * 5 + k;
                if (board->grid[row_index] > 0) {
                    row = false;
                }

                u8 column_index = j + k * 5;
                if (board->grid[column_index] > 0) {
                    column = false;
                }
            }
            if (row || column) {
                if (winner < 0) {
                    winner = i;
                }
                bingo->win_number[i] = n;
                bingo->win_order[i] = round;
            }
        }
    }
    return winner;
}

int calculate_score(Board *board, int n) {
    int score = 0;
    for (int j = 0; j < 25; ++j) {
        if (board->grid[j] >= 0) {
            score += board->grid[j];
        }
    }
    return score * n;
}

int play_bingo(Bingo *bingo) {
    int score = -1;
    for (int i = 0; i < bingo->num_count; ++i) {
        u8 n = bingo->numbers[i];
        mark_boards(bingo, n);
        s8 winner_num = check_for_bingo(bingo, n, i);

        if (winner_num >= 0 && score == -1) {
            Board *winner = &bingo->board[winner_num];
            score = calculate_score(winner, n);
        }
    }
    return score;
}

int find_last_winner_score(Bingo *bingo) {
    int max_index = -1;
    int max_order = -1;
    for (int i = 0; i < bingo->board_count; ++i) {
        int win_order = bingo->win_order[i];
        if (win_order > max_order) {
            max_index = i;
            max_order = win_order;
        }
    }
    return calculate_score(&bingo->board[max_index], bingo->win_number[max_index]);
}

void test_examples(Tester *tester) {
    test_section("Examples Part 1");

    Bingo *bingo = parse_data("../aoc2021/day4/test");
    testi(tester, bingo->num_count, 27, "number count");
    testi(tester, bingo->board_count, 3, "board count");

    int score = play_bingo(bingo);

    testi(tester, score, 4512, "");

    test_section("Examples Part 2");

    score = find_last_winner_score(bingo);
    testi(tester, score, 1924, "");
    free(bingo);
}

int main() {
    Tester tester = create_tester("Giant Squid");
    test_examples(&tester);

    test_section("Solutions");

    Bingo *bingo = parse_data("../aoc2021/day4/input");

    int score = play_bingo(bingo);
    testi(&tester, score, 12796, "solution to part 1");

    score = find_last_winner_score(bingo);
    testi(&tester, score, 18063, "solution to part 2");

    return test_summary(&tester);
}
