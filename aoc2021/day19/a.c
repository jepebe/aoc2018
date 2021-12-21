#include "aoc.h"
#include "dict.h"
#include "utils.h"

typedef struct {
    s32 x;
    s32 y;
    s32 z;
} Beacon;

typedef struct {
    u8 id;
    s32 x;
    s32 y;
    s32 z;
    u8 rot_x;
    u8 rot_y;
    u8 rot_z;
    u8 bcn_count;
    Beacon beacons[32];
    u32 dist[32][32];
    Dict *dist_pairs;
} Scanner;

typedef struct {
    u8 count;
    Scanner scanners[32];
    bool overlap[32][32];
} Scanners;

typedef struct {
    Beacon *b1;
    Beacon *b2;
    u32 dist;
} BeaconPair;

void print_scanner(Scanner *scn) {
    printf("scanner #%d at (%d, %d, %d)\n", scn->id, scn->x, scn->y, scn->z);
    for (int i = 0; i < scn->bcn_count; ++i) {
        Beacon *bcn = &scn->beacons[i];
        printf("--> (%d, %d, %d)\n", bcn->x, bcn->y, bcn->z);
    }

    for (int row = 0; row < scn->bcn_count; ++row) {
        if (row == 0) {
            printf("   ");
            for (int j = 0; j < scn->bcn_count; ++j) {
                printf("%7u ", j);
            }
            puts("");
        }

        printf("%3u ", row);
        for (int j = 0; j < row; ++j) {
            printf("%7u ", scn->dist[row][j]);
        }
        puts("");
    }
}

u32 distance(s32 x1, s32 y1, s32 z1, s32 x2, s32 y2, s32 z2) {
    s32 dx = x2 - x1;
    s32 dy = y2 - y1;
    s32 dz = z2 - z1;
    return dx * dx + dy * dy + dz * dz;
}

bool overlaps(Scanner *a, Scanner *b) {
    int overlap_count = 0;

    Queue *keys = dict_keys(a->dist_pairs);
    QueueNode *key = keys->head;
    while (key) {
        if (dict_contains(b->dist_pairs, &key->value)) {
            overlap_count++;
        }
        key = key->next;
    }

    return overlap_count > 10;
}

void find_overlapping_scanners(Scanners *scanners) {
    for (int j = 0; j < scanners->count - 1; ++j) {
        for (int i = j + 1; i < scanners->count; ++i) {
            scanners->overlap[j][i] = false;
            scanners->overlap[i][j] = false;
            Scanner *a = &scanners->scanners[j];
            Scanner *b = &scanners->scanners[i];
            if (overlaps(a, b)) {
                scanners->overlap[j][i] = true;
                scanners->overlap[i][j] = true;
                //printf("Scanner #%d overlaps with #%d\n", j, i);
            }
        }
    }

    // for (int j = 0; j < scanners->count; ++j) {
    //     if (j == 0) {
    //         printf("   ");
    //         for (int i = 0; i < scanners->count; ++i) {
    //             printf("%3d ", i);
    //         }
    //         puts("");
    //     }
    //     printf("%2d ", j);
    //     for (int i = 0; i < scanners->count; ++i) {
    //         printf("%3d ", scanners->overlap[j][i]);
    //     }
    //     puts("");
    // }
}

Scanners parse_scanners(char *file) {
    char *data = read_input(file);
    Queue *lines = read_lines(data);

    Scanners scanners = {0};
    Scanner *current_scanner;
    QueueNode *node = lines->head;
    while (node) {
        char *line = node->value.as.string;
        if (line[1] == '-') {
            u8 id = scanners.count++;
            current_scanner = &scanners.scanners[id];
            current_scanner->id = id;
            current_scanner->dist_pairs = dict_create();
            current_scanner->rot_x = 0;
            current_scanner->rot_y = 0;
            current_scanner->rot_z = 0;
        } else {
            Beacon *beacon = &current_scanner->beacons[current_scanner->bcn_count++];
            char *end;
            beacon->x = x_strtol(line, 10, &end, __LINE__);
            beacon->y = x_strtol(end + 1, 10, &end, __LINE__);
            beacon->z = x_strtol(end + 1, 10, &end, __LINE__);

            int beacon_index = current_scanner->bcn_count - 1;
            for (int i = 0; i < beacon_index; ++i) {
                Beacon *b1 = &current_scanner->beacons[i];
                Beacon *b2 = beacon;
                u32 dist = distance(b1->x, b1->y, b1->z, b2->x, b2->y, b2->z);

                current_scanner->dist[beacon_index][i] = dist;
                current_scanner->dist[i][beacon_index] = dist;

                Value key = UNSIGNED_VAL(dist);
                BeaconPair *beacon_pair = malloc(sizeof(BeaconPair));
                beacon_pair->dist = dist;
                beacon_pair->b1 = b1;
                beacon_pair->b2 = b2;
                Value pair = POINTER_VAL(beacon_pair);
                dict_set(current_scanner->dist_pairs, &key, pair);
            }
        }
        node = node->next;
    }

    find_overlapping_scanners(&scanners);

    // for (int i = 0; i < scanners.count; ++i) {
    //     print_scanner(&scanners.scanners[i]);
    // }

    queue_free(lines);
    free(data);
    return scanners;
}

