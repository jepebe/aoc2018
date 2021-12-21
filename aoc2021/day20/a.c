#include "aoc.h"
#include "dict.h"
#include "utils.h"
#include <stdlib.h>

typedef struct {
    u8 bits[512];
    u32 width;
    u32 height;
    u8 *image;
    u8 void_state;
} Image;

Image parse_image(char *file) {
    char *data = read_input(file);
    Queue *lines = read_lines(data);

    Image image;
    char *binary = lines->head->value.as.string;
    for (int i = 0; i < 512; ++i) {
        image.bits[i] = binary[i] == '.' ? 0 : 1;
    }

    QueueNode *next = lines->head->next;

    image.width = strlen(next->value.as.string);
    image.height = queue_length(lines) - 1;
    image.image = malloc(sizeof(u8) * image.width * image.height);
    image.void_state = image.bits[0];

    int row = 0;
    while (next) {
        char *line = next->value.as.string;
        for (u32 x = 0; x < image.width; ++x) {
            u32 index = row * image.width + x;
            image.image[index] = line[x] == '.' ? 0 : 1;
        }
        row++;
        next = next->next;
    }

    free(data);
    queue_free(lines);
    return image;
}

void copy_bits(const Image *src, Image *dst) {
    for (int i = 0; i < 512; ++i) {
        dst->bits[i] = src->bits[i];
    }
}

u32 index_at(s32 x, s32 y, Image *image, u8 void_state) {
    s32 width = image->width;
    s32 height = image->height;
    u32 index = 0;
    for (int j = -1; j < 2; ++j) {
        for (int i = -1; i < 2; ++i) {
            index <<= 1;
            s32 tx = x + i;
            s32 ty = y + j;
            if (ty >= 0 && ty < height && tx >= 0 && tx < width) {
                u8 pixel = image->image[ty * width + tx];
                index |= pixel & 0x1;
            } else {
                index |= void_state & 0x1;
            }
        }
    }
    return index;
}

Image process_image(Image *image) {
    Image result;
    copy_bits(image, &result);
    result.width = image->width + 2;
    result.height = image->height + 2;
    result.image = malloc(sizeof(u8) * result.width * result.height);

    int bit_index = 0;
    if (image->void_state) {
        bit_index = 0x1FF;
    }
    // in the input the "void" flips state
    result.void_state = image->bits[bit_index];

    for (u32 y = 0; y < result.height; ++y) {
        for (u32 x = 0; x < result.width; ++x) {
            u32 index = index_at(x - 1, y - 1, image, result.void_state);
            result.image[y * result.width + x] = image->bits[index];
        }
    }
    return result;
}

Image process_image_iter(Image *image, int n) {
    Image result = *image;
    for (int i = 0; i < n; ++i) {
        result = process_image(&result);
    }
    return result;
}

void print_image(Image *image) {
    u32 index = 0;
    for (u32 y = 0; y < image->height; ++y) {
        for (u32 x = 0; x < image->width; ++x) {
            if (image->image[index] == 0) {
                printf(".");
            } else {
                printf("#");
            }
            index++;
        }
        puts("");
    }
    printf("Image size: %dx%d\n", image->width, image->height);
}

u32 count_pixels(Image *image) {
    int count = 0;
    for (u32 i = 0; i < image->width * image->height; ++i) {
        count += image->image[i];
    }
    return count;
}

void test_examples(Tester *tester) {
    test_section("Examples Part 1");
    Image image1 = parse_image("../aoc2021/day20/test");
    testi(tester, image1.width, 5, "");
    testi(tester, image1.height, 5, "");

    Image image2 = process_image(&image1);
    testi(tester, image2.width, 7, "");
    testi(tester, image2.height, 7, "");

    Image image3 = process_image(&image2);
    testi(tester, image3.width, 9, "");
    testi(tester, image3.height, 9, "");

    testi(tester, count_pixels(&image3), 35, "");

    test_section("Examples Part 2");

    Image image50 = process_image_iter(&image1, 50);
    testi(tester, count_pixels(&image50), 3351, "");
    //print_image(&image50);
}

int main() {
    Tester tester = create_tester("Trench Map");
    test_examples(&tester);

    test_section("Solutions");

    Image image = parse_image("../aoc2021/day20/input");
    Image result = process_image_iter(&image, 2);

    u32 count = count_pixels(&result);
    test(&tester, count != 5617, "wrong solution to part 1");
    test(&tester, count != 5570, "wrong solution to part 1");
    testi(&tester, count, 5461, "solution to part 1");

    Image image50 = process_image_iter(&image, 50);
    count = count_pixels(&image50);
    //print_image(&image50);

    test(&tester, count != 179256, "wrong solution to part 2"); // too high
    testi(&tester, count, 18226, "solution to part 2");

    return test_summary(&tester);
}
