#include "aoc.h"
#include "dict.h"
#include "utils.h"
#include <stdlib.h>
#include <string.h>

typedef struct {
    char *name;
    bool large;
    bool start_node;
    bool end_node;

} Cave;

typedef struct {
    Cave *caves;
    bool *connections;
    int count;
    int start;
    int end;
} CaveMap;

Cave create_cave(char *name) {
    Cave cave;
    cave.name = name;
    if (strcmp(name, "start") == 0) {
        cave.start_node = true;
    } else {
        cave.start_node = false;
    }

    if (strcmp(name, "end") == 0) {
        cave.end_node = true;
    } else {
        cave.end_node = false;
    }

    if (*name >= 'a' && *name <= 'z') {
        cave.large = false;
    } else {
        cave.large = true;
    }
    return cave;
}

CaveMap parse_data(char *file) {
    char *data = read_input(file);
    Queue *lines = read_lines(data);
    Dict *dict = dict_create();

    Queue *connections = queue_create();
    QueueNode *node = lines->head;
    int node_num = 0;
    while (node) {
        char *from = strtok(node->value.as.string, "-");
        char *to = strtok(NULL, "-");

        Value from_val = STRING_VAL(strdup(from));
        if (!dict_contains(dict, &from_val)) {
            dict_set(dict, &from_val, SIGNED_VAL(node_num++));
        }

        Value to_val = STRING_VAL(strdup(to));
        if (!dict_contains(dict, &to_val)) {
            dict_set(dict, &to_val, SIGNED_VAL(node_num++));
        }

        Value a;
        Value b;
        dict_get(dict, &from_val, &a);
        dict_get(dict, &to_val, &b);
        queue_append(connections, POINT_VAL(a.as.signed_64, b.as.signed_64));
        //Value *p = &connections->tail->value;
        //printf("connection %d <-> %d\n", p->as.point.x, p->as.point.y);

        node = node->next;
    }

    CaveMap map;
    map.count = dict->count;
    map.caves = (Cave *)malloc(sizeof(Cave) * dict->count);
    map.connections = (bool *)malloc(sizeof(bool) * map.count * map.count);
    memset(map.connections, false, map.count * map.count);
    map.start = -1;
    map.end = -1;

    Queue *keys = dict_keys(dict);
    QueueNode *key_node = keys->head;
    while (key_node) {
        Value val;
        dict_get(dict, &key_node->value, &val);

        map.caves[val.as.signed_64] = create_cave(key_node->value.as.string);

        if (map.caves[val.as.signed_64].start_node) {
            map.start = val.as.signed_64;
        } else if (map.caves[val.as.signed_64].end_node) {
            map.end = val.as.signed_64;
        }

        key_node = key_node->next;
    }

    QueueNode *con_node = connections->head;
    while (con_node) {
        Point p = con_node->value.as.point;
        map.connections[map.count * p.y + p.x] = true;
        map.connections[map.count * p.x + p.y] = true;
        con_node = con_node->next;
    }

    // for(int y = 0; y < map.count; ++y) {
    //     if (y == 0) {
    //         printf("  ");
    //         for(int x = 0; x < map.count; ++x) {
    //             printf("%d ", x);
    //         }
    //         puts("");
    //     }
    //     printf("%d ", y);

    //     for(int x = 0; x < map.count; ++x) {
    //         printf("%d ", map.connections[y * map.count + x]);
    //     }
    //     puts("");
    // }

    dict_free(dict);
    queue_free(lines);
    queue_free(connections);
    free(data);
    return map;
}

typedef struct {
    u8 *visited;
    int reached_end_count;
    int visited_twice;
    bool single_twice;
} Notes;

void trace_route(const CaveMap *map, int node, Notes *notes) {
    if (node == map->end) {
        notes->reached_end_count++;
        return;
    } else if (node == map->start && notes->visited[node] > 0) {
        return;
    }

    if (!map->caves[node].large && notes->visited[node] > 0) {
        if (!notes->single_twice) {
            // already visited small cave
            return;
        } else {
            if (notes->visited_twice == -1) {
                notes->visited_twice = node;
            } else {
                return;
            }
        }
    }

    notes->visited[node]++;

    // printf("%s ", map->caves[node].name);

    int row = node * map->count;
    for (int i = 0; i < map->count; ++i) {
        if (i != node && map->connections[row + i]) {
            trace_route(map, i, notes);
        }
    }

    if (notes->visited_twice == node) {
        notes->visited_twice = -1;
    }
    notes->visited[node]--;
}

int count_routes(const CaveMap *map, bool single_twice) {
    Notes notes;
    notes.reached_end_count = 0;
    notes.single_twice = single_twice;
    notes.visited_twice = -1;
    notes.visited = (u8 *)malloc(sizeof(u8) * map->count);
    memset(notes.visited, 0, map->count);

    trace_route(map, map->start, &notes);

    free(notes.visited);
    return notes.reached_end_count;
}

void test_examples(Tester *tester) {
    test_section("Examples Part 1");

    CaveMap map = parse_data("../aoc2021/day12/test1");
    int routes = count_routes(&map, false);
    testi(tester, routes, 10, "test1");

    map = parse_data("../aoc2021/day12/test2");
    routes = count_routes(&map, false);
    testi(tester, routes, 19, "test2");

    map = parse_data("../aoc2021/day12/test3");
    routes = count_routes(&map, false);
    testi(tester, routes, 226, "test3");

    test_section("Examples Part 2");

    map = parse_data("../aoc2021/day12/test1");
    routes = count_routes(&map, true);
    testi(tester, routes, 36, "test1");

    map = parse_data("../aoc2021/day12/test2");
    routes = count_routes(&map, true);
    testi(tester, routes, 103, "test2");

    map = parse_data("../aoc2021/day12/test3");
    routes = count_routes(&map, true);
    testi(tester, routes, 3509, "test3");
}

int main() {
    Tester tester = create_tester("Passage Pathing");
    test_examples(&tester);

    test_section("Solutions");

    CaveMap map = parse_data("../aoc2021/day12/input");
    int routes = count_routes(&map, false);

    testi(&tester, routes, 3000, "solution to part 1");

    routes = count_routes(&map, true);
    testi(&tester, routes, 74222, "solution to part 2");

    return test_summary(&tester);
}
