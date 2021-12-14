#include "aoc.h"
#include "ocr.h"
#include "utils.h"
#include <stdlib.h>
#include <string.h>

typedef struct {
    u8 *grid;
    Queue *folds;
    int max_x;
    int max_y;
    int fold_x;
    int fold_y;
} Origami;

Point parse_point(char *line) {
    int x = atoi(strtok(line, ","));
    int y = atoi(strtok(NULL, ","));
    return (Point){x, y};
}

Value parse_fold(char *line) {
    char *axis = strtok(line + 11, "=");
    int value = atoi(strtok(NULL, "="));

    if (axis[0] == 'x') {
        return POINT_VAL(value, 0);
    } else {
        return POINT_VAL(0, value);
    }
}

Origami parse_data(char *file) {
    char *data = read_input(file);
    Queue *q = read_lines(data);

    Origami origami;
    origami.max_x = 0;
    origami.max_y = 0;

    origami.folds = queue_create();

    Point points[queue_length(q)];
    //Point *points = (Point *)malloc(sizeof(Point) * queue_length(q));
    int n = 0;

    QueueNode *node = q->head;
    while (node) {
        char *line = node->value.as.string;
        if (line[0] == 'f') {
            Value f = parse_fold(line);
            queue_append(origami.folds, f);
        } else {
            Point p = parse_point(line);
            if (p.x > origami.max_x) {
                origami.max_x = p.x;
            }
            if (p.y > origami.max_y) {
                origami.max_y = p.y;
            }
            points[n++] = p;
        }
        node = node->next;
    }

    origami.max_x++;
    origami.max_y++;

    origami.fold_x = origami.max_x;
    origami.fold_y = origami.max_y;

    origami.grid = malloc(sizeof(u8) * origami.max_x * origami.max_y);
    memset(origami.grid, 0, origami.max_x * origami.max_y);

    for (int i = 0; i < n; ++i) {
        int index = points[i].y * origami.max_x + points[i].x;
        origami.grid[index] = 1;
    }

    // free(points);
    free(data);
    free(q);
    return origami;
}

void fold(Origami *origami, int n) {
    for (int i = 0; i < n; ++i) {
        Point fold = queue_pop_front(origami->folds).as.point;

        for (int y = 0; y < origami->max_y; ++y) {
            for (int x = 0; x < origami->max_x; ++x) {
                int index = y * origami->max_x + x;
                if (origami->grid[index] > 0) {
                    int dst_x = x;
                    if (fold.x > 0) {
                        if (x <= fold.x) {
                            continue;
                        }
                        dst_x = fold.x - (x - fold.x);
                        origami->fold_x = fold.x;
                    }

                    int dst_y = y;
                    if (fold.y > 0) {
                        if (y <= fold.y) {
                            continue;
                        }
                        dst_y = fold.y - (y - fold.y);
                        origami->fold_y = fold.y;
                    }

                    int dst_index = dst_y * origami->max_x + dst_x;
                    origami->grid[dst_index] += origami->grid[index];
                    origami->grid[index] = 0;
                }
            }
        }
    }
}

int count(Origami *origami) {
    int count = 0;
    for (int y = 0; y < origami->max_y; ++y) {
        for (int x = 0; x < origami->max_x; ++x) {
            int index = y * origami->max_x + x;
            if (origami->grid[index] > 0) {
                count++;
            }
        }
    }
    return count;
}

void print_origami(Origami *origami) {
    for (int y = 0; y < origami->fold_y; ++y) {
        for (int x = 0; x < origami->fold_x; ++x) {
            int index = y * origami->max_x + x;
            if (origami->grid[index] > 0) {
                printf("#");
            } else {
                printf(" ");
            }
        }
        puts("");
    }
}

bool is_pixel_set(int x, int y, void *ctx) {
    Origami *origami = (Origami *)ctx;
    if (y >= origami->max_y || x >= origami->max_x) {
        return false;
    }
    int index = y * origami->max_x + x;
    return origami->grid[index] > 0;
}

char *run_ocr(Origami *origami) {
    Queue *letters = queue_create();
    for (int i = 0; i < origami->fold_x; ++i) {
        char result = ocr(i, 0, is_pixel_set, origami);
        if (result) {
            queue_append(letters, CHAR_VAL(result));
        }
    }

    char *word = queue_as_string(letters);
    queue_free(letters);
    return word;
}

void test_examples(Tester *tester) {
    test_section("Examples Part 1");

    Origami origami = parse_data("../aoc2021/day13/test");
    fold(&origami, 1);
    testi(tester, count(&origami), 17, "fold 1");

    test_section("Examples Part 2");

    fold(&origami, 1);
    testi(tester, count(&origami), 16, "fold 2");
}

int main() {
    Tester tester = create_tester("Transparent Origami");
    test_examples(&tester);

    test_section("Solutions");

    Origami origami = parse_data("../aoc2021/day13/input");
    fold(&origami, 1);

    testi(&tester, count(&origami), 842, "solution to part 1");
    fold(&origami, 11);
    char *code = run_ocr(&origami);
    test_str(&tester, code, "BFKRCJZU", "solution to part 2");

    return test_summary(&tester);
}
