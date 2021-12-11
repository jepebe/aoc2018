#include "aoc.h"
#include "utils.h"

typedef struct {
    u8 octopus[100];
} Octopus;

void print_octopus(Octopus *octo) {
    for (int y = 0; y < 10; ++y) {
        for (int x = 0; x < 10; ++x) {
            u8 value = octo->octopus[y * 10 + x];
            if (value == 0) {
                printf("\x1b[0;32m%d\x1b[0m", value);
            } else {
                printf("%d", value);
            }
        }
        puts("");
    }
}

Octopus parse_data(char *path) {
    char *data = read_input(path);
    Queue *lines = read_lines(data);

    int index = 0;
    Octopus octo = {0};
    QueueNode *node = lines->head;
    for (int y = 0; y < 10; ++y) {
        char *line = node->value.as.string;
        for (int x = 0; x < 10; ++x) {
            octo.octopus[index++] = line[x] - 48;
        }
        node = node->next;
    }

    queue_free(lines);
    free(data);
    return octo;
}

void increase_energy(Octopus *octo, int x, int y) {
    if (octo->octopus[y * 10 + x] != 0) {
        octo->octopus[y * 10 + x]++;
    }
}

void flash_neighbours(Octopus *octo, int x, int y) {
    octo->octopus[y * 10 + x] = 0;

    if (x - 1 >= 0) {
        if (y - 1 >= 0) {
            increase_energy(octo, x - 1, y - 1);
        }

        increase_energy(octo, x - 1, y);

        if (y + 1 < 10) {
            increase_energy(octo, x - 1, y + 1);
        }
    }

    if (y - 1 >= 0) {
        increase_energy(octo, x, y - 1);
    }

    if (y + 1 < 10) {
        increase_energy(octo, x, y + 1);
    }

    if (x + 1 < 10) {
        if (y - 1 >= 0) {
            increase_energy(octo, x + 1, y - 1);
        }

        increase_energy(octo, x + 1, y);

        if (y + 1 < 10) {
            increase_energy(octo, x + 1, y + 1);
        }
    }
}

int flash_flashable(Octopus *octo) {
    int flashed = 0;
    for (int y = 0; y < 10; ++y) {
        for (int x = 0; x < 10; ++x) {
            int index = y * 10 + x;
            if (octo->octopus[index] > 9) {
                flash_neighbours(octo, x, y);
                flashed++;
            }
        }
    }
    return flashed;
}

int flash(Octopus *octo, int n) {
    int flash_count = 0;
    for (int i = 0; i < n; ++i) {
        for (int y = 0; y < 10; ++y) {
            for (int x = 0; x < 10; ++x) {
                int index = y * 10 + x;
                octo->octopus[index]++;
            }
        }

        int flashed = flash_flashable(octo);
        while (flashed > 0) {
            flash_count += flashed;
            flashed = flash_flashable(octo);
        }
    }

    return flash_count;
}

int find_synchronization_point(Octopus *octo) {
    int flash_count = flash(octo, 1);
    int n = 101; // continue from previous solution
    while(flash_count != 100) {
        flash_count = flash(octo, 1);
        n++;
    }
    return n;
}

void test_examples(Tester *tester) {
    test_section("Examples Part 1");

    Octopus octo = parse_data("../aoc2021/day11/test");
    // print_octopus(&octo);
    // flash(&octo, 1);
    // puts("");
    // print_octopus(&octo);
    // flash(&octo, 1);
    // puts("");
    // print_octopus(&octo);

    testi(tester, flash(&octo, 100), 1656, "flash 100");

    test_section("Examples Part 2");

    testi(tester, find_synchronization_point(&octo), 195, "");
}

int main() {
    Tester tester = create_tester("Dumbo Octopus");
    test_examples(&tester);

    test_section("Solutions");

    Octopus octo = parse_data("../aoc2021/day11/input");

    testi(&tester, flash(&octo, 100), 1679, "solution to part 1");
    testi(&tester, find_synchronization_point(&octo), 519, "solution to part 2");

    return test_summary(&tester);
}
