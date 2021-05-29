import pytesseract
import os
from PIL import Image, ImageChops
import math, operator
from functools import reduce

image_directory = 'image'

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

def remove_file(file):
  try:
    os.remove(file)
  except OSError as e:  ## if failed, report it back to the user ##
    print ("Error: %s - %s." % (e.filename, e.strerror))

previous_image = ''
previous_image_file_path = ''
THRESHOLD = 10

print('start cleanup process - 2')
for image_filename in sorted(os.listdir(image_directory)):
  if not (image_filename.endswith(".jpg") or image_filename.endswith(".png")):
    continue

  file_path = os.path.join(image_directory, image_filename)
  current_image = crop_image(Image.open(file_path))

  if previous_image == '':
    previous_image = current_image
    previous_image_file_path = file_path # logging purpose
    continue

  diff = rmsdiff(previous_image, current_image)

  # The image is very similar
  if diff < THRESHOLD:
    # delete image
    print('delete ' + file_path)
    remove_file(file_path)
    continue

  # The image is different
  previous_image = current_image
  previous_image_file_path = file_path

print('finish cleanup process')