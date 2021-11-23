#include "aoc.h"

typedef struct {
    ssize_t floor;
    ssize_t basement;
} Floor;

static Floor find_floor(char * parens) {
    Floor result = (Floor) {0, -1};

    size_t i = 0;

    while (parens[i] != '\0') {
        char p = parens[i];
        if (p == '(') {
            result.floor++;
        } else if(p == ')') {
            result.floor--;
        } else {
            printf("What?\n");
        }

        i++;
        
        if (result.floor == -1 && result.basement == -1) {
            result.basement = i;
        }
    }

    return result;
}

static bool cmp(Floor f1, Floor f2) {
    return f1.floor == f2.floor && (f1.basement == f2.basement);
}

int main() {
    Tester tester = create_tester("Not quite LISP");

    test(&tester, cmp(find_floor("(())"), (Floor) {0, -1}), "");
    test(&tester, cmp(find_floor("()()"), (Floor) {0, -1}), "");
    test(&tester, cmp(find_floor("((("), (Floor) {3, -1}), "");
    test(&tester, cmp(find_floor("(()(()("), (Floor) {3, -1}), "");
    test(&tester, cmp(find_floor("))((((())))"), (Floor) {-1, 1}), "");
    test(&tester, cmp(find_floor(")))"), (Floor) {-3, 1}), "");
    test(&tester, cmp(find_floor(")())())"), (Floor) {-3, 1}), "");

    char * parens = read_input("../aoc2015/day1/input");
    Floor result = find_floor(parens);
    ssize_t floor = result.floor;
    ssize_t basement = result.basement;
    test(&tester, floor == 74, "");
    test(&tester, basement == 1795, "");

    printf("Santa ends up on floor %zd enters the basement at %zd\n", floor, basement);

    test_summary(&tester);
}
