#include "aoc.h"
#include "utils.h"

typedef struct {
    int width;
    int height;
    int moved;
    char grid[150][150];
} Map;

void print_map(Map *map) {
    for (int y = 0; y < map->height; ++y) {
        for (int x = 0; x < map->width; ++x) {
            printf("%c", map->grid[y][x]);
        }
        puts("");
    }
}

Map read_map(char *file) {
    Map map = {0};
    int east_bound = 0;
    int south_bound = 0;

    char *data = read_input(file);
    Queue *lines = read_lines(data);
    QueueNode *node = lines->head;
    int row = 0;
    while (node) {
        char *line = node->value.as.string;
        if (map.width == 0) {
            map.width = strlen(line);
            map.height = queue_length(lines);
            // printf("width x height = %d x %d\n", map.width, map.height);
        }
        for (int i = 0; i < map.width; i++) {
            map.grid[row][i] = line[i];
            if(line[i] == '>') {
                east_bound++;
            } else if(line[i] == 'v') {
                south_bound++;
            }
        }
        row++;
        node = node->next;
    }
    map.moved = map.width * map.height;
    // printf("heading east = %d\n", east_bound);
    // printf("heading south = %d\n", south_bound);

    free(data);
    queue_free(lines);
    return map;
}

Map move_cucumbers(Map *map) {
    Map new_map = {0};
    new_map.width = map->width;
    new_map.height = map->height;
    for (int y = 0; y < map->height; ++y) {
        for (int x = 0; x < map->width; ++x) {
            new_map.grid[y][x] = '.';
        }
    }
    int east_bound = 0;
    int south_bound = 0;
    for (int y = 0; y < map->height; ++y) {
        for (int x = 0; x < map->width; ++x) {
            int next_x = (x + 1 == map->width) ? 0 : x + 1;
            if (map->grid[y][x] == '>') {
                east_bound++;
                if (map->grid[y][next_x] == '.') {
                    new_map.grid[y][next_x] = '>';
                    new_map.moved++;
                } else {
                    new_map.grid[y][x] = '>';
                }
            }
        }
    }

    for (int y = 0; y < map->height; ++y) {
        for (int x = 0; x < map->width; ++x) {
            int next_y = (y + 1 == map->height) ? 0 : y + 1;
            if (map->grid[y][x] == 'v') {
                south_bound++;
                if (map->grid[next_y][x] != 'v' && new_map.grid[next_y][x] == '.') {
                    new_map.grid[next_y][x] = 'v';
                    new_map.moved++;
                } else {
                    new_map.grid[y][x] = 'v';
                }
            }
        }
    }
    // printf("heading east = %d\n", east_bound);
    // printf("heading south = %d\n", south_bound);
    return new_map;
}

int iterate_cucumbers(Map *map) {
    int steps = 0;
    Map run_map = *map;
    while (run_map.moved > 0) {
        run_map = move_cucumbers(&run_map);
        // print_map(&run_map);
        // puts("");
        steps++;
    };
    return steps;
}

void test_examples(Tester *tester) {
    test_section("Examples Part 1");
    Map map = read_map("../aoc2021/day25/test1");
    // print_map(&map);

    testi(tester, map.width, 10, "");
    testi(tester, map.height, 9, "");
    testi(tester, iterate_cucumbers(&map), 58, "");

}

int main() {
    Tester tester = create_tester("Sea Cucumber");
    test_examples(&tester);

    test_section("Solutions");

    Map map = read_map("../aoc2021/day25/input");
    int steps = iterate_cucumbers(&map);

    testi(&tester, steps, 360, "solution to part 1");

    return test_summary(&tester);
}
