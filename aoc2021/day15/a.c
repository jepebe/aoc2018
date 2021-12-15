#include "aoc.h"
#include "dict.h"
#include "heap.h"
#include "utils.h"
#include <stdint.h>

typedef struct {
    u16 width;
    u16 height;
    u8 map[501 * 501];
} Riskmap;

Riskmap parse_map(char *file) {
    Riskmap map = {.width = 0, .height = 0};
    char *data = read_input(file);
    Queue *lines = read_lines(data);
    QueueNode *line = lines->head;
    bool first_line = true;
    int count = 0;
    while (line) {
        map.height++;
        char *row = line->value.as.string;
        while (*row) {
            if (first_line) {
                map.width++;
            }
            map.map[count++] = *row - 48; // 0 in ascii = 48
            row++;
        }
        first_line = false;
        line = line->next;
    }
    free(data);
    queue_free(lines);
    return map;
}

int index_for(Riskmap *map, int x, int y) {
    return y * map->width + x;
}

Riskmap extend_map(Riskmap *map) {
    Riskmap new_map;
    new_map.width = map->width * 5;
    new_map.height = map->height * 5;

    int initial_risk = 0;
    for (int row = 0; row < 5; ++row) {
        for (int column = 0; column < 5; ++column) {
            for (int y = 0; y < map->height; ++y) {
                for (int x = 0; x < map->width; ++x) {
                    int idx = index_for(map, x, y);
                    u8 risk = map->map[idx] + initial_risk + column;
                    if (risk > 9) {
                        risk -= 9;
                    }
                    int tile_y = row * new_map.width * map->height;
                    int tile_x = column * map->width;
                    idx = tile_y + tile_x + y * new_map.width + x;
                    new_map.map[idx] = risk;
                }
            }
        }
        initial_risk += 1;
    }

    // for (int y = 0; y < new_map.height; ++y) {
    //     if (y % 10 == 0) {
    //         printf("\n");
    //     }
    //     for (int x = 0; x < new_map.width; ++x) {
    //         if (x % 10 == 0) {
    //             printf(" ");
    //         }

    //         int risk = new_map.map[y * new_map.width + x];
    //         printf("%d", risk);
    //     }
    //     puts("");
    // }

    return new_map;
}


typedef struct {
    Heap *queue;
    Dict *dist;
    Dict *visited;
} Dijkstra;

void add_neighbour(Riskmap *map, Dijkstra *dijkstra, u64 distance, Point p) {
    Value np = POINT_VAL(p.x, p.y);
    u8 risk = map->map[index_for(map, p.x, p.y)];
    if (!dict_contains(dijkstra->visited, &np)) {
        u64 new_distance = distance + risk;
        Value old_distance;
        dict_get(dijkstra->dist, &np, &old_distance);
        if (old_distance.as.unsigned_64 > new_distance) {
            dict_set(dijkstra->dist, &np, UNSIGNED_VAL(new_distance));
            heap_insert(dijkstra->queue, &np, new_distance);
        }
    }
}

int find_lowest_risk_path(Riskmap *map) {
    Dijkstra dijkstra;
    dijkstra.queue = heap_create(1000);
    dijkstra.dist = dict_create();
    dijkstra.visited = dict_create();

    for (int y = 0; y < map->height; ++y) {
        for (int x = 0; x < map->width; ++x) {
            Value p = POINT_VAL(x, y);
            dict_set(dijkstra.dist, &p, UNSIGNED_VAL(UINT64_MAX));
        }
    }
    heap_insert(dijkstra.queue, &POINT_VAL(0, 0), 0);

    dict_set(dijkstra.dist, &POINT_VAL(0, 0), UNSIGNED_VAL(0));

    while (!heap_empty(dijkstra.queue)) {
        Value key = heap_extract(dijkstra.queue);
        dict_set(dijkstra.visited, &key, BOOL_VAL(true));

        Point p = key.as.point;
        Value value;
        dict_get(dijkstra.dist, &key, &value);
        u64 distance = value.as.unsigned_64;

        if (p.x - 1 >= 0) {
            add_neighbour(map, &dijkstra, distance, (Point){p.x - 1, p.y});
        }

        if (p.x + 1 < map->width) {
            add_neighbour(map, &dijkstra, distance, (Point){p.x + 1, p.y});
        }

        if (p.y - 1 >= 0) {
            add_neighbour(map, &dijkstra, distance, (Point){p.x, p.y - 1});
        }

        if (p.y + 1 < map->height) {
            add_neighbour(map, &dijkstra, distance, (Point){p.x, p.y + 1});
        }
    }

    Value distance;
    dict_get(dijkstra.dist, &POINT_VAL(map->width - 1, map->height - 1), &distance);

    heap_free(dijkstra.queue);
    dict_free(dijkstra.dist);
    dict_free(dijkstra.visited);

    return distance.as.unsigned_64;
}

void test_examples(Tester *tester) {
    test_section("Examples Part 1");
    Riskmap map = parse_map("../aoc2021/day15/test");

    u64 risk = find_lowest_risk_path(&map);

    testi(tester, risk, 40, "");

    test_section("Examples Part 2");

    Riskmap xmap = extend_map(&map);
    risk = find_lowest_risk_path(&xmap);

    testi(tester, risk, 315, "");
}

int main() {
    Tester tester = create_tester("Chiton");
    test_examples(&tester);

    test_section("Solutions");

    Riskmap map = parse_map("../aoc2021/day15/input");
    u64 risk = find_lowest_risk_path(&map);
    testi(&tester, risk, 458, "solution to part 1");

    Riskmap xmap = extend_map(&map);
    risk = find_lowest_risk_path(&xmap);
    testi(&tester, risk, 2800, "solution to part 2");

    return test_summary(&tester);
}