void rotate_x(Beacon *beacon) {
    s32 x = beacon->x;
    s32 y = beacon->y;
    s32 z = beacon->z;
    beacon->x = x * 1 + y * 0 + z * 0;
    beacon->y = x * 0 + y * 0 + z * -1;
    beacon->z = x * 0 + y * 1 + z * 0;
}

void rotate_y(Beacon *beacon) {
    s32 x = beacon->x;
    s32 y = beacon->y;
    s32 z = beacon->z;
    beacon->x = x * 0 + y * 0 + z * 1;
    beacon->y = x * 0 + y * 1 + z * 0;
    beacon->z = x * -1 + y * 0 + z * 0;
}

void rotate_z(Beacon *beacon) {
    s32 x = beacon->x;
    s32 y = beacon->y;
    s32 z = beacon->z;
    beacon->x = x * 0 + y * -1 + z * 0;
    beacon->y = x * 1 + y * 0 + z * 0;
    beacon->z = x * 0 + y * 0 + z * 1;
}

bool unique_distances(Scanners *scanners) {
    bool unique = true;
    for (int i = 0; i < scanners->count; ++i) {
        Dict *dict = dict_create();
        Scanner *scanner = &scanners->scanners[i];

        for (int row = 0; row < scanner->bcn_count; ++row) {
            for (int col = 0; col < row; ++col) {
                Value distance = UNSIGNED_VAL(scanner->dist[row][col]);
                if (!dict_contains(dict, &distance)) {
                    dict_set(dict, &distance, UNSIGNED_VAL(0));
                }
                Value val;
                dict_get(dict, &distance, &val);
                val.as.unsigned_64++;
                dict_set(dict, &distance, val);
            }
        }
        Queue *keys = dict_keys(dict);
        QueueNode *node = keys->head;
        while (node) {
            Value val;
            dict_get(dict, &node->value, &val);
            if (val.as.unsigned_64 > 1) {
                printf("Scanner #%d has non unique distance %llu\n", i, node->value.as.unsigned_64);
                unique = false;
            }
            node = node->next;
        }
        queue_free(keys);
        dict_free(dict);
    }

    return unique;
}

Beacon transform(Beacon *beacon, u8 rot_x, u8 rot_y, u8 rot_z) {
    Beacon copy = *beacon;

    for (int i = 0; i < rot_x; ++i) {
        rotate_x(&copy);
    }

    for (int i = 0; i < rot_y; ++i) {
        rotate_y(&copy);
    }

    for (int i = 0; i < rot_z; ++i) {
        rotate_z(&copy);
    }
    return copy;
}

typedef struct {
    s32 dx;
    s32 dy;
    s32 dz;
    s32 dist;
} Vec3;

Vec3 beacon_vector(Beacon *b1, Beacon *b2) {
    Vec3 vec;
    vec.dx = b2->x - b1->x;
    vec.dy = b2->y - b1->y;
    vec.dz = b2->z - b1->z;
    vec.dist = distance(b1->x, b1->y, b1->z, b2->x, b2->y, b2->z);
    return vec;
}

