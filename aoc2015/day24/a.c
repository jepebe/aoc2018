#include "aoc.h"
#include <stdint.h>

uint8_t data[] = {1, 3, 5, 11, 13, 17, 19, 23, 29,
                  31, 37, 41, 43, 47, 53, 59, 67, 71, 73,
                  79, 83, 89, 97, 101, 103, 107, 109, 113};

uint8_t test_data[] = {1, 2, 3, 4, 5, 7, 8, 9, 10, 11};

typedef struct {
    uint8_t *packages;
    size_t package_count;
    int max_sack_weight;
    uint64_t min_qe;
    uint8_t min_package_count;
    int solution;
    uint8_t sack_count;
} Balancer;

int sum(uint8_t elements[], size_t count) {
    unsigned int s = 0;
    for (size_t i = 0; i < count; ++i) {
        s += elements[i];
    }
    return s;
}

void reverse(uint8_t elements[], size_t count) {
    for (size_t i = 0; i < count / 2; ++i) {
        int t = elements[count - i - 1];
        elements[count - i - 1] = elements[i];
        elements[i] = t;
    }
}

int count_bits(int n, int max_bits) {
    int bits = 0;
    for (int i = 0; i < max_bits; ++i) {
        if (n & 0x1) {
            bits++;
        }
        n >>= 1;
    }
    return bits;
}

int weight(uint8_t elements[], size_t count, int mask) {
    int w = 0;
    for (int i = 0; i < (int)count; ++i) {
        if (mask & 0x1) {
            w += elements[i];
        }
        mask >>= 1;
    }
    return w;
}

uint64_t quantum_entanglement(uint8_t elements[], size_t count, int mask) {
    uint64_t qe = 1;
    for (int i = 0; i < (int)count; ++i) {
        if (mask & 0x1) {
            qe *= elements[i];
        }
        mask >>= 1;
    }
    return qe;
}

uint64_t greedy(Balancer *balancer, int bits, int bit_num) {
    if (bit_num >= (int)balancer->package_count) {
        return balancer->min_qe;
    }

    int current = bits | (0x1 << bit_num);
    int bit_count = count_bits(current, balancer->package_count);

    if (bit_count > balancer->min_package_count) {
        return balancer->min_qe;
    }

    int w = weight(balancer->packages, balancer->package_count, current);

    if (w < balancer->max_sack_weight) {
        // check further with this bit set
        greedy(balancer, current, bit_num + 1);
    } else if (w == balancer->max_sack_weight) {
        uint64_t qe = quantum_entanglement(balancer->packages, balancer->package_count, current);

        if (bit_count < balancer->min_package_count) {
            balancer->min_package_count = bit_count;
            balancer->min_qe = qe;
            balancer->solution = current;
        } else if (bit_count == balancer->min_package_count && qe < balancer->min_qe) {
            balancer->min_qe = qe;
            balancer->solution = current;
        }
    }

    // Check without this bit set
    greedy(balancer, bits, bit_num + 1);

    return balancer->min_qe;
}

Balancer create_balancer(uint8_t packages[], size_t count, int sack_count) {
    Balancer balancer;
    balancer.packages = packages;
    balancer.package_count = count;
    balancer.min_qe = 0xFFFFFFFFFFFFFFFF;
    balancer.min_package_count = 0xFF;
    balancer.solution = 0;
    balancer.sack_count = sack_count;
    balancer.max_sack_weight = sum(packages, count) / sack_count;
    return balancer;
}

int main() {
    Tester tester = create_tester("It Hangs in the Balance");

    testi(&tester, sum(test_data, LEN(test_data)), 60, "sum of test data");
    testi(&tester, sum(data, LEN(data)), 1524, "sum of input data");

    reverse(test_data, LEN(test_data));
    reverse(data, LEN(data));

    Balancer test_balancer = create_balancer(test_data, LEN(test_data), 3);
    testi(&tester, greedy(&test_balancer, 0, 0), 99, "QE test 3 sacks");

    test_balancer = create_balancer(test_data, LEN(test_data), 4);
    testi(&tester, greedy(&test_balancer, 0, 0), 44, "QE test 3 sacks + trunk");

    Balancer balancer = create_balancer(data, LEN(data), 3);
    test_u64(&tester, greedy(&balancer, 0, 0), 10439961859, "solution to part 1");

    balancer = create_balancer(data, LEN(data), 4);
    test_u64(&tester, greedy(&balancer, 0, 0), 72050269, "solution to part 2");

    return test_summary(&tester);
}
