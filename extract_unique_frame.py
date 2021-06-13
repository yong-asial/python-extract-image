import os
import sys
import cv2
from datetime import datetime

## CHANGE PARAMETERS HERE
VIDEO_FILENAME = 'video1.mov'
SAVE_DIR = 'captured'
SAVE_FILENAME = 'frame'
THRESHOLD = 0.3   ## please experiment with this value, i.e smaller value:less sensitive
RESIZE_HEIGHT = 360
WIN_NAME = 'VIDEO DISPLAY'
##

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
        print("The similarity of the two pictures is: %s"% score)
        return score
    except:
        print('Unable to calculate the similarity of two pictures')
        return 0

def save_image(id, img):
    filename = SAVE_FILENAME + '-' + str(id) + '.png'
    save_path = os.path.join(SAVE_DIR, filename)
    cv2.imwrite(save_path, img)
    print("Frame saved!")

def print_time():
    now = datetime.now()
    print("now =", now)

def main():
    print_time()

    # Variable to store each unique image
    base_frame = None
    SAVED_ID  = 0

    # Create folder to store extracted frames
    if not os.path.exists(SAVE_DIR):
        os.mkdir(SAVE_DIR)

    # Open video and read frame
    CAP = cv2.VideoCapture(VIDEO_FILENAME)
    if not CAP.isOpened():
        print('Unable to open the file.')
        sys.exit()
    ret, frame = CAP.read()

    if ret:
        height = frame.shape[0]
        RESIZE_SCALE = float(height)/RESIZE_HEIGHT
        img_size = frame.shape[0:2]
        save_image(SAVED_ID, frame)
    else:
        print('Unable to read frame')
        sys.exit()

    # Loop over video
    while True:
        # Read each frame
        ret, frame = CAP.read()
        small_frame = None
        # Resize to smaller frame for faster similarity calculation
        try:
            small_frame = cv2.resize(frame, None, fx=1.0/RESIZE_SCALE, fy=1.0/RESIZE_SCALE,
                                interpolation=cv2.INTER_LINEAR)
        except:
            print('Sth wrong')
            break
        # Assign the first frame as unique frame
        if base_frame is None:
            base_frame = small_frame
        # Based on the similirity score
        similarity_score = calculate_similarity_score(base_frame, small_frame)
        if similarity_score < THRESHOLD:
            SAVED_ID += 1
            save_image(SAVED_ID, frame)
            base_frame = small_frame

        # Display the video
        cv2.imshow(WIN_NAME, small_frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or key==27: #ESC
            break

    cv2.destroyAllWindows()
    CAP.release()
    print('Program Exited')
    print_time()

if __name__ == '__main__':
    main()