bool find_transformation(Scanner *a, Scanner *b) {
    for (int rot_x = 0; rot_x < 4; ++rot_x) {
        for (int rot_y = 0; rot_y < 4; ++rot_y) {
            for (int rot_z = 0; rot_z < 4; ++rot_z) {
                Queue *keys = dict_keys(a->dist_pairs);
                QueueNode *key = keys->head;
                bool match = true;
                bool initialized = false;
                Vec3 v1;
                Vec3 v2;
                Vec3 v3;
                Vec3 v4;
                while (key && match) {
                    Value val;
                    dict_get(a->dist_pairs, &key->value, &val);
                    BeaconPair *bp1 = (BeaconPair *)val.as.ptr;
                    Beacon sb1 = transform(bp1->b1, a->rot_x, a->rot_y, a->rot_z);
                    Beacon sb2 = transform(bp1->b2, a->rot_x, a->rot_y, a->rot_z);

                    if (dict_contains(b->dist_pairs, &key->value)) {
                        dict_get(b->dist_pairs, &key->value, &val);
                        BeaconPair *bp2 = (BeaconPair *)val.as.ptr;
                        Beacon b1 = transform(bp2->b1, rot_x, rot_y, rot_z);
                        Beacon b2 = transform(bp2->b2, rot_x, rot_y, rot_z);

                        if (!initialized) {
                            v1 = beacon_vector(&sb1, &b1);
                            v2 = beacon_vector(&sb1, &b2);
                            v3 = beacon_vector(&sb2, &b1);
                            v4 = beacon_vector(&sb2, &b2);
                            initialized = true;
                        } else {
                            Vec3 v = beacon_vector(&sb1, &b1);

                            if (v.dist != v1.dist && v.dist != v2.dist) {
                                v = beacon_vector(&sb1, &b2);
                                if (v.dist != v1.dist && v.dist != v2.dist) {
                                    match = false;
                                }
                            }
                        }
                    }
                    key = key->next;
                }

                if (match) {
                    if (v1.dist == v3.dist || v1.dist == v4.dist) {
                        b->x = a->x - v1.dx;
                        b->y = a->y - v1.dy;
                        b->z = a->z - v1.dz;
                        b->rot_x = rot_x;
                        b->rot_y = rot_y;
                        b->rot_z = rot_z;

                    } else if (v2.dist == v3.dist || v2.dist == v4.dist) {
                        b->x = a->x - v2.dx;
                        b->y = a->y - v2.dy;
                        b->z = a->z - v2.dz;
                        b->rot_x = rot_x;
                        b->rot_y = rot_y;
                        b->rot_z = rot_z;

                    } else {
                        printf("What? Not a match\n");
                    }
                    //printf("x=%d y=%d z=%d\n", b->x, b->y, b->z);
                    return true;
                }
            }
        }
    }
    return false;
}

void resolve_scanners(Scanners *scanners) {
    Queue *queue = queue_create();
    Dict *completed = dict_create();

    queue_append(queue, UNSIGNED_VAL(0));
    dict_set(completed, &UNSIGNED_VAL(0), NIL_VAL);

    while (!queue_empty(queue)) {
        Value index = queue_pop_front(queue);
        if (!dict_contains(completed, &index)) {
            queue_append(queue, index);
            continue;
        }
        int idx = index.as.unsigned_64;
        for (int i = 0; i < scanners->count; ++i) {
            if (idx == i || dict_contains(completed, &UNSIGNED_VAL(i))) {
                continue;
            }
            if (scanners->overlap[idx][i]) {
                Scanner *a = &scanners->scanners[idx];
                Scanner *b = &scanners->scanners[i];
                bool found = find_transformation(a, b);
                //printf("%d -> %d = %s\n", idx, i, found ? "true" : "false");

                if (found) {
                    dict_set(completed, &UNSIGNED_VAL(i), NIL_VAL);
                    queue_append(queue, UNSIGNED_VAL(i));
                }
            }
        }
    }
    //printf("completed=%d/%d\n", completed->count, scanners->count);
    queue_free(queue);
    dict_free(completed);
}

u64 count_unique_beacons(Scanners *scanners) {
    Dict *unique = dict_create();

    for (int i = 0; i < scanners->count; ++i) {
        Scanner *scanner = &scanners->scanners[i];
        //printf("--- Scanner %d ---\n", i);
        for (int j = 0; j < scanner->bcn_count; ++j) {
            Beacon *b = &scanner->beacons[j];
            Beacon c = transform(b, scanner->rot_x, scanner->rot_y, scanner->rot_z);
            Point3D p = {.x = c.x + scanner->x,
                         .y = c.y + scanner->y,
                         .z = c.z + scanner->z};

            if (dict_contains(unique, &AS_POINT3D_VAL(p))) {
                //printf("%5d, %5d, %5d\n", p.x, p.y, p.z);
            } else {
                //printf("%5d, %5d, %5d\n", p.x, p.y, p.z);
                dict_set(unique, &AS_POINT3D_VAL(p), NIL_VAL);
            }
        }
    }
    u64 count = unique->count;
    dict_free(unique);
    return count;
}

