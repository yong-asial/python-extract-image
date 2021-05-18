import cv2
import os

video_directory = 'video'
image_directory = 'image'
frameRate = 20 #//it will capture image in each x second

try:
  # creating a folder named data
  if not os.path.exists(image_directory):
      os.makedirs(image_directory)
# if not created then raise error
except OSError:
  print ('Error: Creating directory of data')

def length_of_video(vidcap):
  length = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
  return length

def getFrame(vidcap, video_filename, sec, count):
  vidcap.set(cv2.CAP_PROP_POS_MSEC, sec*1000)
  hasFrames,image = vidcap.read()
  filename = os.path.splitext(video_filename)[0]
  if hasFrames:
    cv2.imwrite(image_directory + "/" + filename + "_" + "{:06d}".format(count) + ".jpg", image)
  return hasFrames

for video_filename in os.listdir(video_directory):
  if not (video_filename.endswith(".mov") or video_filename.endswith(".mp4")):
    continue
  sec = 0
  count = 1
  vidcap = cv2.VideoCapture(os.path.join(video_directory, video_filename))
  success = getFrame(vidcap, video_filename, sec, count)
  print(video_filename + '- start')
  while success:
    print(count)
    count = count + 1
    sec = sec + frameRate
    sec = round(sec, 2)
    success = getFrame(vidcap, video_filename, sec, count)
  print(video_filename + '- complete')
