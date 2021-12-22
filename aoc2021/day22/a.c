#include "aoc.h"
#include "cuboids.c"
#include "utils.h"
#include <stdint.h>

#define CUBE_SIZE 128

typedef struct {
    s32 count;
    Cuboid bounds;
    Cuboid cuboids[500];
} Cuboids;

bool is_in_initialization_area(Cuboid *cuboid) {
    return cuboid->x.from >= -50 && cuboid->x.to <= 50 &&
           cuboid->y.from >= -50 && cuboid->y.to <= 50 &&
           cuboid->z.from >= -50 && cuboid->z.to <= 50;
}

void adjust_range(Range *a, Range *b) {
    // adjusts a to encompass b
    if (b->from < a->from) {
        a->from = b->from;
    }

    if (b->to > a->to) {
        a->to = b->to;
    }
}

void adjust_bounds(Cuboid *bounds, Cuboid *cuboid) {
    // adjust _bounds_ to encompass the ranges if _cuboid_
    adjust_range(&bounds->x, &cuboid->x);
    adjust_range(&bounds->y, &cuboid->y);
    adjust_range(&bounds->z, &cuboid->z);
}

Cuboids *parse_reboot(char *file) {
    char *data = read_input(file);
    Queue *lines = read_lines(data);

    Cuboids *cuboids = malloc(sizeof(Cuboids));
    cuboids->bounds.x.from = INT32_MAX;
    cuboids->bounds.x.to = INT32_MIN;
    cuboids->bounds.y.from = INT32_MAX;
    cuboids->bounds.y.to = INT32_MIN;
    cuboids->bounds.z.from = INT32_MAX;
    cuboids->bounds.z.to = INT32_MIN;

    QueueNode *node = lines->head;
    while (node) {
        char *line = node->value.as.string;
        char *end = line;
        Cuboid *cuboid = &cuboids->cuboids[cuboids->count++];
        cuboid->id = cuboids->count - 1;

        if (line[1] == 'n') {
            end = &line[5];
            cuboid->on = true;
        } else {
            end = &line[6];
            cuboid->on = false;
        }

        cuboid->x.from = x_strtol(end, 10, &end, __LINE__);
        cuboid->x.to = x_strtol(end + 2, 10, &end, __LINE__);
        cuboid->y.from = x_strtol(end + 3, 10, &end, __LINE__);
        cuboid->y.to = x_strtol(end + 2, 10, &end, __LINE__);
        cuboid->z.from = x_strtol(end + 3, 10, &end, __LINE__);
        cuboid->z.to = x_strtol(end + 2, 10, &end, __LINE__);
        cuboid->in_init_area = is_in_initialization_area(cuboid);

        adjust_bounds(&cuboids->bounds, cuboid);

        size_cuboid(cuboid);

        node = node->next;
    }

    size_cuboid(&cuboids->bounds);

    free(data);
    queue_free(lines);
    return cuboids;
}

void accumulate_size(Value *val, void *ctx) {
    // map function to accumulate the Cuboid sizes in a Queue
    Cuboid *cuboid = (Cuboid *)val->as.ptr;
    (*(u64 *)ctx) += cuboid->size;
}

u64 count_cuboids(Cuboids *cuboids, bool init) {
    Queue *on = queue_create();
    for (int i = 0; i < cuboids->count; ++i) {
        Cuboid *current = &cuboids->cuboids[i];
        if (init && !current->in_init_area) {
            continue;
        }
        if (!current->on) {
            // skip _off_ cuboids
            // previous iterations has already "adapted" to the shape of this one
            continue;
        }
        Queue *queue = queue_create();
        queue_append(queue, POINTER_VAL(current));
        for (int j = i + 1; j < cuboids->count; ++j) {
            Cuboid *next = &cuboids->cuboids[j];

            QueueNode *node = queue->head;
            while (node) {
                Cuboid *cuboid = (Cuboid *)node->value.as.ptr;
                if (has_overlap(cuboid, next)) {
                    CuboidSplit *split = split_cuboid(cuboid, next);
                    for (int k = 0; k < split->count; ++k) {
                        queue_append(queue, POINTER_VAL(&split->cuboids[k]));
                    }
                    QueueNode *temp = node;
                    node = node->next;
                    queue_remove_node(queue, temp);
                } else {
                    node = node->next;
                }
            }
        }
        queue_add_all(on, queue);
        queue_free(queue);
    }

    u64 count = 0;
    queue_map(on, accumulate_size, &count);
    
    queue_free(on);
    return count;
}

void test_examples(Tester *tester) {
    test_section("Examples Part 1");

    Cuboids *cuboids = parse_reboot("../aoc2021/day22/test1");
    testi(tester, count_cuboids(cuboids, true), 39, "");
    testi(tester, count_cuboids(cuboids, false), 39, "");

    cuboids = parse_reboot("../aoc2021/day22/test2");
    testi(tester, count_cuboids(cuboids, true), 590784, "");
    testi(tester, count_cuboids(cuboids, false), 2100164115, "?");

    test_section("Examples Part 2");

    cuboids = parse_reboot("../aoc2021/day22/test3");
    testi(tester, count_cuboids(cuboids, true), 474140, "");
    test_u64(tester, count_cuboids(cuboids, false), 2758514936282235, "");
}

int main() {
    Tester tester = create_tester("Reactor Reboot");
    test_cuboids(&tester);
    test_examples(&tester);

    test_section("Solutions");

    Cuboids *cuboids = parse_reboot("../aoc2021/day22/input");
    test_u64(&tester, count_cuboids(cuboids, true), 527915, "solution to part 1");
    test_u64(&tester, count_cuboids(cuboids, false), 1218645427221987, "solution to part 2");

    return test_summary(&tester);
}
