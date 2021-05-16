from PIL import Image, ImageChops

im1 = Image.open('./data/videoqZg6k_0.jpg')
im2 = Image.open('./data/videoqZg6k_120.jpg')

data1 = list(im1.getdata())
data2 = list(im2.getdata())
if data1 == data2:
    print("Identical")
else:
    print("Different")
    diff = ImageChops.difference(im1, im2)
    print(diff.getbbox())