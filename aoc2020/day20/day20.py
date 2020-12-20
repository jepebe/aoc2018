import intcode as ic

tester = ic.Tester('Jurassic Jigsaw')


def read_monster():
    with open(f'sea_monster') as f:
        lines = f.read().splitlines(keepends=False)

    monster = {}
    y = 0
    for line in lines:
        for x, c in enumerate(line):
            if c == '#':
                monster[x, y] = c
        y += 1
    return monster


def read_file(postfix=''):
    with open(f'input{postfix}') as f:
        lines = f.read().splitlines(keepends=False)
    return lines


def parse(lines):
    tiles = {}
    tile = None
    tile_id = None
    y = 0
    for line in lines:
        if line.startswith('Tile'):
            if tile:
                tiles[tile_id] = tile
            tile_id = int(line[4:9])
            y = 0
            tile = {}
        else:
            for x, c in enumerate(line):
                tile[x, y] = c
            y += 1
    tiles[tile_id] = tile
    # for tid in tiles:
    #     print(f'Tile {tid}:')
    #     ic.print_map(tiles[tid], {'#': '#', '.': '.'})
    return tiles


def find_edges(tiles):
    edges = {}
    for tid, tile in tiles.items():
        edges[tid] = {'top': [], 'bottom': [], 'left': [], 'right': []}
        for i in range(10):
            edges[tid]['top'].append(tile[i, 0])
            edges[tid]['bottom'].append(tile[i, 9])
            edges[tid]['left'].append(tile[0, i])
            edges[tid]['right'].append(tile[9, i])

        edges[tid]['top'] = ''.join(edges[tid]['top'])
        edges[tid]['bottom'] = ''.join(edges[tid]['bottom'])
        edges[tid]['left'] = ''.join(edges[tid]['left'])
        edges[tid]['right'] = ''.join(edges[tid]['right'])
    # print(edges[tid])
    return edges


def find_corners(tiles):
    tile_edges = find_edges(tiles)
    match_count = {}
    for tid, edges in tile_edges.items():
        match_count[tid] = 0
        for otid, oedges in tile_edges.items():
            if tid != otid:
                for side, edge in edges.items():
                    for oside, oedge in oedges.items():
                        # print(f'{edge} {oedge}')
                        if edge == oedge:
                            # print(f'match {tid} {side} {otid} {oside} ')
                            match_count[tid] += 1
                        elif edge == oedge[::-1]:
                            # print(f'reverse match {tid} {side} {otid} {oside}')
                            match_count[tid] += 1
    prod = 1
    corners = []
    for tid, count in match_count.items():
        if count == 2:
            prod *= tid
            corners.append(tid)
    return prod, corners


def transpose(tile, size=10):
    new_tile = {}
    for y in range(size):
        for x in range(size):
            new_tile[y, x] = tile[x, y]
    return new_tile


def flip_horizontal(tile, size=10):
    new_tile = {}
    for y in range(size):
        for x in range(size):
            new_tile[size - 1 - x, y] = tile[x, y]
    return new_tile


def flip_vertical(tile, size=10):
    new_tile = {}
    for y in range(size):
        for x in range(size):
            new_tile[x, size - 1 - y] = tile[x, y]
    return new_tile


def rotate90(tile, size=10):
    tile = transpose(tile, size)
    tile = flip_horizontal(tile, size)
    return tile


def check_right_edge(tile, otile):
    for i in range(10):
        if tile[9, i] != otile[0, i]:
            return False
    return True


def check_left_edge(tile, otile):
    for i in range(10):
        if tile[0, i] != otile[9, i]:
            return False
    return True


def check_top_edge(tile, otile):
    for i in range(10):
        if tile[i, 0] != otile[i, 9]:
            return False
    return True


def check_bottom_edge(tile, otile):
    for i in range(10):
        if tile[i, 9] != otile[i, 0]:
            return False
    return True


def check_if_adjacent(tile, otile):
    if check_right_edge(tile, otile):
        return True, 1, 0
    elif check_bottom_edge(tile, otile):
        return True, 0, 1
    elif check_left_edge(tile, otile):
        return True, -1, 0
    elif check_top_edge(tile, otile):
        return True, 0, -1
    return False, 0, 0


def create_grid(tiles, arrangement):
    min_x = 144
    max_x = -144
    min_y = 144
    max_y = -144
    lookup = {}
    for tid, (x, y) in arrangement.items():
        if x <= min_x and y <= min_y:
            min_x = x
            min_y = y
        if x >= max_x and y >= max_y:
            max_x = x
            max_y = y
        lookup[x, y] = tid

    extents = ic.find_extents_nd(tiles[lookup[0, 0]], 2)
    grid = {}
    gy = 0
    for y in range(min_y, max_y + 1):
        gx = 0
        for x in range(min_x, max_x + 1):
            tile = tiles[lookup[x, y]]
            for (tx, ty), c in tile.items():
                if tx != 0 and tx != extents[0][1] and ty != 0 and ty != extents[1][1]:
                    grid[gx + tx - 1, gy + ty - 1] = c
            gx += extents[0][1] - 1
        gy += extents[1][1] - 1
    # ic.print_map(grid, {'#': '#', '.': '.'})
    return grid


