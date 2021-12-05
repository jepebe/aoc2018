#include "aoc.h"
#include "utils.h"

void test_examples(Tester *tester) {
    test_section("Examples Part 1");

    testi(tester, 0, 0, "");

    test_section("Examples Part 2");

    testi(tester, 0, 0, "");
}

int main() {
    Tester tester = create_tester("");
    test_examples(&tester);

    test_section("Solutions");

    char *data = read_input("../aoc2021/day6/input");
    (void)data;

    testi(&tester, 0, 0, "solution to part 1");
    
    testi(&tester, 0, 0, "solution to part 2");

    return test_summary(&tester);
}
