#include "aoc.h"
#include "utils.h"
#include <stdlib.h>

typedef struct {
    u64 n_age[9];    
} FishPopulation;

u64 count_fish(FishPopulation *fp) {
    u64 sum = 0;
    for(int i = 0; i < 9; ++i) {
        sum += fp->n_age[i];
        // printf("%d=%llu ", i, fp->n_age[i]);
    }
    // puts("");
    return sum;
}

FishPopulation parse_fish(char * data) {
    FishPopulation fp = {0};
    char *token = strtok(data, ",");
    while (token) {
        int age = atoi(token);
        fp.n_age[age]++;
        
        token = strtok(NULL, ",");
    }
    return fp;
}

void simulate_fish(FishPopulation *fp, int days) {
    for(int i = 0; i < days; ++i) {
        u64 new_fish = 0;
        
        new_fish = fp->n_age[0];
        for(int p = 0; p < 8; ++p) {
            fp->n_age[p] = fp->n_age[p + 1];
        }

        fp->n_age[8] = new_fish;
        fp->n_age[6] += new_fish;
    }
}


void test_examples(Tester *tester) {
    test_section("Examples Part 1");

    char data[] = "3,4,3,1,2";

    FishPopulation fish = parse_fish(data);
    testi(tester, count_fish(&fish), 5, "length");

    simulate_fish(&fish, 18);
    testi(tester, count_fish(&fish), 26, "length 18");

    simulate_fish(&fish, 80 - 18);
    testi(tester, count_fish(&fish), 5934, "length 80");


    test_section("Examples Part 2");

    simulate_fish(&fish, 256 - 80);
    test_u64(tester, count_fish(&fish), 26984457539, "length 256");
}

int main() {
    Tester tester = create_tester("Lanternfish");
    test_examples(&tester);

    test_section("Solutions");

    char *data = read_input("../aoc2021/day6/input");
    FishPopulation fish = parse_fish(data);
    simulate_fish(&fish, 80);

    testi(&tester, count_fish(&fish), 361169, "solution to part 1");

    simulate_fish(&fish, 256 - 80);
    test_u64(&tester, count_fish(&fish), 1634946868992, "solution to part 2");

    return test_summary(&tester);
}
