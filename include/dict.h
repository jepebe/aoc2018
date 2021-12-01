#pragma once
#include "aoc.h"
#include "values.h"
#include <stdlib.h>

typedef struct {
    Value key;
    Value value;
} Entry;

typedef struct {
    int count;
    int capacity;
    Entry *entries;
} Dict;

Dict *dict_create() {
    Dict *dict = (Dict *)malloc(sizeof(Dict));
    dict->count = 0;
    dict->capacity = -1;
    dict->entries = NULL;
    return dict;
}

static Entry *dict_find_entry(Entry *entries, int capacity, Value *key) {
    u64 hash = hash_value(key);
    u64 index = hash & capacity;
    Entry *tombstone = NULL;
    for (;;) {
        Entry *entry = &entries[index];

        if (IS_NIL(entry->key)) {
            if (IS_NIL(entry->value)) {
                // Empty entry.
                return tombstone != NULL ? tombstone : entry;
            } else {
                // We found a tombstone.
                if (tombstone == NULL) {
                    tombstone = entry;
                }
            }
        } else if (is_value_equal(&entry->key, key)) {
            // We found the key.
            return entry;
        }

        index = (index + 1) & capacity;
    }
}

static void dict_adjust_capacity(Dict *dict, int capacity) {
    Entry *entries = (Entry *)malloc(sizeof(Entry) * (capacity + 1));

    for (int i = 0; i <= capacity; i++) {
        entries[i].key = NIL_VAL;
        entries[i].value = NIL_VAL;
    }

    dict->count = 0;
    for (int i = 0; i <= dict->capacity; i++) {
        Entry *entry = &dict->entries[i];
        if (IS_NIL(entry->key)) {
            continue;
        }

        Entry *dst = dict_find_entry(entries, capacity, &entry->key);
        dst->key = entry->key;
        dst->value = entry->value;
        dict->count++;
    }

    free(dict->entries);

    dict->entries = entries;
    dict->capacity = capacity;
}

static inline int dict_grow_capacity(int capacity) {
    if (capacity < 8) {
        return 8;
    }
    return capacity * 2;
}

bool dict_set(Dict *dict, Value *key, Value value) {
    if (dict->count + 1 > (dict->capacity + 1) * 0.75) {
        int capacity = dict_grow_capacity(dict->capacity + 1) - 1;
        dict_adjust_capacity(dict, capacity);
    }

    Entry *entry = dict_find_entry(dict->entries, dict->capacity, key);

    bool is_new_key = IS_NIL(entry->key);
    if (is_new_key && IS_NIL(entry->value)) {
        dict->count++;
    }

    entry->key = *key;
    entry->value = value;
    return is_new_key;
}

bool dict_get(Dict *dict, Value *key, Value *value) {
    if (dict->count == 0) {
        return false;
    }
    Entry *entry = dict_find_entry(dict->entries, dict->capacity, key);
    if (IS_NIL(entry->key)) {
        return false;
    }

    *value = entry->value;
    return true;
}

bool dict_contains(Dict *dict, Value *key) {
    if (dict->count == 0) {
        return false;
    }
    Entry *entry = dict_find_entry(dict->entries, dict->capacity, key);
    if (IS_NIL(entry->key)) {
        return false;
    }

    return true;
}

void dict_free(Dict *dict) {
    free(dict->entries);
    free(dict);
}
