#include "aoc.h"
#include "utils.h"
#include <stdint.h>

typedef struct {
    u32 length;
    u8 *bits;
    int index;
    u64 version_sum;
    u32 depth;
} Packet;

Packet convert_hex_to_bin(char *hex) {
    int len = strlen(hex);
    Packet packet;
    packet.index = 0;
    packet.depth = 0;
    packet.version_sum = 0;
    packet.length = len * 4;
    packet.bits = malloc(sizeof(u8) * packet.length);
    for (int i = 0; i < len; ++i) {
        char c = hex[i];
        u8 b;
        if (c >= '0' && c <= '9') {
            b = c - '0';
        } else {
            b = c - 'A' + 10;
        }
        packet.bits[i * 4] = (b >> 3) & 0x1;
        packet.bits[i * 4 + 1] = (b >> 2) & 0x1;
        packet.bits[i * 4 + 2] = (b >> 1) & 0x1;
        packet.bits[i * 4 + 3] = b & 0x1;
    }
    return packet;
}

bool compare(Packet *packet, char *data) {
    if (strlen(data) != packet->length) {
        printf("length mismatch\n");
        return false;
    }

    for (int i = 0; i < (int)packet->length; ++i) {
        u8 c = data[i] - '0';
        u8 bit = packet->bits[i];
        if (c != bit) {
            printf("bit mismatch at %d -> %d != %d\n", i, c, bit);
            return false;
        }
    }
    return true;
}

void print_prefix(int depth) {
    for (int i = 0; i < depth; ++i) {
        printf("-");
    }
}

u8 read_bit(Packet *packet) {
    return packet->bits[packet->index++];
}

u64 convert_to_value(Packet *packet, int bit_count) {
    u64 result = 0;
    for (int i = bit_count - 1; i >= 0; --i) {
        result |= (read_bit(packet) & 0x1) << i;
    }
    return result;
}

u64 parse_literal(Packet *packet) {
    u64 literal = 0;

    int group_count = 0;
    u8 group;

    do {
        group = read_bit(packet);
        literal <<= 4;
        literal |= read_bit(packet) << 3;
        literal |= read_bit(packet) << 2;
        literal |= read_bit(packet) << 1;
        literal |= read_bit(packet) << 0;
        group_count++;
    } while (group == 1);

    return literal;
}

u64 parse_packet(Packet *packet);

u64 parse_operator(Packet *packet, u8 type) {
    u8 length_bit = read_bit(packet);
    u64 values[64];
    int packets = 0;
    if (length_bit == 0) {
        int sub_packet_length = convert_to_value(packet, 15);
        int start = packet->index;

        while ((packet->index - start) < sub_packet_length) {
            values[packets++] = parse_packet(packet);
        }
        if ((packet->index - start) > sub_packet_length) {
            printf("\nPacket overflow!\n");
        }
    } else {
        int sub_packet_count = convert_to_value(packet, 11);
        for (int i = 0; i < sub_packet_count; ++i) {
            values[packets++] = parse_packet(packet);
        }
    }
    u64 result = 0;
    switch (type) {
    case 0:
        // sum
        for (int i = 0; i < packets; ++i) {
            result += values[i];
        }
        break;
    case 1:
        // product
        result = values[0];
        for (int i = 1; i < packets; ++i) {
            result *= values[i];
        }
        break;
    case 2:
        // min
        result = values[0];
        for (int i = 1; i < packets; ++i) {
            if (values[i] < result) {
                result = values[i];
            }
        }
        break;
    case 3:
        // max
        result = values[0];
        for (int i = 1; i < packets; ++i) {
            if (values[i] > result) {
                result = values[i];
            }
        }
        break;
    case 5:
        // greater than
        result = values[0] > values[1];
        break;
    case 6:
        // less than
        result = values[0] < values[1];
        break;
    case 7:
        // equal
        result = values[0] == values[1];
        break;
    default:
        printf("What?\n");
    }

    return result;
}

u64 parse_packet(Packet *packet) {
    packet->depth++;

    u8 version = convert_to_value(packet, 3);
    packet->version_sum += version;

    u8 id = convert_to_value(packet, 3);

    u64 result;
    if (id == 4) {
        result = parse_literal(packet);
    } else {
        result = parse_operator(packet, id);
    }

    packet->depth--;
    return result;
}

u64 calculate_version_sum(char *hex) {
    Packet packet = convert_hex_to_bin(hex);
    parse_packet(&packet);
    return packet.version_sum;
}

u64 parse_hex(char *hex) {
    Packet packet = convert_hex_to_bin(hex);
    return parse_packet(&packet);
}

void test_examples(Tester *tester) {
    test_section("Examples Part 1");

    Packet packet = convert_hex_to_bin("D2FE28");
    test(tester, compare(&packet, "110100101111111000101000"), "");
    testi(tester, parse_packet(&packet), 2021, "");

    packet = convert_hex_to_bin("38006F45291200");
    testi(tester, parse_packet(&packet), 1, "");

    packet = convert_hex_to_bin("EE00D40C823060");
    testi(tester, parse_packet(&packet), 3, "");

    testi(tester, calculate_version_sum("8A004A801A8002F478"), 16, "");
    testi(tester, calculate_version_sum("620080001611562C8802118E34"), 12, "");
    testi(tester, calculate_version_sum("C0015000016115A2E0802F182340"), 23, "");
    testi(tester, calculate_version_sum("A0016C880162017C3686B18A3D4780"), 31, "");

    test_section("Examples Part 2");

    test_u64(tester, parse_hex("C200B40A82"), 3, "");
    test_u64(tester, parse_hex("04005AC33890"), 54, "");
    test_u64(tester, parse_hex("880086C3E88112"), 7, "");
    test_u64(tester, parse_hex("CE00C43D881120"), 9, "");
    test_u64(tester, parse_hex("D8005AC2A8F0"), 1, "");
    test_u64(tester, parse_hex("F600BC2D8F"), 0, "");
    test_u64(tester, parse_hex("9C005AC2F8F0"), 0, "");
    test_u64(tester, parse_hex("9C0141080250320F1802104A08"), 1, "");
}

int main() {
    Tester tester = create_tester("Packet Decoder");
    test_examples(&tester);

    test_section("Solutions");

    char *data = read_input("../aoc2021/day16/input");
    testi(&tester, calculate_version_sum(data), 984, "solution to part 1");
    test(&tester, parse_hex(data) != 1708615090, "wrong solution to part 2");
    test_u64(&tester, parse_hex(data), 1015320896946, "solution to part 2");

    return test_summary(&tester);
}
