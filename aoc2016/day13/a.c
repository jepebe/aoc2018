#include "aoc.h"
#include "queue.h"
#include "dict.h"

#define INPUT 1358

bool is_wall(s8 x, s8 y, int fav) {
    if (x < 0 || y < 0) {
        return 1; // wall if negative
    }
    u64 n = x * x + 3 * x + 2 * x * y + y + y * y + fav;
    u8 c = count_set_bits(n);
    return c & 0x1; // odd
}

int bfs(int x, int y, int fav) {
    Queue *q = queue_create();
    Value target = POINT_VAL(x, y);
    Value start = POINT_VAL(1, 1);
    queue_append(q, start);

    Dict *map = dict_create();
    dict_set(map, &start, UNSIGNED_VAL(0));

    Value temp;
    int target_depth = -1;
    while(!queue_empty(q)) {
        Value current = queue_pop_front(q);

        dict_get(map, &current, &temp);
        u64 distance = temp.as.unsigned_64;
        
        if(is_value_equal(&current, &target)) {
            target_depth = distance;
            break;
        }
        
        int x = current.as.point.x;
        int y = current.as.point.y;

        Value p = POINT_VAL(x, y - 1);

        if(!is_wall(p.as.point.x, p.as.point.y, fav) && !dict_contains(map, &p)) {
            queue_append(q, p);
            dict_set(map, &p, UNSIGNED_VAL(distance + 1));
        }

        p = POINT_VAL(x, y + 1);

        if(!is_wall(p.as.point.x, p.as.point.y, fav) && !dict_contains(map, &p)) {
            queue_append(q, p);
            dict_set(map, &p, UNSIGNED_VAL(distance + 1));
        }

        p = POINT_VAL(x + 1, y);

        if(!is_wall(p.as.point.x, p.as.point.y, fav) && !dict_contains(map, &p)) {
            queue_append(q, p);
            dict_set(map, &p, UNSIGNED_VAL(distance + 1));
        }

        p = POINT_VAL(x - 1, y);

        if(!is_wall(p.as.point.x, p.as.point.y, fav) && !dict_contains(map, &p)) {
            queue_append(q, p);
            dict_set(map, &p, UNSIGNED_VAL(distance + 1));
        }
    }

    int count = 0;
    for(int i = 0; i <= map->capacity; ++i) {
        Entry *e = &map->entries[i];
        if (!IS_NIL(e->key) && e->value.as.unsigned_64 <= 50) {
            count++;
        }
    }

    printf("visited <= 50 = %d\n", count); // 141
    free(map);
    free(q);
    return target_depth;
}

int main() {
    Tester tester = create_tester("A Maze of Twisty Little Cubicles");

    test(&tester, is_wall(1, 0, 10), "tests");
    test(&tester, !is_wall(0, 0, 10), "");
    test(&tester, is_wall(5, 2, 10), "");
    test(&tester, is_wall(5, 4, 10), "");
    test(&tester, !is_wall(4, 4, 10), "");

    testi(&tester, bfs(7, 4, 10), 11, "test case");
    testi(&tester, bfs(31, 39, 1358), 96, "solution to part 1");

    return test_summary(&tester);
}
