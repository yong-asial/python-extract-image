from PIL import Image, ImageChops
import math, operator
import cv2
from functools import reduce
from datetime import datetime

def crop_image(image, p = 0.2):
    x1 = image.width * p
    y1 = image.height * p
    x2 = image.width * (1 - p)
    y2 = image.height * (1 - p)
    crop_rectangle = (x1, y1, x2, y2)
    return image.crop(crop_rectangle)

def calculate_similarity_score(img1,img2):
    try:
        # Convert to RGB
        img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
        img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)

        # Initialize ORB detector
        orb = cv2.ORB_create()
        kp1, des1 = orb.detectAndCompute(img1, None)
        kp2, des2 = orb.detectAndCompute(img2, None)

        # Extract and calculate feature points
        bf = cv2.BFMatcher(cv2.NORM_HAMMING)

        # knnFilter results
        matches = bf.knnMatch(des1, trainDescriptors=des2, k=2)

        # View the maximum number of matching points
        good = [m for (m, n) in matches if m.distance < 0.75 * n.distance]

        if len(matches) == 0:
            return 0
        score = len(good) / len(matches)
        # print("The similarity of the two pictures is: %s"% score)
        return score
    except:
        print('Unable to calculate the similarity of two pictures')
        return 0

def rmsdiff(im1, im2):
    "Calculate the root-mean-square difference between two images"

    h = ImageChops.difference(im1, im2).histogram()

    # calculate rms
    return math.sqrt(reduce(operator.add,
        map(lambda h, i: h*(i**2), h, range(256))
    ) / (float(im1.size[0]) * im1.size[1]))

def get_time():
    now = datetime.now()
    return now

def get_diff(date_1, date_2):
    time_delta = (date_2 - date_1)
    total_seconds = time_delta.total_seconds()
    return total_seconds

file1 = 'im1.png'
file2 = 'im2.png'

date_1 = get_time()
im1 = Image.open(file1)
im2 = Image.open(file2)
print(rmsdiff(im1, im1)) # 0
print(rmsdiff(im1, im2)) # 70.28
# print("time:" + str(get_diff(date_1, get_time())))
# diff = ImageChops.difference(im1, im2)
# diff.show()

# same image -> 0
# the higher, the diff

# RESIZE_HEIGHT = 360
# height = im1.shape[0]
# RESIZE_SCALE = float(height)/RESIZE_HEIGHT
# im1 = cv2.resize(im1, None, fx=1.0/RESIZE_SCALE, fy=1.0/RESIZE_SCALE,
#                                 interpolation=cv2.INTER_LINEAR)

date_1 = get_time()
im1 = cv2.imread(file1)
im2 = cv2.imread(file2)
print(calculate_similarity_score(im1, im1)) # 0.992
print(calculate_similarity_score(im1, im2)) # 0.364
# print("time:" + str(get_diff(date_1, get_time())))
# same image -> 1
# the lower, the diff
