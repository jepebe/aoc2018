#include <errno.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

typedef struct {
    char *name;
    struct timespec time;
    uint8_t count;
    uint8_t success;
    uint8_t fail;

} Tester;

Tester create_tester(char *name) {
    Tester tester;
    tester.name = name;
    timespec_get(&tester.time, TIME_UTC);
    tester.count = 0;
    tester.success = 0;
    tester.fail = 0;
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
        printf("\x1b[0;32m\u2705  Test #%d OK! %s\x1b[0m\n", tester->count, message);
    } else {
        tester->fail++;
        printf("\x1b[0;31m\u274C  Test #%d Error! %s\x1b[0m\n", tester->count, message);
    }
}

void testi(Tester *tester, int a, int b, char *msg) {
    tester->count++;
    int count = tester->count;

    if (a == b) {
        tester->success++;
        printf("\x1b[0;32m\u2705  Test #%d %d == %d %s\x1b[0m\n", count, a, b, msg);
    } else {
        tester->fail++;
        printf("\x1b[0;31m\u274C  Test #%d  %d != %d %s\x1b[0m\n", count, a, b, msg);
    }
}

void test_summary(Tester *tester) {
    if (tester->fail > 0) {
        uint8_t fail_count = tester->fail;
        uint8_t count = tester->count;
        printf("\x1b[0;31mError! %d of %d test(s) failed!\x1b[0m\n", fail_count, count);
    } else {
        uint8_t success = tester->success;
        printf("\x1b[0;32mSuccess! %d test(s) ran successfully!\x1b[0m\n", success);
    }
    double diff = timespec_diff(&tester->time);
    printf("\x1b[33mRunning time: %0.5f s.\x1b[0m\n", diff);
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
