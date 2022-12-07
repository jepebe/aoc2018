import aoc

tester = aoc.Tester("No Space Left On Device")

test_data = """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
"""


def parse_input(data: str = None) -> list[str]:
    if not data:
        data = aoc.read_input()

    return [line for line in data.splitlines()]


def print_fs(fs: dict, prefix: str = ""):
    if fs["name"] == "/":
        print(f"{prefix}- / (dir, size={fs['size']})")
        prefix += "  "

    for key, value in fs["children"].items():
        if not value["dir"]:
            print(f"{prefix}- {key} (file, size={value['size']})")
        else:
            print(f"{prefix}- {key} (dir, size={value['size']})")
            print_fs(value, prefix=prefix + "  ")


def calculate_directory_sizes(fs: dict):
    for key, value in fs["children"].items():
        if value["dir"]:
            calculate_directory_sizes(value)
            fs["size"] += value["size"]
        else:
            fs["size"] += value["size"]


def cli(ops: list[str]):
    fs = {"dir": True, "size": 0, "name": "/", "children": {}}
    cwd = []
    for line in ops:
        if line.startswith("$"):
            cmd = line[2:]
            if cmd.startswith("cd"):
                directory = cmd[3:]
                if directory == "..":
                    cwd.pop()
                elif directory == "/":
                    cwd = [fs]
                else:
                    cwd.append(cwd[-1]["children"][directory])
            elif cmd == "ls":
                pass
            else:
                raise UserWarning(f"Unknown command {cmd}")
        elif line.startswith("dir"):
            directory = line[4:]
            cwd[-1]["children"][directory] = {"dir": True, "size": 0, "name": directory, "children": {}}
        else:
            size, name = line.split(sep=" ")
            cwd[-1]["children"][name] = {"dir": False, "size": int(size), "name": name}

    calculate_directory_sizes(fs)
    # print_fs(fs)
    return fs


def limit_sum(fs: dict, limit: int = 100000) -> int:
    if not fs["dir"]:
        return 0

    size = fs["size"] if fs["size"] <= limit else 0
    for node in fs["children"].values():
        size += limit_sum(node, limit)

    return size


def collect_directory_sizes(fs: dict) -> list[int]:
    if not fs["dir"]:
        return []
    else:
        directories = [fs["size"]]
        for node in fs["children"].values():
            directories.extend(collect_directory_sizes(node))
        return directories


def find_best_fit(fs: dict) -> int:
    directories = collect_directory_sizes(fs)
    total = 70000000
    required = 30000000
    used = fs["size"]
    free = total - used
    for size in sorted(directories):
        if free + size >= required:
            return size
    return -1


tester.test_section("Tests")
test_fs = cli(parse_input(test_data))
tester.test_value(test_fs["size"], 48381165)
tester.test_value(test_fs["children"]["a"]["children"]["e"]["size"], 584)
tester.test_value(test_fs["children"]["a"]["size"], 94853)
tester.test_value(test_fs["children"]["d"]["size"], 24933642)
tester.test_value(limit_sum(test_fs), 95437)
tester.test_value(find_best_fit(test_fs), 24933642)

tester.test_section("Part 1")
fs = cli(parse_input())
tester.test_value(limit_sum(fs), 1348005, "solution to part 1=%s")

tester.test_section("Part 2")
tester.test_value(find_best_fit(fs), 12785886, "solution to part 2=%s")
