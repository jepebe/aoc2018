import aoc

tester = aoc.Tester('Calorie Counting')

with open("input") as f:
    data = f.read()

elf_data_list = data.split("\n\n")
elf_burden_list = [sum(map(int, elf_data.split())) for elf_data in elf_data_list]
max_elf_burden = max(elf_burden_list)

tester.test_section("Part 1")
tester.test_value(max_elf_burden, 71502, 'solution to part 1=%s')

tester.test_section("Part 2")
max_three_burden = sum(list(reversed(sorted(elf_burden_list)))[:3])
tester.test_value(max_three_burden, 208191, 'solution to part 2=%s')
