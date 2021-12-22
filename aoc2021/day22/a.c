#include "aoc.h"
#include "cuboids.c"
#include "utils.h"
#include <stdint.h>

#define CUBE_SIZE 128

typedef struct {
    u32 count;
    Cuboid bounds;
    Cuboid init_bounds;
    Cuboid cuboids[500];
} Cuboids;

bool is_in_initialization_area(Cuboid *cuboid) {
    return cuboid->x.from >= -50 && cuboid->x.to <= 50 &&
           cuboid->y.from >= -50 && cuboid->y.to <= 50 &&
           cuboid->z.from >= -50 && cuboid->z.to <= 50;
}

void check_bounds(Cuboid *bounds, Cuboid *cuboid) {
    if (cuboid->x.from < bounds->x.from) {
        bounds->x.from = cuboid->x.from;
    }

    if (cuboid->x.to > bounds->x.to) {
        bounds->x.to = cuboid->x.to;
    }

    if (cuboid->y.from < bounds->y.from) {
        bounds->y.from = cuboid->y.from;
    }

    if (cuboid->y.to > bounds->y.to) {
        bounds->y.to = cuboid->y.to;
    }

    if (cuboid->z.from < bounds->z.from) {
        bounds->z.from = cuboid->z.from;
    }

    if (cuboid->z.to > bounds->z.to) {
        bounds->z.to = cuboid->z.to;
    }
}

Cuboids *parse_reboot(char *file) {
    char *data = read_input(file);
    Queue *lines = read_lines(data);

    Cuboids *cuboids = malloc(sizeof(Cuboids));
    cuboids->init_bounds.x.from = INT32_MAX;
    cuboids->init_bounds.x.to = INT32_MIN;
    cuboids->init_bounds.y.from = INT32_MAX;
    cuboids->init_bounds.y.to = INT32_MIN;
    cuboids->init_bounds.z.from = INT32_MAX;
    cuboids->init_bounds.z.to = INT32_MIN;
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

        if (cuboid->in_init_area) {
            check_bounds(&cuboids->init_bounds, cuboid);
        }
        check_bounds(&cuboids->bounds, cuboid);

        size_cuboid(cuboid);

        node = node->next;
    }
    size_cuboid(&cuboids->bounds);
    size_cuboid(&cuboids->init_bounds);

    free(data);
    queue_free(lines);
    return cuboids;
}

// void find_overlapping_cuboids(Cuboids *cuboids) {
//     for (u32 i = 0; i < cuboids->count - 1; ++i) {
//         cuboids->overlap[i][i] = 0;
//         cuboids->overlap[i + 1][i + 1] = 0;
//         for (u32 j = i + 1; j < cuboids->count; ++j) {

//             Cuboid *a = &cuboids->cuboids[i];
//             Cuboid *b = &cuboids->cuboids[j];
//             if (has_overlap(a, b)) {
//                 cuboids->overlap[i][j] = 1;
//                 cuboids->overlap[j][i] = 1;
//             } else {
//                 cuboids->overlap[i][j] = 0;
//                 cuboids->overlap[j][i] = 0;
//             }
//         }
//     }

//     // for(u32 i = 0; i < cuboids->count; ++i) {
//     //     if (i == 0) {
//     //         printf("   ");
//     //         for(u32 j = 0; j < cuboids->count; ++j) {
//     //             printf("%2d ", j);
//     //         }
//     //         puts("");
//     //     }

//     //     printf("%2d ", i);
//     //     for(u32 j = 0; j < cuboids->count; ++j) {
//     //         printf("%2s ", cuboids->overlap[i][j] ? "#" : " ");
//     //     }
//     //     puts("");
//     // }
// }

// u32 count_activated_cuboids(Cuboid *init_bounds, u8 *space) {
//     u32 count = 0;
//     u32 dx = init_bounds->x.to - init_bounds->x.from + 1;
//     u32 dy = init_bounds->y.to - init_bounds->y.from + 1;
//     u32 dz = init_bounds->z.to - init_bounds->z.from + 1;

//     for (u32 i = 0; i < dx * dy * dz; ++i) {
//         count += space[i];
//     }

//     return count;
// }

// u32 reboot(Cuboids *cuboids) {
//     u32 dx = cuboids->init_bounds.x.to - cuboids->init_bounds.x.from + 1;
//     u32 dy = cuboids->init_bounds.y.to - cuboids->init_bounds.y.from + 1;
//     u32 dz = cuboids->init_bounds.z.to - cuboids->init_bounds.z.from + 1;
//     u8 *space = malloc(sizeof(u8) * dx * dy * dz);
//     memset(space, 0, sizeof(u8) * dx * dy * dz);

