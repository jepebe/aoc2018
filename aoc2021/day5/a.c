#include "aoc.h"
#include "utils.h"
#include <stdlib.h>
#include <string.h>

typedef struct {
    u16 x1;
    u16 y1;
    u16 x2;
    u16 y2;
    bool single_axis;
} Line;

typedef struct {
    Line vents[501];
    u16 vent_count;
} Vents;

typedef struct {
    u16 width;
    u16 height;
    u16 *grid;
} Map;

void parse_line(char *data, Line *line) {
    char *current_pos = data;
    char *next_pos = NULL;
    line->x1 = x_strtol(current_pos, 10, &next_pos, __LINE__);
    current_pos = next_pos + 1;
    line->y1 = x_strtol(current_pos, 10, &next_pos, __LINE__);
    current_pos = next_pos + 4;
    line->x2 = x_strtol(current_pos, 10, &next_pos, __LINE__);
    current_pos = next_pos + 1;
    line->y2 = x_strtol(current_pos, 10, &next_pos, __LINE__);

    line->single_axis = (line->x1 == line->x2) || (line->y1 == line->y2);
}

Vents parse_vents(char *data) {
    Vents vents = {0};
    char *token = strtok(data, "\n");
    while (token) {
        Line *line = &vents.vents[vents.vent_count++];
        parse_line(token, line);
        token = strtok(NULL, "\n");
    }
    return vents;
}

Map map_vents(Vents *vents, bool diagonal) {
    s16 max_x = 0;
    s16 max_y = 0;

    for (int i = 0; i < vents->vent_count; ++i) {
        Line *line = &vents->vents[i];
        if (line->x1 > max_x) {
            max_x = line->x1;
        }

        if (line->x2 > max_x) {
            max_x = line->x2;
        }

        if (line->y1 > max_y) {
            max_y = line->y1;
        }

        if (line->y2 > max_y) {
            max_y = line->y2;
        }
    }
    // increase grid size so coordinates are inside grid
    Map map = {.grid = NULL, .width = max_x + 1, .height = max_y + 1};

    map.grid = (u16 *)malloc(sizeof(u16) * map.width * map.height);
    memset(map.grid, 0, map.width * map.height);

    for (int i = 0; i < vents->vent_count; ++i) {
        Line *line = &vents->vents[i];
        if (line->single_axis || diagonal) {

            int dx = line->x2 - line->x1;
            int dy = line->y2 - line->y1;
            int steps = abs(dx) > abs(dy) ? abs(dx) : abs(dy);

            int x = line->x1;
            int y = line->y1;
            for (int i = 0; i <= steps; ++i) {
                u64 index = y * map.width + x;
                map.grid[index]++;

                if (dx != 0)
                    x += dx < 0 ? -1 : 1;
                if (dy != 0)
                    y += dy < 0 ? -1 : 1;
            }
        }
    }

    return map;
}

int count_vent_overlaps(Map *map) {
    s16 overlaps = 0;
    for (int y = 0; y < map->height; ++y) {
        for (int x = 0; x < map->width; ++x) {
            u16 count = map->grid[y * map->width + x];
            if (count > 1) {
                overlaps++;
            }
        }
    }
    return overlaps;
}

void test_examples(Tester *tester) {
    test_section("Examples Part 1");

    char *data = read_input("../aoc2021/day5/test");
    Vents vents = parse_vents(data);
    testi(tester, vents.vent_count, 10, "vents");
    test(tester, vents.vents[0].single_axis, "single axis");
    test(tester, !vents.vents[1].single_axis, "! single axis");

    Map map = map_vents(&vents, false);
    testi(tester, map.width, 10, "map width");
    testi(tester, map.height, 10, "map height");
    testi(tester, count_vent_overlaps(&map), 5, "overlaps");

    test_section("Examples Part 2");

    map = map_vents(&vents, true);
    // for (int y = 0; y < map.height; ++y) {
    //     for (int x = 0; x < map.width; ++x) {
    //         printf("%d", map.grid[y * map.width + x]);
    //     }
    //     puts("");
    // }
    testi(tester, count_vent_overlaps(&map), 12, "overlaps w/diagonals");
}

int main() {
    Tester tester = create_tester("Hydrothermal Venture");
    test_examples(&tester);

    test_section("Solutions");

    char *data = read_input("../aoc2021/day5/input");
    Vents vents = parse_vents(data);
    Map map = map_vents(&vents, false);
    int overlaps = count_vent_overlaps(&map);

    testi(&tester, overlaps, 6856, "solution to part 1");

    map = map_vents(&vents, true);
    overlaps = count_vent_overlaps(&map);
    testi(&tester, overlaps, 20666, "solution to part 2");

    return test_summary(&tester);
}
