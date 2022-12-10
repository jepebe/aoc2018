import aoc

tester = aoc.Tester("Tuning Trouble")

tester.test_section("Tests")

test_streams = [
    ("mjqjpqmgbljsphdztnvjfqwrcgsmlb", 7, 19),
    ("bvwbjplbgvbhsrlpgdmjqwftvncz", 5, 23),
    ("nppdvjthqldpwncqszvftbrmjlhg", 6, 23),
    ("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 10, 29),
    ("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 11, 26),
]


def find_start_of_packet(stream: str, packet_size: int) -> int:
    for i in range(len(stream) - (packet_size - 1)):
        seq = stream[i : i + packet_size]
        if len(set(seq)) == packet_size:
            return i + packet_size
    return 0


for sequence, start_of_packet, start_of_message in test_streams:
    tester.test_value(find_start_of_packet(sequence, 4), start_of_packet)
    tester.test_value(find_start_of_packet(sequence, 14), start_of_message)

data = aoc.read_input()

tester.test_section("Part 1")
tester.test_value(find_start_of_packet(data, 4), 1282, "solution to part 1=%s")

tester.test_section("Part 2")
tester.test_value(find_start_of_packet(data, 14), 3513, "solution to part 2=%s")
