#include "aoc.h"
#include <stdint.h>

uint64_t next_number(uint64_t previous) {
    return (previous * 252533) % 33554393;
}

int index(int row, int column) {
    int idx = 0;

    for (int i = 1; i <= column; ++i) {
        idx += i;
    }

    for (int i = 1; i < row; ++i) {
        idx += column;
        column++;
    }
    return idx;
}

int number_at(int idx) {
    int previous = 20151125;
    for (int i = 1; i < idx; ++i) {
        previous = next_number(previous);
    }
    return previous;
}

int main() {
    //row 2947, column 3029.
    Tester tester = create_tester("Let It Snow");

    testi(&tester, index(1, 1), 1, "");
    testi(&tester, index(3, 3), 13, "");
    testi(&tester, index(5, 1), 11, "");
    testi(&tester, index(4, 4), 25, "");
    testi(&tester, index(1, 6), 21, "");

    test_u64(&tester, next_number(20151125), 31916031, "");
    test_u64(&tester, next_number(31916031), 18749137, "");
    test_u64(&tester, next_number(18749137), 16080970, "");

    testi(&tester, number_at(1), 20151125, "");
    testi(&tester, number_at(6), 17289845, "");

    testi(&tester, number_at(index(2947, 3029)), 19980801, "solution to part 1");
    
    return test_summary(&tester);
}
