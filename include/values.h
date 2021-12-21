#pragma once
#include "aoc.h"
#include <string.h>

typedef struct {
    s16 x;
    s16 y;
} Point;

typedef struct {
    s32 x;
    s32 y;
    s32 z;
} Point3D;



typedef enum {
    VAL_BOOL,
    VAL_NIL,
    VAL_CHAR,
    VAL_POINT,
    VAL_POINT3D,
    VAL_SIGNED_64,
    VAL_UNSIGNED_64,
    VAL_STRING,
    VAL_PTR
} ValueType;

typedef struct {
    ValueType type;
    union {
        bool boolean;
        u64 unsigned_64;
        s64 signed_64;
        Point point;
        Point3D point3d;
        char *string;
        char character;
        void *ptr;
    } as;
} Value;

#define BOOL_VAL(value) ((Value){VAL_BOOL, {.boolean = value}})

#define NIL_VAL ((Value){VAL_NIL, {.unsigned_64 = 0}})
#define IS_NIL(value) ((value).type == VAL_NIL)

#define IS_POINT(value) ((value).type == VAL_POINT)
#define POINT_VAL(x, y) ((Value){VAL_POINT, {.point = (Point){x, y}}})

#define IS_POINT3D(value) ((value).type == VAL_POINT3D)
#define POINT3D_VAL(x, y, z) ((Value){VAL_POINT3D, {.point3d = (Point3D){x, y, z}}})
#define AS_POINT3D_VAL(p) ((Value){VAL_POINT3D, {.point3d = p}})

#define IS_STRING(value) ((value).type == VAL_STRING)
#define STRING_VAL(value) ((Value){VAL_STRING, {.string = value}})

#define IS_POINTER(value) ((value).type == VAL_PTR)
#define POINTER_VAL(value) ((Value){VAL_PTR, {.ptr = value}})

#define IS_CHAR(value) ((value).type == VAL_CHAR)
#define CHAR_VAL(value) ((Value){VAL_CHAR, {.character = value}})

#define SIGNED_VAL(value) ((Value){VAL_SIGNED_64, {.signed_64 = value}})
#define UNSIGNED_VAL(value) ((Value){VAL_UNSIGNED_64, {.unsigned_64 = value}})

bool is_value_equal(const Value *a, const Value *b) {
    if (a->type != b->type) {
        return false;
    } else if (a->type == VAL_UNSIGNED_64) {
        return a->as.unsigned_64 == b->as.unsigned_64;
    } else if (a->type == VAL_SIGNED_64) {
        return a->as.signed_64 == b->as.signed_64;
    } else if (a->type == VAL_CHAR) {
        return a->as.character == b->as.character;
    } else if (a->type == VAL_PTR) {
        return a->as.ptr == b->as.ptr;
    } else if (a->type == VAL_NIL) {
        return true;
    } else if (a->type == VAL_POINT) {
        const Point *p1 = &a->as.point;
        const Point *p2 = &b->as.point;
        return p1->x == p2->x && p1->y == p2->y;
    } else if (a->type == VAL_POINT3D) {
        const Point3D *p1 = &a->as.point3d;
        const Point3D *p2 = &b->as.point3d;
        return p1->x == p2->x && p1->y == p2->y && p1->z == p2->z;
    } else if (a->type == VAL_STRING) {
        const char *s1 = a->as.string;
        const char *s2 = b->as.string;
        return strcmp(s1, s2) == 0;
    } else {
        printf("equals: Unknown value type %d\n", a->type);
        return false;
    }
}

u32 hash_string(const char *key, int length) {
    u32 hash = 2166136261u;

    for (int i = 0; i < length; i++) {
        hash ^= (unsigned)key[i];
        hash *= 16777619u;
    }

    return hash;
}

u32 hash_point(const Point *p) {
    u32 hash = 2166136261u;

    hash ^= (unsigned)p->x;
    hash *= 16777619u;

    hash ^= (unsigned)p->y;
    hash *= 16777619u;

    return hash;
}

u32 hash_point3d(const Point3D *p) {
    u32 hash = 2166136261u;

    hash ^= (unsigned)p->x;
    hash *= 16777619u;

    hash ^= (unsigned)p->y;
    hash *= 16777619u;

    hash ^= (unsigned)p->z;
    hash *= 16777619u;

    return hash;
}

u32 hash_u64(u64 n) {
    u32 hash = 2166136261u;
    hash ^= (n >> 32) ^ (n & 0xFFFFFFFF);
    hash *= 16777619u;
    return hash;
}

u32 hash_s64(s64 n) {
    u32 hash = 2166136261u;
    hash ^= (n >> 32) ^ (n & 0xFFFFFFFF);
    hash *= 16777619u;
    return hash;
}

u32 hash_value(const Value *value) {
    if (value->type == VAL_POINT) {
        return hash_point(&value->as.point);
    } else if (value->type == VAL_POINT3D) {
        return hash_point3d(&value->as.point3d);
    } else if (value->type == VAL_UNSIGNED_64) {
        return hash_u64(value->as.unsigned_64);
    } else if (value->type == VAL_SIGNED_64) {
        return hash_s64(value->as.signed_64);
    } else if (value->type == VAL_CHAR) {
        return hash_s64(value->as.character);
    } else if (value->type == VAL_PTR) {
        return hash_u64((u64) value->as.ptr);
    } else if (value->type == VAL_STRING) {
        return hash_string(value->as.string, strlen(value->as.string));
    } else {
        printf("hash: Unknown value type %d\n", value->type);
    }
    return 0;
}
