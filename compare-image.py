from PIL import Image, ImageChops
import math, operator
from functools import reduce

def crop_image(image, p = 0.2):
    x1 = image.width * p
    y1 = image.height * p
    x2 = image.width * (1 - p)
    y2 = image.height * (1 - p)
    crop_rectangle = (x1, y1, x2, y2)
    return image.crop(crop_rectangle)

def rmsdiff(im1, im2):
    "Calculate the root-mean-square difference between two images"

    h = ImageChops.difference(im1, im2).histogram()

    # calculate rms
    return math.sqrt(reduce(operator.add,
        map(lambda h, i: h*(i**2), h, range(256))
    ) / (float(im1.size[0]) * im1.size[1]))

im1 = Image.open('image/video2_000029.jpg')
im2 = Image.open('image/video2_000030.jpg')

# crop
im1 = crop_image(im1)
im2 = crop_image(im2)

print(rmsdiff(im1, im2))

diff = ImageChops.difference(im1, im2)
diff.show()