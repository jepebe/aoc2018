import intcode as ic

tester = ic.Tester('Lobby Layout')


def read_file(postfix=''):
    with open(f'input{postfix}') as f:
        lines = f.read().splitlines(keepends=False)
    return lines


def parse(lines):
    directions = []
    for line in lines:
        tile = []
        i = 0
        while i < len(line):
            if line[i] in ('s', 'n'):
                tile.append(line[i:i + 2])
                i += 1
            else:
                tile.append(line[i])
            i += 1
        directions.append(tile)
    return directions


def flip(tiles):
    grid = {}

    for tile in tiles:
        x, y = 0, 0
        for d in tile:
            if d == 'e':
                x += 1
            elif d == 'w':
                x -= 1
            elif d == 'ne':
                y += 1
            elif d == 'nw':
                x -= 1
                y += 1
            elif d == 'se':
                x += 1
                y -= 1
            elif d == 'sw':
                y -= 1

        if (x, y) not in grid:
            grid[x, y] = False

        grid[x, y] = not grid[x, y]

    return sum(1 for flipped in grid.values() if flipped), grid


def count_black_neighbours(grid, x, y):
    count = 0
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1), (-1, 1), (1, -1)):
        p = (x + dx, y + dy)
        if p in grid and grid[p]:
            count += 1
    return count


def flip_day(grid):
    ext = ic.find_extents_nd(grid, 2)
    new_grid = {}
    for y in range(ext[1][0] - 1, ext[1][1] + 2):
        for x in range(ext[0][0] - 1, ext[0][1] + 2):
            p = (x, y)
            nc = count_black_neighbours(grid, x, y)
            tile = grid[p] if p in grid else False
            if tile:
                if nc == 0 or nc > 2:
                    pass
                else:
                    new_grid[p] = True
            else:
                if nc == 2:
                    new_grid[p] = True

    return new_grid


def run_daily_flip(grid, days):
    for i in range(days):
        grid = flip_day(grid)
    return sum(1 for flipped in grid.values() if flipped)

lines = """sesenwnenenewseeswwswswwnenewsewsw
neeenesenwnwwswnenewnwwsewnenwseswesw
seswneswswsenwwnwse
nwnwneseeswswnenewneswwnewseswneseene
swweswneswnenwsewnwneneseenw
eesenwseswswnenwswnwnwsewwnwsene
sewnenenenesenwsewnenwwwse
wenwwweseeeweswwwnwwe
wsweesenenewnwwnwsenewsenwwsesesenwne
neeswseenwwswnwswswnw
nenwswwsewswnenenewsenwsenwnesesenew
enewnwewneswsewnwswenweswnenwsenwsw
sweneswneswneneenwnewenewwneswswnese
swwesenesewenwneswnwwneseswwne
enesenwswwswneneswsenwnewswseenwsese
wnwnesenesenenwwnenwsewesewsesesew
nenewswnwewswnenesenwnesewesw
eneswnwswnwsenenwnwnwwseeswneewsenese
neswnwewnwnwseenwseesewsenwsweewe
wseweeenwnesenwwwswnew""".splitlines(keepends=False)

tiles = parse(lines)
black, grid = flip(tiles)
tester.test_value(black, 10)
tester.test_value(run_daily_flip(grid, 1), 15)
tester.test_value(run_daily_flip(grid, 2), 12)
tester.test_value(run_daily_flip(grid, 10), 37)
tester.test_value(run_daily_flip(grid, 20), 132)
tester.test_value(run_daily_flip(grid, 100), 2208)

tiles = parse(read_file())
black, grid = flip(tiles)
tester.test_value(black, 549, 'solution to part 1=%s')
tester.test_value(run_daily_flip(grid, 100), 4147, 'solution to part 2=%s')

