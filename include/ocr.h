#pragma once
#include "aoc.h"

#define GLYPH_WIDTH 5
#define GLYPH_HEIGHT 6

typedef struct {
    char type;
    char pixels[GLYPH_WIDTH * GLYPH_HEIGHT];
} Glyph;

Glyph GLYPHS[18] = {
    {.type = 'A', .pixels = {" ##  "
                             "#  # "
                             "#  # "
                             "#### "
                             "#  # "
                             "#  # "}},
    {.type = 'B', .pixels = {"###  "
                             "#  # "
                             "###  "
                             "#  # "
                             "#  # "
                             "###  "}},
    {.type = 'C', .pixels = {" ##  "
                             "#  # "
                             "#    "
                             "#    "
                             "#  # "
                             " ##  "}},
    //{0}, // D
    {.type = 'E', .pixels = {"#### "
                             "#    "
                             "###  "
                             "#    "
                             "#    "
                             "#### "}},
    {.type = 'F', .pixels = {"#### "
                             "#    "
                             "###  "
                             "#    "
                             "#    "
                             "#    "}},
    {.type = 'G', .pixels = {" ##  "
                             "#  # "
                             "#    "
                             "# ## "
                             "#  # "
                             " ### "}},
    {.type = 'H', .pixels = {"#  # "
                             "#  # "
                             "#### "
                             "#  # "
                             "#  # "
                             "#  # "}},
    {.type = 'I', .pixels = {"###  "
                             " #   "
                             " #   "
                             " #   "
                             " #   "
                             "###  "}},
    {.type = 'J', .pixels = {"  ## "
                             "   # "
                             "   # "
                             "   # "
                             "#  # "
                             " ##  "}},
    {.type = 'K', .pixels = {"#  # "
                             "# #  "
                             "##   "
                             "# #  "
                             "# #  "
                             "#  # "}},
    {.type = 'L', .pixels = {"#    "
                             "#    "
                             "#    "
                             "#    "
                             "#    "
                             "#### "}},
    //{0}, //M
    //{0}, //N
    {.type = '0', .pixels = {" ##  "
                             "#  # "
                             "#  # "
                             "#  # "
                             "#  # "
                             " ##  "}},
    {.type = 'P', .pixels = {"###  "
                             "#  # "
                             "#  # "
                             "###  "
                             "#    "
                             "#    "}},
    //{0}, //Q
    {.type = 'R', .pixels = {"###  "
                             "#  # "
                             "#  # "
                             "###  "
                             "# #  "
                             "#  # "}},
    {.type = 'S', .pixels = {" ### "
                             "#    "
                             "#    "
                             " ##  "
                             "   # "
                             "###  "}},
    //{0}, //T
    {.type = 'U', .pixels = {"#  # "
                             "#  # "
                             "#  # "
                             "#  # "
                             "#  # "
                             " ##  "}},
    //{0}, //V
    //{0}, //W
    //{0}, //X
    {.type = 'Y', .pixels = {"#   #"
                             "#   #"
                             " # # "
                             "  #  "
                             "  #  "
                             "  #  "}},
    {.type = 'Z', .pixels = {"#### "
                             "   # "
                             "  #  "
                             " #   "
                             "#    "
                             "#### "}},
};

// OCR function returns true if grid point is set
typedef bool (*OCR)(int x, int y, void *ctx);

char ocr(int x, int y, OCR ocr, void *ctx) {
    for (int g = 0; g < 18; ++g) {
        Glyph *glyph = &GLYPHS[g];
        bool glyph_match = true;

        for (int i = 0; i < GLYPH_HEIGHT; ++i) {
            for (int j = 0; j < GLYPH_WIDTH; ++j) {
                int idx = i * GLYPH_WIDTH + j;
                bool pixel_set = glyph->pixels[idx] == '#';
                if (ocr(x + j, y + i, ctx) != pixel_set) {
                    glyph_match = false;
                    break;
                }
            }
            if (!glyph_match) {
                break;
            }
        }
        if (glyph_match) {
            return glyph->type;
        }
    }
    return '\0';
}