u64 max_distance(Scanners *scanners) {
    u64 dist = 0;
    for(int j = 0; j < scanners->count - 1; ++j) {
        for(int i = j + 1; i < scanners->count; ++i) {
            u64 dx = abs(scanners->scanners[i].x - scanners->scanners[j].x);
            u64 dy = abs(scanners->scanners[i].y - scanners->scanners[j].y);
            u64 dz = abs(scanners->scanners[i].z - scanners->scanners[j].z);
            if((dx + dy + dz) > dist) {
                dist = dx + dy + dz;
            }
            
        }
    }
    return dist;
}

void test_examples(Tester *tester) {
    test_section("Examples Part 1");

    Scanners scanners = parse_scanners("../aoc2021/day19/test2");
    bool unique = unique_distances(&scanners);
    test(tester, unique, "Unique distances");

    Beacon bt = {.x = 1, .y = 1, .z = 1};
    rotate_z(&bt);
    testi(tester, bt.x, -1, "x");
    testi(tester, bt.y, 1, "y");
    testi(tester, bt.z, 1, "z");
    rotate_z(&bt);
    testi(tester, bt.x, -1, "x");
    testi(tester, bt.y, -1, "y");
    testi(tester, bt.z, 1, "z");
    rotate_z(&bt);
    testi(tester, bt.x, 1, "x");
    testi(tester, bt.y, -1, "y");
    testi(tester, bt.z, 1, "z");

    bt = (Beacon){.x = 1, .y = 1, .z = 1};
    rotate_x(&bt);
    testi(tester, bt.x, 1, "x 90");
    testi(tester, bt.y, -1, "y");
    testi(tester, bt.z, 1, "z");
    rotate_x(&bt);
    testi(tester, bt.x, 1, "x 180");
    testi(tester, bt.y, -1, "y");
    testi(tester, bt.z, -1, "z");
    rotate_x(&bt);
    testi(tester, bt.x, 1, "x 270");
    testi(tester, bt.y, 1, "y");
    testi(tester, bt.z, -1, "z");

    bt = (Beacon){.x = 1, .y = 1, .z = 1};
    rotate_y(&bt);
    testi(tester, bt.x, 1, "x 90");
    testi(tester, bt.y, 1, "y");
    testi(tester, bt.z, -1, "z");
    rotate_y(&bt);
    testi(tester, bt.x, -1, "x 180");
    testi(tester, bt.y, 1, "y");
    testi(tester, bt.z, -1, "z");
    rotate_y(&bt);
    testi(tester, bt.x, -1, "x 270");
    testi(tester, bt.y, 1, "y");
    testi(tester, bt.z, 1, "z");

    Scanner *a = &scanners.scanners[0];
    Scanner *b = &scanners.scanners[1];
    find_transformation(a, b);

    testi(tester, b->x, 68, "");
    testi(tester, b->y, -1246, "");
    testi(tester, b->z, -43, "");

    puts("");

    a = &scanners.scanners[1];
    b = &scanners.scanners[4];
    find_transformation(a, b);

    testi(tester, b->x, -20, "");
    testi(tester, b->y, -1133, "");
    testi(tester, b->z, 1061, "");

    a = &scanners.scanners[4];
    b = &scanners.scanners[2];
    find_transformation(a, b);

    testi(tester, b->x, 1105, "");
    testi(tester, b->y, -1205, "");
    testi(tester, b->z, 1229, "");

    a = &scanners.scanners[4];
    b = &scanners.scanners[3];
    find_transformation(a, b);

    testi(tester, b->x, -92, "");
    testi(tester, b->y, -2380, "");
    testi(tester, b->z, -20, "");

    scanners = parse_scanners("../aoc2021/day19/test2");
    resolve_scanners(&scanners);
    testi(tester, count_unique_beacons(&scanners), 79, "");

    test_section("Examples Part 2");

    testi(tester, max_distance(&scanners), 3621, "");
}

int main() {
    Tester tester = create_tester("Beacon Scanner");
    test_examples(&tester);

    test_section("Solutions");

    Scanners scanners = parse_scanners("../aoc2021/day19/input");
    resolve_scanners(&scanners);
    int count = count_unique_beacons(&scanners);
    test(&tester, count != 491, "wrong solution to part 1"); // too high
    test(&tester, count != 350, "wrong solution to part 1"); // too high
    testi(&tester, count, 338, "solution to part 1");

    testi(&tester, max_distance(&scanners), 9862, "solution to part 2");

    return test_summary(&tester);
}