def arrange(tiles):
    arrangement = {}
    tid = list(tiles.keys())[0]
    arrangement[tid] = (0, 0)
    queue = [tid]

    while queue:
        tid = queue.pop(0)
        tile = tiles[tid]
        x, y = arrangement[tid]

        for otid, otile in tiles.items():
            if tid != otid and otid not in arrangement:
                adj, dx, dy = check_if_adjacent(tile, otile)
                if adj:
                    arrangement[otid] = (x + dx, y + dy)
                    queue.append(otid)
                    continue

                tile90 = rotate90(otile)
                adj, dx, dy = check_if_adjacent(tile, tile90)
                if adj:
                    arrangement[otid] = (x + dx, y + dy)
                    queue.append(otid)
                    tiles[otid] = tile90
                    continue

                tile180 = rotate90(tile90)
                adj, dx, dy = check_if_adjacent(tile, tile180)
                if adj:
                    arrangement[otid] = (x + dx, y + dy)
                    queue.append(otid)
                    tiles[otid] = tile180
                    continue

                tile270 = rotate90(tile180)
                adj, dx, dy = check_if_adjacent(tile, tile270)
                if adj:
                    arrangement[otid] = (x + dx, y + dy)
                    queue.append(otid)
                    tiles[otid] = tile270
                    continue

                tile_flip_v = flip_vertical(otile)
                adj, dx, dy = check_if_adjacent(tile, tile_flip_v)
                if adj:
                    arrangement[otid] = (x + dx, y + dy)
                    queue.append(otid)
                    tiles[otid] = tile_flip_v
                    continue

                tile_flip_v = flip_vertical(tile90)
                adj, dx, dy = check_if_adjacent(tile, tile_flip_v)
                if adj:
                    arrangement[otid] = (x + dx, y + dy)
                    queue.append(otid)
                    tiles[otid] = tile_flip_v
                    continue

                tile_flip_h = flip_horizontal(otile)
                adj, dx, dy = check_if_adjacent(tile, tile_flip_h)
                if adj:
                    arrangement[otid] = (x + dx, y + dy)
                    queue.append(otid)
                    tiles[otid] = tile_flip_h
                    continue

    return create_grid(tiles, arrangement)


def find_sea_monster(grid, monster):
    monster_ext = ic.find_extents_nd(monster, 2)
    ext = ic.find_extents_nd(grid, 2)
    unique_monster_points = set()
    for dy in range(ext[1][1] - monster_ext[1][1]):
        for dx in range(ext[0][1] - monster_ext[0][1]):
            monster_points = []
            for mx, my in monster:
                if grid[mx + dx, my + dy] == '#':
                    monster_points.append((mx + dx, my + dy))
            if len(monster_points) == len(monster):
                for p in monster_points:
                    unique_monster_points.add(p)

    return sum(1 for p in grid if grid[p] == '#' and p not in unique_monster_points)


def search_for_monster(grid):
    monster = read_monster()
    ext = ic.find_extents_nd(grid, 2)
    max_points = sum(1 for p in grid if grid[p] == '#')

    count = find_sea_monster(grid, monster)
    if count != max_points:
        return count

    rotate_grid = rotate90(grid, ext[0][1] + 1)
    count = find_sea_monster(rotate_grid, monster)
    if count != max_points:
        return count

    rotate_grid = rotate90(rotate_grid, ext[0][1] + 1)
    count = find_sea_monster(rotate_grid, monster)
    if count != max_points:
        return count

    rotate_grid = rotate90(rotate_grid, ext[0][1] + 1)
    count = find_sea_monster(rotate_grid, monster)
    if count != max_points:
        return count

    flip_grid = flip_vertical(grid, ext[0][1] + 1)
    count = find_sea_monster(flip_grid, monster)
    if count != max_points:
        return count

    flip_grid = flip_horizontal(grid, ext[0][1] + 1)
    count = find_sea_monster(flip_grid, monster)
    if count != max_points:
        return count

    rotate_grid = rotate90(grid, ext[0][1] + 1)
    flip_grid = flip_horizontal(rotate_grid, ext[0][1] + 1)
    count = find_sea_monster(flip_grid, monster)
    if count != max_points:
        return count


tiles = parse(read_file('_example'))
grid = arrange(tiles)

tester.test_value(find_corners(tiles)[0], 20899048083289)
tester.test_value(search_for_monster(grid), 273)

tiles = parse(read_file(''))
grid = arrange(tiles)
tester.test_value(find_corners(tiles)[0], 18482479935793, 'solution to part 1=%s')
tester.test_value(search_for_monster(grid), 2118, 'solution to part 2=%s')
