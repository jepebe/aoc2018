def create_layers(image_data, w, h):
    image_size = w * h
    layer_count = len(image_data) / image_size
    layers = [image_data[i * image_size:(i + 1) * image_size] for i in range(int(layer_count))]
    return layers


def find_checksum(layers):
    hists = {}
    min_zero_layer = (-1, 9999)
    for lno, layer in enumerate(layers):
        hist = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}
        for i in layer:
            hist[int(i)] += 1
        hists[lno] = hist

        if hist[0] < min_zero_layer[1]:
            min_zero_layer = (lno, hist[0])
    checksum = hists[min_zero_layer[0]][1] * hists[min_zero_layer[0]][2]
    return checksum


layers = list(create_layers('123456789012', 3, 2))
checksum = find_checksum(layers)

assert checksum == 1


with open('input') as f:
    image_data = f.readline().strip()

layers = create_layers(image_data, 25, 6)
print('checksum %s' % find_checksum(layers))

print(f'layer count = {len(layers)}')
pixels = []
for pixel in zip(*layers):
    for p in pixel:
        if p != '2':
            pixels.append(' ' if p == '0' else '*')
            break

for y in range(6):
    print(''.join(pixels[y * 25:(y + 1) * 25]))
