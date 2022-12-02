from aoc import Tester, find_extents
from aoc.glyphs import glyph_data


def ocr(grid, look_up, missing=' '):
    minx, maxx, miny, maxy = find_extents(grid)
    characters = []
    for j in range(miny, maxy):
        for i in range(minx, maxx):
            patch = []
            for y in range(6):
                for x in range(5):
                    if (i + x, j + y) in grid:
                        patch.append(look_up[grid[(i + x, j + y)]])
                    else:
                        patch.append(missing)
            patch = ''.join(patch)
            if patch in glyph_data:
                characters.append(glyph_data[patch])
    return ''.join(characters)


if __name__ == '__main__':
    data = {
        (0, 0): 0, (1, 0): 1, (1, 1): 1, (2, 1): 0, (2, 0): 0, (3, 0): 0, (3, 1): 0, (4, 1): 1, (4, 0): 1, (5, 0): 0,
        (5, 1): 0, (6, 1): 1, (6, 0): 1, (7, 0): 1, (7, 1): 0, (8, 1): 0, (8, 0): 1, (9, 0): 1, (9, 1): 0, (10, 1): 0,
        (10, 0): 0, (11, 0): 1, (11, 1): 1, (12, 1): 0, (12, 0): 1, (13, 0): 1, (13, 1): 0, (14, 1): 1, (14, 0): 0,
        (15, 0): 0, (15, 1): 0, (16, 1): 1, (16, 0): 1, (17, 0): 1, (17, 1): 0, (18, 1): 0, (18, 0): 1, (19, 0): 0,
        (19, 1): 1, (20, 1): 0, (20, 0): 0, (21, 0): 1, (21, 1): 1, (22, 1): 0, (22, 0): 1, (23, 0): 1, (23, 1): 0,
        (24, 1): 1, (24, 0): 0, (25, 0): 0, (25, 1): 0, (26, 1): 1, (26, 0): 1, (27, 0): 1, (27, 1): 0, (28, 1): 0,
        (28, 0): 1, (29, 0): 1, (29, 1): 0, (30, 1): 0, (30, 0): 0, (31, 0): 0, (31, 1): 1, (32, 1): 0, (32, 0): 1,
        (33, 0): 1, (33, 1): 0, (34, 1): 1, (34, 0): 0, (35, 0): 0, (35, 1): 0, (36, 1): 0, (36, 0): 0, (37, 0): 0,
        (37, 1): 0, (38, 1): 0, (38, 0): 1, (39, 0): 1, (39, 1): 1, (40, 1): 0, (40, 0): 0, (41, 0): 0, (41, 1): 0,
        (42, 1): 0, (42, 2): 0, (41, 2): 0, (41, 3): 0, (40, 3): 0, (40, 2): 0, (39, 2): 1, (39, 3): 1, (38, 3): 0,
        (38, 2): 0, (37, 2): 0, (37, 3): 0, (36, 3): 0, (36, 2): 0, (35, 2): 0, (35, 3): 0, (34, 3): 1, (34, 2): 0,
        (33, 2): 0, (33, 3): 1, (32, 3): 0, (32, 2): 0, (31, 2): 1, (31, 3): 1, (30, 3): 0, (30, 2): 0, (29, 2): 0,
        (29, 3): 0, (28, 3): 0, (28, 2): 1, (27, 2): 1, (27, 3): 0, (26, 3): 1, (26, 2): 1, (25, 2): 0, (25, 3): 0,
        (24, 3): 0, (24, 2): 1, (23, 2): 0, (23, 3): 1, (22, 3): 1, (22, 2): 0, (21, 2): 1, (21, 3): 1, (20, 3): 0,
        (20, 2): 0, (19, 2): 1, (19, 3): 0, (18, 3): 1, (18, 2): 0, (17, 2): 0, (17, 3): 1, (16, 3): 1, (16, 2): 1,
        (15, 2): 0, (15, 3): 0, (14, 3): 0, (14, 2): 1, (13, 2): 0, (13, 3): 1, (12, 3): 1, (12, 2): 0, (11, 2): 1,
        (11, 3): 1, (10, 3): 0, (10, 2): 0, (9, 2): 0, (9, 3): 0, (8, 3): 0, (8, 2): 1, (7, 2): 1, (7, 3): 0, (6, 3): 1,
        (6, 2): 1, (5, 2): 0, (5, 3): 0, (4, 3): 1, (4, 2): 1, (3, 2): 0, (3, 3): 0, (2, 3): 0, (2, 2): 0, (1, 2): 1,
        (1, 3): 1, (0, 3): 0, (0, 4): 0, (1, 4): 1, (1, 5): 0, (2, 5): 1, (2, 4): 0, (3, 4): 0, (3, 5): 1, (4, 5): 0,
        (4, 4): 1, (5, 4): 0, (5, 5): 0, (6, 5): 1, (6, 4): 1, (7, 4): 0, (7, 5): 1, (8, 5): 1, (8, 4): 0, (9, 4): 0,
        (9, 5): 1, (10, 5): 0, (10, 4): 0, (11, 4): 1, (11, 5): 1, (12, 5): 0, (12, 4): 0, (13, 4): 1, (13, 5): 0,
        (14, 5): 1, (14, 4): 0, (15, 4): 0, (15, 5): 0, (16, 5): 1, (16, 4): 1, (17, 4): 0, (17, 5): 0, (18, 5): 0,
        (18, 4): 0, (19, 4): 0, (19, 5): 0, (20, 5): 0, (20, 4): 0, (21, 4): 1, (21, 5): 1, (22, 5): 0, (22, 4): 0,
        (23, 4): 1, (23, 5): 0, (24, 5): 1, (24, 4): 0, (25, 4): 0, (25, 5): 0, (26, 5): 1, (26, 4): 1, (27, 4): 0,
        (27, 5): 0, (28, 5): 0, (28, 4): 0, (29, 4): 0, (29, 5): 0, (30, 5): 0, (30, 4): 0, (31, 4): 1, (31, 5): 0,
        (32, 5): 1, (32, 4): 0, (33, 4): 0, (33, 5): 1, (34, 5): 1, (34, 4): 1, (35, 4): 0, (35, 5): 0, (36, 5): 0,
        (36, 4): 1, (37, 4): 0, (37, 5): 1, (38, 5): 1, (38, 4): 0, (39, 4): 1, (39, 5): 0, (40, 5): 0, (40, 4): 0
    }

    tester = Tester('ocr')

    result = ocr(data, {0: ' ', 1: '#'})
    tester.test_value(result, 'UERPRFGJ')
    tester.summary()