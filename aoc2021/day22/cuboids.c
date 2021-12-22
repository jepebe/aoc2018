#include "aoc.h"

typedef struct {
    s32 from;
    s32 to;
} Range;

typedef struct {
    Range x;
    Range y;
    Range z;
    bool on;
    bool in_init_area;
    u64 size;
} Cuboid;

void print_cuboid(Cuboid *cuboid) {
    s32 x1 = cuboid->x.from;
    s32 x2 = cuboid->x.to;
    s32 y1 = cuboid->y.from;
    s32 y2 = cuboid->y.to;
    s32 z1 = cuboid->z.from;
    s32 z2 = cuboid->z.to;
    u64 s = cuboid->size;
    printf("x=%d..%d y=%d..%d z=%d..%d size=%llu\n", x1, x2, y1, y2, z1, z2, s);
}

void size_cuboid(Cuboid *cuboid) {
    u64 dx = cuboid->x.to - cuboid->x.from + 1;
    u64 dy = cuboid->y.to - cuboid->y.from + 1;
    u64 dz = cuboid->z.to - cuboid->z.from + 1;
    // if (dx * dy * dz == 0) {
    //     printf("size == 0 <- %llu %llu %llu ", dx, dy, dz);
    //     print_cuboid(cuboid);
    // }
    cuboid->size = dx * dy * dz;
}

Cuboid create_cuboid(s32 x1, s32 y1, s32 z1, s32 x2, s32 y2, s32 z2) {
    Cuboid c = {0};
    c.x.from = x1;
    c.x.to = x2;
    c.y.from = y1;
    c.y.to = y2;
    c.z.from = z1;
    c.z.to = z2;
    size_cuboid(&c);
    return c;
}

bool has_overlap(Cuboid *a, Cuboid *b) {
    bool overlap_x = a->x.from <= b->x.to && a->x.to >= b->x.from;
    bool overlap_y = a->y.from <= b->y.to && a->y.to >= b->y.from;
    bool overlap_z = a->z.from <= b->z.to && a->z.to >= b->z.from;
    return overlap_x && overlap_y && overlap_z;
}

Cuboid intersection(Cuboid *a, Cuboid *b) {
    Cuboid c = {0};

    if (a->x.from >= b->x.from && a->x.from <= b->x.to) {
        c.x.from = a->x.from;
    } else {
        c.x.from = b->x.from;
    }

    if (a->x.to >= b->x.from && a->x.to <= b->x.to) {
        c.x.to = a->x.to;
    } else {
        c.x.to = b->x.to;
    }

    if (a->y.from >= b->y.from && a->y.from <= b->y.to) {
        c.y.from = a->y.from;
    } else {
        c.y.from = b->y.from;
    }

    if (a->y.to >= b->y.from && a->y.to <= b->y.to) {
        c.y.to = a->y.to;
    } else {
        c.y.to = b->y.to;
    }

    if (a->z.from >= b->z.from && a->z.from <= b->z.to) {
        c.z.from = a->z.from;
    } else {
        c.z.from = b->z.from;
    }

    if (a->z.to >= b->z.from && a->z.to <= b->z.to) {
        c.z.to = a->z.to;
    } else {
        c.z.to = b->z.to;
    }

    size_cuboid(&c);
    return c;
}

void test_cuboids(Tester *tester) {
    test_section("Cuboids");
    Cuboid a = create_cuboid(0, 0, 0, 5, 5, 5);
    test(tester, has_overlap(&a, &a), "self");

    Cuboid b = create_cuboid(5, 5, 5, 6, 6, 6);
    test(tester, has_overlap(&a, &b), "corner");
    test(tester, has_overlap(&b, &a), "corner");

    Cuboid iab = intersection(&a, &b);
    Cuboid iba = intersection(&b, &a);
    testi(tester, iab.x.from, b.x.from, NULL);
    testi(tester, iba.x.from, b.x.from, NULL);
    testi(tester, iab.x.to, a.x.to, NULL);
    testi(tester, iba.x.to, a.x.to, NULL);
    testi(tester, iab.y.from, b.y.from, NULL);
    testi(tester, iba.y.from, b.y.from, NULL);
    testi(tester, iab.y.to, a.y.to, NULL);
    testi(tester, iba.y.to, a.y.to, NULL);
    testi(tester, iab.z.from, b.z.from, NULL);
    testi(tester, iba.z.from, b.z.from, NULL);
    testi(tester, iab.z.to, a.z.to, NULL);
    testi(tester, iba.z.to, a.z.to, NULL);
    testi(tester, iba.size, 1, NULL);

    Cuboid c = create_cuboid(6, 6, 6, 10, 10, 10);
    test(tester, !has_overlap(&a, &c), "miss");
    test(tester, has_overlap(&b, &c), "corner");

    Cuboid ibc = intersection(&b, &c);
    Cuboid icb = intersection(&c, &b);
    testi(tester, ibc.x.from, b.x.to, "");
    testi(tester, icb.x.from, b.x.to, "");
    testi(tester, ibc.x.to, c.x.from, "");
    testi(tester, icb.x.to, c.x.from, "");

    a = create_cuboid(0, 0, 0, 5, 5, 5);
    b = create_cuboid(3, 3, 3, 7, 7, 7);
    c = intersection(&a, &b);
    testi(tester, c.x.from, 3, NULL);
    testi(tester, c.y.from, 3, NULL);
    testi(tester, c.z.from, 3, NULL);
    testi(tester, c.x.to, 5, NULL);
    testi(tester, c.y.to, 5, NULL);
    testi(tester, c.z.to, 5, NULL);
    testi(tester, c.size, 3 * 3 * 3, NULL);

    a = create_cuboid(0, 0, 0, 5, 5, 5);
    b = create_cuboid(3, 3, 3, 4, 4, 4);
    c = intersection(&a, &b);
    testi(tester, c.x.from, 3, NULL);
    testi(tester, c.y.from, 3, NULL);
    testi(tester, c.z.from, 3, NULL);
    testi(tester, c.x.to, 4, NULL);
    testi(tester, c.y.to, 4, NULL);
    testi(tester, c.z.to, 4, NULL);
    testi(tester, c.size, 2 * 2 * 2, NULL);
}
