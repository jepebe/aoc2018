#include "aoc.h"

u64 run_program(u8 input[14]) {
    u8 index = 0;
    s64 w = 0;
    s64 x = 0;
    s64 y = 0;
    s64 z = 0;
    if (input[index] == 0) {
        return z;
    }
    w = input[index++];
    x = x * 0;
    x = x + z;
    x = x % 26;
    z = z / 1;
    x = x + 10;
    x = x == w;
    x = x == 0;
    y = y * 0;
    y = y + 25;
    y = y * x;
    y = y + 1;
    z = z * y;
    y = y * 0;
    y = y + w;
    y = y + 10;
    y = y * x;
    z = z + y;
    if (input[index] == 0) {
        return z;
    }
    w = input[index++];
    x = x * 0;
    x = x + z;
    x = x % 26;
    z = z / 1;
    x = x + 13;
    x = x == w;
    x = x == 0;
    y = y * 0;
    y = y + 25;
    y = y * x;
    y = y + 1;
    z = z * y;
    y = y * 0;
    y = y + w;
    y = y + 5;
    y = y * x;
    z = z + y;
    if (input[index] == 0) {
        return z;
    }
    w = input[index++];
    x = x * 0;
    x = x + z;
    x = x % 26;
    z = z / 1;
    x = x + 15;
    x = x == w;
    x = x == 0;
    y = y * 0;
    y = y + 25;
    y = y * x;
    y = y + 1;
    z = z * y;
    y = y * 0;
    y = y + w;
    y = y + 12;
    y = y * x;
    z = z + y;
    if (input[index] == 0) {
        return z;
    }
    w = input[index++];
    x = x * 0;
    x = x + z;
    x = x % 26;
    z = z / 26;
    x = x + -12;
    x = x == w;
    x = x == 0;
    y = y * 0;
    y = y + 25;
    y = y * x;
    y = y + 1;
    z = z * y;
    y = y * 0;
    y = y + w;
    y = y + 12;
    y = y * x;
    z = z + y;
    if (input[index] == 0) {
        return z;
    }
    w = input[index++];
    x = x * 0;
    x = x + z;
    x = x % 26;
    z = z / 1;
    x = x + 14;
    x = x == w;
    x = x == 0;
    y = y * 0;
    y = y + 25;
    y = y * x;
    y = y + 1;
    z = z * y;
    y = y * 0;
    y = y + w;
    y = y + 6;
    y = y * x;
    z = z + y;
    if (input[index] == 0) {
        return z;
    }
    w = input[index++];
    x = x * 0;
    x = x + z;
    x = x % 26;
    z = z / 26;
    x = x + -2;
    x = x == w;
    x = x == 0;
    y = y * 0;
    y = y + 25;
    y = y * x;
    y = y + 1;
    z = z * y;
    y = y * 0;
    y = y + w;
    y = y + 4;
    y = y * x;
    z = z + y;
    if (input[index] == 0) {
        return z;
    }
    w = input[index++];
    x = x * 0;
    x = x + z;
    x = x % 26;
    z = z / 1;
    x = x + 13;
    x = x == w;
    x = x == 0;
    y = y * 0;
    y = y + 25;
    y = y * x;
    y = y + 1;
    z = z * y;
    y = y * 0;
    y = y + w;
    y = y + 15;
    y = y * x;
    z = z + y;
    if (input[index] == 0) {
        return z;
    }
    w = input[index++];
    x = x * 0;
    x = x + z;
    x = x % 26;
    z = z / 26;
    x = x + -12;
    x = x == w;
    x = x == 0;
    y = y * 0;
    y = y + 25;
    y = y * x;
    y = y + 1;
    z = z * y;
    y = y * 0;
    y = y + w;
    y = y + 3;
    y = y * x;
    z = z + y;
    if (input[index] == 0) {
        return z;
    }
    w = input[index++];
    x = x * 0;
    x = x + z;
    x = x % 26;
    z = z / 1;
    x = x + 15;
    x = x == w;
    x = x == 0;
    y = y * 0;
    y = y + 25;
    y = y * x;
    y = y + 1;
    z = z * y;
    y = y * 0;
    y = y + w;
    y = y + 7;
    y = y * x;
    z = z + y;
    if (input[index] == 0) {
        return z;
    }
    w = input[index++];
    x = x * 0;
    x = x + z;
    x = x % 26;
    z = z / 1;
    x = x + 11;
    x = x == w;
    x = x == 0;
    y = y * 0;
    y = y + 25;
    y = y * x;
    y = y + 1;
    z = z * y;
    y = y * 0;
    y = y + w;
    y = y + 11;
    y = y * x;
    z = z + y;
    if (input[index] == 0) {
        return z;
    }
    w = input[index++];
    x = x * 0;
    x = x + z;
    x = x % 26;
    z = z / 26;
    x = x + -3;
    x = x == w;
    x = x == 0;
    y = y * 0;
    y = y + 25;
    y = y * x;
    y = y + 1;
    z = z * y;
    y = y * 0;
    y = y + w;
    y = y + 2;
    y = y * x;
    z = z + y;
    if (input[index] == 0) {
        return z;
    }
    w = input[index++];
    x = x * 0;
    x = x + z;
    x = x % 26;
    z = z / 26;
    x = x + -13;
    x = x == w;
    x = x == 0;
    y = y * 0;
    y = y + 25;
    y = y * x;
    y = y + 1;
    z = z * y;
    y = y * 0;
    y = y + w;
    y = y + 12;
    y = y * x;
    z = z + y;
    if (input[index] == 0) {
        return z;
    }
    w = input[index++];
    x = x * 0;
    x = x + z;
    x = x % 26;
    z = z / 26;
    x = x + -12;
    x = x == w;
    x = x == 0;
    y = y * 0;
    y = y + 25;
    y = y * x;
    y = y + 1;
    z = z * y;
    y = y * 0;
    y = y + w;
    y = y + 4;
    y = y * x;
    z = z + y;
    if (input[index] == 0) {
        return z;
    }
    w = input[index++];
    x = x * 0;
    x = x + z;
    x = x % 26;
    z = z / 26;
    x = x + -13;
    x = x == w;
    x = x == 0;
    y = y * 0;
    y = y + 25;
    y = y * x;
    y = y + 1;
    z = z * y;
    y = y * 0;
    y = y + w;
    y = y + 11;
    y = y * x;
    z = z + y;
    return z;
}
