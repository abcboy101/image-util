# Sets fully transparent pixels to black
from PIL import Image
import sys

filename = sys.argv[1]
with Image.open(filename) as img:
    img = img.convert(mode="RGBA")
    for x in range(img.width):
        for y in range(img.height):
            colors = img.getpixel((x, y))
            if colors[3] == 0:
                img.putpixel((x, y), (0, 0, 0, 0))
    img.save(filename)