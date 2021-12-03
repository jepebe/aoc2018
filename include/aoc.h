#pragma once

#include <errno.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define u8 uint8_t
#define u16 uint16_t
#define u32 uint32_t
#define u64 uint64_t

#define s8 int8_t
#define s16 int16_t
#define s32 int32_t
#define s64 int64_t

#define LEN(x) (sizeof(x) / sizeof((x)[0]))

typedef struct {
    char *name;
    struct timespec time;
    u16 count;
    u16 success;
    u16 fail;

} Tester;

Tester create_tester(char *name) {
    Tester tester;
    tester.name = name;
    timespec_get(&tester.time, TIME_UTC);
    tester.count = 0;
    tester.success = 0;
    tester.fail = 0;

    printf("\x1b[33m--== %s ==--\x1b[0m\n", name);
    return tester;
}

static inline double timespec_diff(struct timespec *a) {
    struct timespec result;
    struct timespec b;
    timespec_get(&b, TIME_UTC);
    result.tv_sec = b.tv_sec - a->tv_sec;
    result.tv_nsec = b.tv_nsec - a->tv_nsec;
    if (result.tv_nsec < 0) {
        --result.tv_sec;
        result.tv_nsec += 1000000000L;
    }
    double t = result.tv_sec * 1000000000.0;
    t += result.tv_nsec;
    t /= 1000000000.0;

    return t;
}

void test(Tester *tester, bool test_state, char *message) {
    tester->count++;

    if (test_state) {
        tester->success++;
        if (message) {
            printf("\x1b[0;32m\u2705  Test #%02d OK! %s\x1b[0m\n", tester->count, message);
        }
    } else {
        tester->fail++;

        printf("\x1b[0;31m\u274C  Test #%02d Error! %s\x1b[0m\n", tester->count, message);
    }
}

void testi(Tester *tester, int a, int b, char *msg) {
    tester->count++;
    int count = tester->count;

    if (a == b) {
        tester->success++;
        if (msg) {
            printf("\x1b[0;32m\u2705  Test #%02d %d == %d %s\x1b[0m\n", count, a, b, msg);
        }
    } else {
        tester->fail++;
        printf("\x1b[0;31m\u274C  Test #%02d  %d != %d %s\x1b[0m\n", count, a, b, msg);
    }
}

void test_u64(Tester *tester, uint64_t a, uint64_t b, char *msg) {
    tester->count++;
    int count = tester->count;

    if (a == b) {
        tester->success++;
        if (msg) {
            printf("\x1b[0;32m\u2705  Test #%02d %llu == %llu %s\x1b[0m\n", count, a, b, msg);
        }
    } else {
        tester->fail++;
        printf("\x1b[0;31m\u274C  Test #%02d %llu != %llu %s\x1b[0m\n", count, a, b, msg);
    }
}

void test_str(Tester *tester, char *a, char *b, char *msg) {
    tester->count++;
    int count = tester->count;

    if (strcmp(a, b) == 0) {
        tester->success++;
        if (msg) {
            printf("\x1b[0;32m\u2705  Test #%02d %s == %s %s\x1b[0m\n", count, a, b, msg);
        }
    } else {
        tester->fail++;
        printf("\x1b[0;31m\u274C  Test #%02d %s != %s %s\x1b[0m\n", count, a, b, msg);
    }
}

void test_section(char *name) {
    printf("\n\x1b[33m[%s]\x1b[0m\n", name);
}

int test_summary(Tester *tester) {
    printf("\n");
    if (tester->fail > 0) {
        u16 fail_count = tester->fail;
        u16 count = tester->count;
        printf("\x1b[0;31mError! %d of %d test(s) failed!\x1b[0m\n", fail_count, count);
    } else {
        u16 success = tester->success;
        printf("\x1b[0;32mSuccess! %d test(s) ran successfully!\x1b[0m\n", success);
    }
    double diff = timespec_diff(&tester->time);
    printf("\x1b[33mRunning time: %0.5f s.\x1b[0m\n", diff);

    return tester->fail;
}

u8 count_set_bits(u64 n) {
    int count = 0;
    while (n) {
        n = n & (n - 1);
        count++;
    }
    return count;
}

void print_bits(size_t bits, u64 value) {
    for (int i = bits - 1; i >= 0; i--) {
        unsigned char byte = (value >> i) & 1;
        printf("%d", byte);
    }
    puts("");
}

char *read_input(const char *path) {
    FILE *fd = fopen(path, "rb");

    if (!fd) {
        perror("fopen");
        exit(1);
    }
    // get filesize
    fseek(fd, 0, SEEK_END);
    size_t file_size = ftell(fd);
    rewind(fd);

    if (file_size > 0x10000) {
        printf("File limit exceeded!\n");
        exit(1);
    }
    char *dst = malloc(sizeof(char) * file_size);
    size_t read = fread(dst, sizeof(char), file_size, fd);

    if (read < file_size) {
        if (ferror(fd)) {
            perror("fopen");
            exit(1);
        }
    }
    fclose(fd);

    return dst;
}
