import cv2
import os
import string
import random

# vidcap = cv2.VideoCapture(video_path)

try:
    # creating a folder named data
    if not os.path.exists('data'):
        os.makedirs('data')
# if not created then raise error
except OSError:
    print ('Error: Creating directory of data')

def rand_string(length):
    rand_str = ''.join(random.choice(
            string.ascii_lowercase
            + string.ascii_uppercase
            + string.digits)
        for i in range(length))
    return rand_str

def length_of_video(video_path):
    cap = cv2.VideoCapture(video_path)
    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    return length

def extracting_frames(video_path, save_path, skip_frames = 30):
    _, file_name = os.path.split(video_path)
    file_name_without_ext = os.path.splitext(file_name)[0]
    length = length_of_video(video_path)
    if length == 0:
        print('length is 0, exiting')
        return 0
    cap = cv2.VideoCapture(video_path)
    count = 0
    random_string = rand_string(5)

    ret,frame = cap.read()
    test_file_path = os.path.join(
        save_path,
        file_name_without_ext + \
        '{}_{}.jpg'.format(random_string, count))
    print(test_file_path)
    cv2.imwrite(test_file_path, frame)

    if os.path.isfile(test_file_path):
        print('save test frame success')
        count = 1
        while ret:
            ret,frame = cap.read()
            if ret and count % skip_frames == 0:
                cv2.imwrite(os.path.join(
                    save_path,
                    file_name_without_ext +
                    '{}_{}.jpg'.format(random_string, count)), frame)
                count +=1
                print(count)
            else:
                count+=1
    else:
        print('could not save test frame')
        return 0
    cap.release()


if __name__ == '__main__':
    save_path = 'data'
    video_path = './video/video.mov'
    extracting_frames(video_path, save_path, skip_frames = 30)