#include "aoc.h"
#include "md5.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    bool hashed;
    uint8_t digest[16];
    char hash[33];
} MD5;

char HEX[] = "0123456789abcdef";

void md5_str_w_len(char *msg, size_t len, MD5 *result) {
    result->hashed = true;
    md5((uint8_t *)msg, len, result->digest);

    for (int i = 0; i < 16; ++i) {
        result->hash[i * 2] = HEX[(result->digest[i] >> 4) & 0xF];
        result->hash[i * 2 + 1] = HEX[result->digest[i] & 0xF];
    }
    result->hash[32] = '\0';
}

void md5_str(char *msg, MD5 *result) {
    md5_str_w_len(msg, strlen(msg), result);
}

void test_md5(Tester *tester) {
    MD5 res;
    md5_str("Hello, World!", &res);
    test_str(tester, res.hash, "65a8e27d8879283831b664bd8b7f0ad4", "md5");

    md5_str("The quick brown fox jumps over the lazy dog", &res);
    test_str(tester, res.hash, "9e107d9d372bb6826bd81d3542a419d6", "md5");
}

void salt(char *prefix, int index, MD5 *result, int stretch) {
    // printf("Salting #%d\n", index);
    char buffer[33];
    sprintf(&buffer[0], "%s%d", prefix, index);

    md5_str((char *)&buffer, result);

    if (stretch) {
        for (int i = 0; i < stretch; ++i) {
            md5_str_w_len(result->hash, 32, result);
        }
    }
}

void test_salting(Tester *tester) {
    MD5 res;
    salt("abc", 18, &res, false);
    test(tester, strstr(res.hash, "888") != NULL, "abc18");

    salt("abc", 39, &res, false);
    test(tester, strstr(res.hash, "eee") != NULL, "abc39");

    salt("abc", 816, &res, false);
    test(tester, strstr(res.hash, "eeeee") != NULL, "abc816");

    salt("abc", 0, &res, 1);
    test_str(tester, res.hash, "eec80a0c92dc8a0777c619d9bb51e910", "stretched 1");

    salt("abc", 0, &res, 2);
    test_str(tester, res.hash, "16062ce768787384c81fe17a7a60c7e3", "stretched 2");

    salt("abc", 0, &res, 2016);
    test_str(tester, res.hash, "a107ff634856bb300138cac6568c0f24", "stretched 2016");
}

char has_triple(char *hash) {
    char current = *hash;
    int count = 0;

    while (*hash != '\0') {
        if (current != *hash) {
            current = *hash;
            count = 1;
        } else {
            count++;

            if (count == 3) {
                return current;
            }
        }
        hash++;
    }
    return '-';
}

bool has_quintuple(char *hash, char of) {
    int count = 0;

    while (*hash != '\0') {
        if (*hash != of) {
            count = 0;
        } else {
            count++;

            if (count == 5) {
                return true;
            }
        }
        hash++;
    }
    return false;
}

void test_triple_and_quintuple(Tester *tester) {
    test(tester, has_triple("abbbc"), "triple");
    test(tester, has_triple("abbc"), "!triple");
    test(tester, has_quintuple("abbbbbc", 'b'), "quintuple b");
    test(tester, !has_quintuple("abbbbbc", 'c'), "!quintuple c");
}

int find_key(char *prefix, int starting_from, MD5 *hashes, int stretch) {
    int index = starting_from;

    for (;;) {
        MD5 *res = &hashes[index];
        if (!res->hashed) {
            salt(prefix, index, res, stretch);
        }
        // printf("%d %s\n", index, res.hash);
        char triple = has_triple(res->hash);
        if (triple != '-') {
            //printf("Found %c triple at %d\n", triple, index);
            int quint = 0;
            while (quint < 1000) {
                MD5 *qres = &hashes[index + quint + 1];
                if (!qres->hashed) {
                    salt(prefix, index + quint + 1, qres, stretch);
                }

                if (has_quintuple(qres->hash, triple)) {
                    //printf("Found %c quintuple at %d -> %s -- %s\n", triple, index + quint + 1, qres->hash, res->hash);
                    return index;
                }
                quint++;
            }
        }
        index++;
    }
    return -1;
}

MD5 *create_md5_table(int n) {
    MD5 *table = (MD5 *)malloc(sizeof(MD5) * n);
    for (int i = 0; i < n; ++i) {
        table[i].hashed = false;
    }
    return table;
}

int find_key_number(char *prefix, int n, int stretch) {
    int found = 0;
    int key = 0;

    MD5 *hashes = create_md5_table(30000);

    while (found < n) {
        key = find_key(prefix, key, hashes, stretch);
        found++;

        if (found == n) {
            break;
        }
        key++;
    }
    free(hashes);
    return key;
}

void test_find_key_number(Tester *tester) {
    MD5 *hashes = create_md5_table(1100);
    int key = find_key("abc", 0, &hashes[0], 0);
    testi(tester, key, 39, "test 1");
    free(hashes);

    key = find_key_number("abc", 64, 0);
    testi(tester, key, 22728, "test 64");

    key = find_key_number("abc", 64, 2016);
    testi(tester, key, 22551, "test 64 stretch");
}

int main() {
    Tester tester = create_tester("One-Time Pad");
    test_md5(&tester);
    test_salting(&tester);
    test_triple_and_quintuple(&tester);
    test_find_key_number(&tester);

    int key = find_key_number("cuanljph", 64, 0);
    testi(&tester, key, 23769, "solution to part 1");

    key = find_key_number("cuanljph", 64, 2016);
    testi(&tester, key, 20606, "solution to part 2");

    return test_summary(&tester);
}
