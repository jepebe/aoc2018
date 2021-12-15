#include "aoc.h"
#include "utils.h"
#include "dict.h"
#include <stdint.h>

typedef struct {
    u8 width;
    u8 height;
    u16 count;
    u8 map[101 * 101];
} Riskmap;

Riskmap parse_map(char *file) {
    Riskmap map = {.width = 0, .height = 0, .count = 0};
    char *data = read_input(file);
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
    free(data);
    queue_free(lines);
    // for(int i = 0; i < map.count; ++i) {
    //     printf("%d ", map.map[i]);
    // }
    return map;
}

int indexify(Riskmap *map, u8 x, u8 y) {
    return y * map->width + x;
}

u64 lowest_neighbour_risk(Riskmap *map, u64 *riskmap, u8 x, u8 y) {
    u64 lowest_risk = UINT64_MAX;
    u64 risk;
    
    if(x - 1 >= 0) {
        risk = riskmap[indexify(map, x - 1, y)];
        if (risk < lowest_risk) {
            lowest_risk = risk;
        }
    }

    if(x + 1 < map->width) {
        risk = riskmap[indexify(map, x + 1, y)];
        if (risk < lowest_risk) {
            lowest_risk = risk;
        }
    }

    if(y - 1 >= 0) {
        risk = riskmap[indexify(map, x, y - 1)];
        if (risk < lowest_risk) {
            lowest_risk = risk;
        }
    }

    if(y + 1 < map->height) {
        risk = riskmap[indexify(map, x, y + 1)];
        if (risk < lowest_risk) {
            lowest_risk = risk;
        }
    }

    return lowest_risk;
}

int find_lowest_path_risk(Riskmap *map) {
    Dict *visited = dict_create();
    
    Queue *q = queue_create();
    queue_append(q, POINT_VAL(0, 0));

    u64 risk[map->height][map->width];
    for(int y = 0; y < map->height; ++y) {
        for(int x = 0; x < map->width; ++x) {
            risk[y][x] = UINT64_MAX;
        }
    }
    //risk[0][0] = 0;

    while (!queue_empty(q)) {
        Value v = queue_pop_front(q);
        Point p = v.as.point;
        u8 local_risk = map->map[indexify(map, p.x, p.y)];
        
        if (dict_contains(visited, &v)) {
            u64 check_risk = lowest_neighbour_risk(map, &risk[0][0], p.x, p.y);
            if(check_risk + local_risk < risk[p.y][p.x]) {
                //printf("Shorter path exists!\n");
                risk[p.y][p.x] = check_risk + local_risk;
            }
        } else {
            u64 risk_to_here = lowest_neighbour_risk(map, &risk[0][0], p.x, p.y);
            risk[p.y][p.x] = local_risk + risk_to_here;

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
            dict_set(visited, &v, SIGNED_VAL(1));
        }
    }


    queue_free(q);
    dict_free(visited);

    for(int y = 0; y < map->height; ++y) {
        for(int x = 0; x < map->width; ++x) {
            printf("%3d ", (int) risk[y][x]);
        }
        puts("");
    }

    return risk[map->height - 1][map->width - 1];
}

void test_examples(Tester *tester) {
    test_section("Examples Part 1");
    Riskmap map = parse_map("../aoc2021/day15/test");

    u64 risk = find_lowest_path_risk(&map);

    testi(tester, risk, 40, "");

    test_section("Examples Part 2");

    testi(tester, 0, 0, "");
}

int main() {
    Tester tester = create_tester("");
    test_examples(&tester);

    test_section("Solutions");

    Riskmap map = parse_map("../aoc2021/day15/input");
    u64 risk = find_lowest_path_risk(&map);

    testi(&tester, risk, 0, "solution to part 1");
    testi(&tester, 0, 0, "solution to part 2");

    return test_summary(&tester);
}
