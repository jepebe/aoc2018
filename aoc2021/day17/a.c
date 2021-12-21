#include "aoc.h"
#include "utils.h"

typedef struct {
    s32 x;
    s32 y;
    s32 dx;
    s32 dy;
    s32 initial_dx;
    s32 initial_dy;
    s32 max_y;
    bool hit;
} Probe;

bool probe_in_target(Probe *probe, s32 x1, s32 x2, s32 y1, s32 y2) {
    return x1 <= probe->x && probe->x <= x2 && y1 <= probe->y && probe->y <= y2;
}

void probe_step(Probe *probe) {
    probe->x += probe->dx;
    probe->y += probe->dy;
    if (probe->dx > 0) {
        probe->dx--;
    } else if (probe->dx < 0) {
        probe->dx++;
    }
    probe->dy--;
    if (probe->y > probe->max_y) {
        probe->max_y = probe->y;
    }
}

Probe simulate_probe(s32 dx, s32 dy, s32 x1, s32 x2, s32 y1, s32 y2) {
    Probe probe = {0};
    probe.initial_dx = dx;
    probe.initial_dy = dy;
    probe.dx = dx;
    probe.dy = dy;
    probe.hit = false;
    while (probe.y > y1) {
        probe_step(&probe);

        if (probe_in_target(&probe, x1, x2, y1, y2)) {
            probe.hit = true;
            break;
        }
    }

    return probe;
}

Probe probe_ballistic(s32 x1, s32 x2, s32 y1, s32 y2) {
    Probe max_probe = {0};
    max_probe.hit = false;
    for (int dy = 0; dy < -y1; ++dy) {
        for (int dx = 0; dx < x1; ++dx) {
            Probe p = simulate_probe(dx, dy, x1, x2, y1, y2);
            if(p.hit && p.max_y > max_probe.max_y) {
                max_probe = p;
            }
        }
    }
    return max_probe;
}

s32 probe_hit(s32 x1, s32 x2, s32 y1, s32 y2) {
    s32 hit_count = 0;
    for (int dy = y1; dy <= -y1; ++dy) {
        for (int dx = 0; dx <= x2; ++dx) {
            Probe p = simulate_probe(dx, dy, x1, x2, y1, y2);
            if(p.hit) {
                hit_count++;
                //printf("dx=%d dy=%d\n", p.initial_dx, p.initial_dy);
            }
        }
    }
    return hit_count;
}

void test_examples(Tester *tester) {
    test_section("Examples Part 1");

    Probe probe = simulate_probe(7, 2, 20, 30, -10, -5);
    test(tester, probe.hit, "");
    testi(tester, probe.max_y, 3, "");

    probe = simulate_probe(6, 3, 20, 30, -10, -5);
    test(tester, probe.hit, "");
    testi(tester, probe.max_y, 6, "");

    probe = simulate_probe(9, 0, 20, 30, -10, -5);
    test(tester, probe.hit, "");
    testi(tester, probe.max_y, 0, "");

    probe = simulate_probe(17, -4, 20, 30, -10, -5);
    test(tester, !probe.hit, "");
    testi(tester, probe.max_y, 0, "");

    probe = probe_ballistic(20, 30, -10, -5);
    testi(tester, probe.max_y, 45, "");

    test_section("Examples Part 2");

    testi(tester, probe_hit(20, 30, -10, -5), 112, "");
}

int main() {
    Tester tester = create_tester("Trick Shot");
    test_examples(&tester);

    test_section("Solutions");

    // target area: x=25..67, y=-260..-200
    Probe probe = probe_ballistic(25, 67, -260, -200);
    //printf("dx=%d dy=%d\n", probe.initial_dx, probe.initial_dy);

    testi(&tester, probe.max_y, 33670, "solution to part 1");
    s32 hit_count = probe_hit(25, 67, -260, -200);
    test(&tester, hit_count != 4802, "not solution to part 2");
    test(&tester, hit_count != 2562, "not solution to part 2");
    test(&tester, hit_count != 3877, "not solution to part 2");
    testi(&tester, hit_count, 4903, "solution to part 2");

    return test_summary(&tester);
}
