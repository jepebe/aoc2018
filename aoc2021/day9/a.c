#include "aoc.h"
#include "dict.h"
#include "utils.h"

typedef struct {
    u8 width;
    u8 height;
    u16 count;
    u8 map[101 * 101];
} Heightmap;

Heightmap parse_map(char *data) {
    Heightmap map = {.width = 0, .height = 0, .count = 0};
    Queue *lines = read_lines(data);
    QueueNode *line = lines->head;
    bool first_line = true;
    while (line) {
        map.height++;
        char *row = line->value.as.string;
        while (*row) {
            if (first_line) {
                map.width++;
            }
            map.map[map.count++] = *row - 48; // 0 in ascii = 48
            row++;
        }
        first_line = false;
        line = line->next;
    }
    queue_free(lines);
    // for(int i = 0; i < map.count; ++i) {
    //     printf("%d ", map.map[i]);
    // }
    return map;
}

int indexify(Heightmap *map, u8 x, u8 y) {
    return y * map->width + x;
}

bool is_low_point(Heightmap *map, u8 x, u8 y) {
    u8 p = map->map[indexify(map, x, y)];
    if (x - 1 >= 0 && map->map[indexify(map, x - 1, y)] <= p) {
        return false;
    }

    if (y - 1 >= 0 && map->map[indexify(map, x, y - 1)] <= p) {
        return false;
    }

    if (x + 1 < map->width && map->map[indexify(map, x + 1, y)] <= p) {
        return false;
    }

    if (y + 1 < map->height && map->map[indexify(map, x, y + 1)] <= p) {
        return false;
    }

    return true;
}

int calculate_risk_level(Heightmap *map) {
    int risk_level = 0;
    for (u8 y = 0; y < map->height; ++y) {
        for (u8 x = 0; x < map->width; ++x) {
            if (is_low_point(map, x, y)) {
                risk_level += 1 + map->map[indexify(map, x, y)];
            }
        }
    }
    return risk_level;
}

int grow_basin(Heightmap *map, u8 x, u8 y) {
    int size = 0;

    Dict *visited = dict_create();
    Queue *q = queue_create();
    queue_append(q, POINT_VAL(x, y));

    while (!queue_empty(q)) {
        Value v = queue_pop_front(q);
        if (!dict_contains(visited, &v)) {
            Point p = v.as.point;
            u8 value = map->map[indexify(map, p.x, p.y)];
            if (value < 9) {
                size++;
                if (p.x - 1 >= 0) {
                    queue_append(q, POINT_VAL(p.x - 1, p.y));
                }
                if (p.y - 1 >= 0) {
                    queue_append(q, POINT_VAL(p.x, p.y - 1));
                }
                if (p.x + 1 < map->width) {
                    queue_append(q, POINT_VAL(p.x + 1, p.y));
                }
                if (p.y + 1 < map->height) {
                    queue_append(q, POINT_VAL(p.x, p.y + 1));
                }
            }
            dict_set(visited, &v, SIGNED_VAL(1));
        }
    }

    queue_free(q);
    dict_free(visited);

    return size;
}

int grow_basins(Heightmap *map) {
    Queue *q = queue_create();

    for (u8 y = 0; y < map->height; ++y) {
        for (u8 x = 0; x < map->width; ++x) {
            if (is_low_point(map, x, y)) {
                int size = grow_basin(map, x, y);
                queue_append(q, SIGNED_VAL(size));
            }
        }
    }

    int size = 1;
    for (int i = 0; i < 3; ++i) {
        QueueNode *max_node = q->head;
        QueueNode *node = q->head;

        while (node) {
            if (node->value.as.signed_64 > max_node->value.as.signed_64) {
                max_node = node;
            }
            node = node->next;
        }
        queue_remove_node(q, max_node);
        size *= max_node->value.as.signed_64;
    }
    return size;
}

void test_examples(Tester *tester) {
    test_section("Examples Part 1");

    char *data = read_input("../aoc2021/day9/test");

    Heightmap map = parse_map(data);

    testi(tester, map.width, 10, "width");
    testi(tester, map.height, 5, "height");
    testi(tester, calculate_risk_level(&map), 15, "risk level");

    test_section("Examples Part 2");

    testi(tester, grow_basins(&map), 1134, "basin sizes");
}

int main() {
    Tester tester = create_tester("Smoke Basin");
    test_examples(&tester);

    test_section("Solutions");

    char *data = read_input("../aoc2021/day9/input");
    Heightmap map = parse_map(data);

    testi(&tester, calculate_risk_level(&map), 535, "solution to part 1");
    testi(&tester, grow_basins(&map), 1122700, "solution to part 2");

    return test_summary(&tester);
}
