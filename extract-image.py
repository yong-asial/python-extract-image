import os
import cv2
import os

video_directory = 'video'
image_directory = 'data'
frameRate = 0.5 #//it will capture image in each 0.5 second

try:
  # creating a folder named data
  if not os.path.exists(image_directory):
      os.makedirs(image_directory)
# if not created then raise error
except OSError:
  print ('Error: Creating directory of data')

def getFrame(vidcap, video_filename, sec, count):
  vidcap.set(cv2.CAP_PROP_POS_MSEC, sec*1000)
  hasFrames,image = vidcap.read()
  filename = os.path.splitext(video_filename)[0]
  if hasFrames:
    cv2.imwrite(image_directory + "/" + filename + "_" + str(count) + ".jpg", image)
  return hasFrames

for video_filename in os.listdir(video_directory):
  sec = 0
  count = 1
  vidcap = cv2.VideoCapture(os.path.join(video_directory, video_filename))
  success = getFrame(vidcap, video_filename, sec, count)
  while success:
    count = count + 1
    sec = sec + frameRate
    sec = round(sec, 2)
    success = getFrame(vidcap, video_filename, sec, count)
