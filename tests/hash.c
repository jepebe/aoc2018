#include "aoc.h"
#include "dict.h"

void test_hashing(Tester *tester) {
    test_u64(tester, hash_string("hello", 5), 1335831723, "hello");
    test_u64(tester, hash_string("world", 5), 933488787, "world");

    Point p1 = {0, 0};
    Point p2 = {1, 0};
    Point p3 = {0, 1};
    Point p4 = {1, 1};
    test_u64(tester, hash_point(&p1), 292984781, "(0,0)");
    test_u64(tester, hash_point(&p2), 3950255460, "(1,0)");
    test_u64(tester, hash_point(&p3), 276207162, "(0,1)");
    test_u64(tester, hash_point(&p4), 3967033079, "(1,1)");
    test_u64(tester, hash_point(&((Point){1, 1})), 3967033079, "(1,1)");

    test_u64(tester, hash_u64(1), 67918732, "1");
    test_u64(tester, hash_u64(2), 118251589, "2");
    test_u64(tester, hash_u64(13), 135029208, "13");
}

void test_dict_with_unsigned(Tester *tester) {
    Dict *dict = dict_create();

    Value key_1 = UNSIGNED_VAL(13);
    Value set_val = UNSIGNED_VAL(1337);
    Value return_val = {0};

    test(tester, !dict_get(dict, &key_1, &return_val), "get empty");
    test(tester, dict_set(dict, &key_1, set_val), "set 13 = 1337");
    test(tester, dict_get(dict, &key_1, &return_val), "get 13");
    test_u64(tester, return_val.as.unsigned_64, 1337, "check content = 1337");

    testi(tester, dict->capacity, 7, "capacity");
    testi(tester, dict->count, 1, "count");

    for (int i = 0; i < 1000; ++i) {
        Value key = UNSIGNED_VAL(i);
        Value val = UNSIGNED_VAL(i ^ 2166136261u);
        //printf("index=%d hash=%u\n", i, hash_value(&key));
        if (i == 13) {
            test(tester, !dict_set(dict, &key, val), NULL);
        } else {
            test(tester, dict_set(dict, &key, val), NULL);
        }
    }

    testi(tester, dict->capacity, 2047, "capacity");
    testi(tester, dict->count, 1000, "count");

    for (int i = 0; i < 1000; ++i) {
        Value key = UNSIGNED_VAL(i);
        Value val;

        test(tester, dict_get(dict, &key, &val), NULL);
        test_u64(tester, val.as.unsigned_64, i ^ 2166136261u, NULL);
    }
    dict_free(dict);
}

void test_dict_with_point(Tester *tester) {
    Dict *dict = dict_create();

    int i = 0;
    for(int y = 0; y < 100; ++y) {
        for(int x = 0; x < 100; ++x) {
            Value key = POINT_VAL(x, y);
            Value val = UNSIGNED_VAL(i++);
            test(tester, dict_set(dict, &key, val), NULL);
        }
    }

    i = 0;
    for(int y = 0; y < 100; ++y) {
        for(int x = 0; x < 100; ++x) {
            Value key = POINT_VAL(x, y);
            Value val;
            test(tester, dict_get(dict, &key, &val), NULL);
            test_u64(tester, val.as.unsigned_64, i++, NULL);
        }
    }

    dict_free(dict);
}

int main() {
    Tester tester = create_tester("Hashing");

    test_hashing(&tester);
    test_dict_with_unsigned(&tester);
    test_dict_with_point(&tester);

    return test_summary(&tester);
}
