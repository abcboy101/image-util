# Converts an image from red = black/white, green = alpha to a b/w/a image
from PIL import Image
import sys

filename = sys.argv[1]
with Image.open(filename) as img:
    img = img.convert(mode="RGBA")
    for x in range(img.width):
        for y in range(img.height):
            colors = img.getpixel((x, y))
            img.putpixel((x, y), (colors[0], colors[0], colors[0], colors[1]))
    img.save(filename[:-4] + "_a" + filename[-4:])