//     for (u32 i = 0; i < cuboids->count; ++i) {
//         Cuboid *c = &cuboids->cuboids[i];
//         if (!c->in_init_area) {
//             continue;
//         }
//         u32 from_z = c->z.from - cuboids->init_bounds.z.from;
//         u32 to_z = c->z.to - cuboids->init_bounds.z.from;
//         u32 from_y = c->y.from - cuboids->init_bounds.y.from;
//         u32 to_y = c->y.to - cuboids->init_bounds.y.from;
//         u32 from_x = c->x.from - cuboids->init_bounds.x.from;
//         u32 to_x = c->x.to - cuboids->init_bounds.x.from;
//         //printf("x=%d..%d y=%d..%d z=%d..%d\n", from_x, to_x, from_y, to_y, from_z, to_z);
//         for (u32 z = from_z; z <= to_z; ++z) {
//             for (u32 y = from_y; y <= to_y; ++y) {
//                 for (u32 x = from_x; x <= to_x; ++x) {
//                     space[z * dx * dy + y * dx + x] = c->on;
//                 }
//             }
//         }
//     }

//     u32 count = count_activated_cuboids(&cuboids->init_bounds, space);

//     free(space);
//     return count;
// }
typedef struct {
    Cuboid *cuboids[500];
    u64 count;
    u64 leafs;
} CuboidsSubset;

u64 reboot_subcube(CuboidsSubset *cuboids, Cuboid *bounds) {
    u8 space[CUBE_SIZE + 1][CUBE_SIZE + 1][CUBE_SIZE + 1];
    memset(space, 0, sizeof(u8) * (CUBE_SIZE + 1) * (CUBE_SIZE + 1) * (CUBE_SIZE + 1));

    for (u32 i = 0; i < cuboids->count; ++i) {
        Cuboid *cuboid = cuboids->cuboids[i];
        Cuboid c = intersection(bounds, cuboids->cuboids[i]);

        u32 from_z = c.z.from - bounds->z.from;
        u32 to_z = c.z.to - bounds->z.from;
        u32 from_y = c.y.from - bounds->y.from;
        u32 to_y = c.y.to - bounds->y.from;
        u32 from_x = c.x.from - bounds->x.from;
        u32 to_x = c.x.to - bounds->x.from;

        for (u32 z = from_z; z <= to_z; ++z) {
            for (u32 y = from_y; y <= to_y; ++y) {
                for (u32 x = from_x; x <= to_x; ++x) {
                    space[z][y][x] = cuboid->on;
                }
            }
        }
    }
    u64 count = 0;
    for (u32 z = 0; z <= CUBE_SIZE; ++z) {
        for (u32 y = 0; y <= CUBE_SIZE; ++y) {
            for (u32 x = 0; x <= CUBE_SIZE; ++x) {
                count += space[z][y][x];
            }
        }
    }
    return count;
}

