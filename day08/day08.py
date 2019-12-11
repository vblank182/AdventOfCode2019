## Advent of Code 2019: Day 8
## https://adventofcode.com/2019/day/8
## Jesse Williams | github.com/vblank182
## Answers: [Part 1]: 1474, [Part 2]: JCRCB

from collections import Counter
from PIL import Image

if __name__ == '__main__':

    # Image and layer properties
    img_w = 25
    img_h = 6
    layer_size = img_w*img_h

    # Split image data into layers
    with open("day08_input.txt") as f:
        data = f.readline()[:-1]
        if len(data) % layer_size == 0:
            layers = []
            for i in range( int(len(data)/layer_size) ):
                layers.append(data[layer_size*(i) : layer_size*(i+1)])
        else:
            print("Error: Image data length not a multiple of layer size.")

    # Make a list of digit counts for each layer
    layerDigits = []
    for layer in layers:
        layerDigits.append(Counter(layer))

    leastZeroAmount = len(layers[0])
    for idx, lCount in enumerate(layerDigits):
        if lCount['0'] < leastZeroAmount:
            leastZeroAmount = lCount['0']
            leastZeroLayer = (idx, layers[idx])
            leastZeroLayerCount = lCount

    leastZeroChecksum = leastZeroLayerCount['1']*leastZeroLayerCount['2']

    print("[Part 1] Layer #{} has the fewest '0' digits at {}. This layer's checksum (1's multiplied by 2's) is {}.".format(leastZeroLayer[0], leastZeroAmount, leastZeroChecksum))

    # Color constants
    C_BLACK, C_WHITE, C_TRNSP = (0,0,0), (240,240,240), (255, 255, 255)

    # Generate a string of pixels for the final image with colors determined by reading through all layers
    finalImagePixels = [2]*layer_size
    for px in range(layer_size):
        for layer in layers:
            if layer[px] == '0':                  # if a black pixel is reached,
                finalImagePixels[px] = C_BLACK    # color final image pixel black and stop checking layers
                break
            elif layer[px] == '1':                # if a white pixel is reached,
                finalImagePixels[px] = C_WHITE    # color final image pixel white and stop checking layers
                break
            else:                                 # this is a transparent pixel
                pass                              # leave final image pixel transparent temporarily and continue through layers

    # Generate image using final pixel array
    img = Image.new('RGB', (img_w, img_h))
    img.putdata(finalImagePixels)
    img.save('day08_output.png')
