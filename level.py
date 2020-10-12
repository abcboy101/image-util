# Attempts to find the parameters for a levels adjustment between two images.
from PIL import Image
import numpy as np
from scipy.optimize import curve_fit
import sys


def transform(x, a, b, c, d, e):
    """
    Function for the levels adjustment. Color values are in the range [0, 1].
    a: black point of input
    b: black point of output
    c: white point of input
    d: white point of output
    e: gamma adjustment
    """
    return np.add(np.multiply(d - b, np.power(np.abs(np.divide(np.subtract(x, a), c - a)), e)), b)


def level(image, transforms):
    """
    Levels each band of the image.
    """
    table = []
    for t in transforms:
        table += list(np.rint(np.multiply(transform(np.array(range(256)) / 255, *t), 255)))
    return image.point(table)


def match(tolevel, tomatch):
    """
    Curve fits each band to find the level parameters.
    """
    assert tolevel.size == tomatch.size  # check that dimensions match

    # Curve fit each band separately
    transforms = []
    for b, x, y in zip(tolevel.getbands(), tolevel.split(), tomatch.split()):
        xdata = np.divide(np.array(x).flatten(), 255)
        ydata = np.divide(np.array(y).flatten(), 255)
        popt, pcov = curve_fit(transform, xdata, ydata, p0=[0, 0, 1, 1, 1],
                               bounds=([0, 0, 0, 0, 0], [1, 1, 1, 1, np.inf]))
        t = tuple(list(np.multiply(popt, 255))[:4] + [popt[4]])
        print(b + ":", t)  # print the parameters for each band
        transforms.append(popt)

    return transforms


def main(tolevel, tomatch, filename="output.png", image=None, mode=None):
    """
    Main method.
    tolevel: the original image to be leveled
    tomatch: the leveled image to compare to
    filename: the output filename
    image: the input image to level, if different from tolevel
    mode: the output image mode
    """
    # Open each image
    tolevel = Image.open(tolevel)
    tomatch = Image.open(tomatch)
    if image is None:
        image = tolevel
    else:
        image = Image.open(image)

    # Handle images with different modes/palettes
    if mode is None:
        mode = max({i.mode for i in [tolevel, tomatch, image]}, key=lambda x: len(x))
    if mode in ["P", "PA"]:
        mode = {"P": "RGB", "PA": "RGBA"}[mode]

    tolevel = tolevel.convert(mode=mode)
    tomatch = tomatch.convert(mode=mode)
    image = image.convert(mode=mode)

    # Process images
    transforms = match(tolevel, tomatch)
    output = level(image, transforms)
    output.save(filename, mode=mode)
    print(filename + " saved")


if __name__ == "__main__":
    main(*sys.argv[1:])