u64 count_sub_cube(CuboidsSubset *cuboids, Cuboid bounds, bool init) {
    //printf("size=%llu\n", bounds.size);
    CuboidsSubset subset = {0};

    int overlap_count = 0;
    bool full_overlap = true;
    Cuboid *last_overlap;

    for (u32 i = 0; i < cuboids->count; ++i) {
        Cuboid *cuboid = cuboids->cuboids[i];
        if (init && !cuboid->in_init_area) {
            continue;
        }
        if (has_overlap(cuboid, &bounds)) {
            subset.cuboids[overlap_count++] = cuboid;

            last_overlap = cuboid;
            Cuboid overlap = intersection(&bounds, last_overlap);
            if (overlap.size != bounds.size) {
                full_overlap = false;
            }
        }
    }
    subset.count = overlap_count;

    u64 activated = 0;

    if (overlap_count == 0) {
        cuboids->leafs++;
        activated = 0;
    } else if (bounds.size == 1) {
        cuboids->leafs++;
        activated = last_overlap->on;
    } else if (full_overlap || overlap_count == 1) {
        cuboids->leafs++;
        Cuboid overlap = intersection(&bounds, last_overlap);
        activated = overlap.size * last_overlap->on;
    } else if (overlap_count == 2) {
        //printf("overlap 2 at %llu\n", bounds.size);
        cuboids->leafs++;
        Cuboid a = intersection(&bounds, subset.cuboids[0]);
        Cuboid b = intersection(&bounds, subset.cuboids[1]);
        Cuboid overlap = intersection(&a, &b);

        if (subset.cuboids[0]->on && subset.cuboids[1]->on) {
            activated += a.size + b.size - overlap.size;
        } else if (subset.cuboids[1]->on) {
            activated += b.size;
        } else if (subset.cuboids[0]->on && !subset.cuboids[1]->on) {
            activated += a.size - overlap.size;
        } else {
            activated += 0;
        }
    } else if (bounds.size == CUBE_SIZE * CUBE_SIZE * CUBE_SIZE) {
        cuboids->leafs++;
        activated = reboot_subcube(&subset, &bounds);
    } else {
        //printf("overlap count = %d size=%llu \n", overlap_count, bounds.size);

        s32 x1 = bounds.x.from;
        s32 x2 = bounds.x.to;
        s32 hx = x1 + (x2 - x1) / 2;
        s32 y1 = bounds.y.from;
        s32 y2 = bounds.y.to;
        s32 hy = y1 + (y2 - y1) / 2;
        s32 z1 = bounds.z.from;
        s32 z2 = bounds.z.to;
        s32 hz = z1 + (z2 - z1) / 2;

        activated += count_sub_cube(&subset, create_cuboid(x1, y1, z1, hx, hy, hz), init);
        activated += count_sub_cube(&subset, create_cuboid(hx + 1, y1, z1, x2, hy, hz), init);
        activated += count_sub_cube(&subset, create_cuboid(x1, hy + 1, z1, hx, y2, hz), init);
        activated += count_sub_cube(&subset, create_cuboid(hx + 1, hy + 1, z1, x2, y2, hz), init);

        activated += count_sub_cube(&subset, create_cuboid(x1, y1, hz + 1, hx, hy, z2), init);
        activated += count_sub_cube(&subset, create_cuboid(hx + 1, y1, hz + 1, x2, hy, z2), init);
        activated += count_sub_cube(&subset, create_cuboid(x1, hy + 1, hz + 1, hx, y2, z2), init);
        activated += count_sub_cube(&subset, create_cuboid(hx + 1, hy + 1, hz + 1, x2, y2, z2), init);
    }
    cuboids->leafs += subset.leafs;
    return activated;
}

u64 count_cuboids(Cuboids *cuboids, bool init) {
    Cuboid bounds;
    u64 n = 0;
    s32 x1 = abs(cuboids->bounds.x.from);
    s32 x2 = abs(cuboids->bounds.x.to);
    u64 x = x1 > x2 ? next_pow2(x1) : next_pow2(x2);
    n = x;
    s32 y1 = abs(cuboids->bounds.y.from);
    s32 y2 = abs(cuboids->bounds.y.to);
    u64 y = y1 > y2 ? next_pow2(y1) : next_pow2(y2);
    if (y > n) {
        n = y;
    }
    s32 z1 = abs(cuboids->bounds.z.from);
    s32 z2 = abs(cuboids->bounds.z.to);
    u64 z = z1 > z2 ? next_pow2(z1) : next_pow2(z2);
    if (z > n) {
        n = z;
    }

    bounds.x.from = -n;
    bounds.x.to = n;
    bounds.y.from = -n;
    bounds.y.to = n;
    bounds.z.from = -n;
    bounds.z.to = n;
    size_cuboid(&bounds);
    print_cuboid(&bounds);
    //print_cuboid(&bounds);
    //printf("x=%d..%d y=%d..%d z=%d..%d\n", bounds.x.from, bounds.x.to, bounds.y.from, bounds.y.to, bounds.z.from, bounds.z.to);
    CuboidsSubset subset = {0};
    for (u64 i = 0; i < cuboids->count; ++i) {
        subset.cuboids[i] = &cuboids->cuboids[i];
    }
    subset.count = cuboids->count;
    subset.leafs = 0;
    u64 count = count_sub_cube(&subset, bounds, init);
    printf("leafs visisted = %llu\n", subset.leafs);
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
    //test_u64(tester, count_cuboids(cuboids, false), 2758514936282235, "");

    testi(tester, 0, 0, "");
}

int main() {
    Tester tester = create_tester("Reactor Reboot");
    test_cuboids(&tester);
    test_examples(&tester);

    test_section("Solutions");

    Cuboids *cuboids = parse_reboot("../aoc2021/day22/input");

    test_u64(&tester, count_cuboids(cuboids, true), 527915, "solution to part 1");
    // test_u64(&tester, 0, 0, "solution to part 2");

    return test_summary(&tester);
}
