# console input: python lane_detect.py -i ""

import cv2
import numpy as np
import argparse
import shutil
# import matplotlib.pyplot as plt

# sets up console inputs
inp = argparse.ArgumentParser()
inp.add_argument("-i", "--input", type=str, required=True,
	help="path to input video")
#inp.add_argument("-o", "--output", type=str, required=True,
	#help="base path to input video")	
args = vars(inp.parse_args())


def do_canny(frame):
    # Converts frame to grayscale because we only need the luminance channel for detecting edges - less computationally expensive
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    # Applies a 5x5 gaussian blur with deviation of 0 to frame - not mandatory since Canny will do this for us
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    # Applies Canny edge detector with minVal of 50 and maxVal of 150
    canny = cv2.Canny(blur, 50, 150)
    return canny


# The video feed is read in as a VideoCapture object
cap = cv2.VideoCapture(args["input"])
while (cap.isOpened()):
    cv2.namedWindow("canny", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("canny", 1334, 750)
    
    # ret = a boolean return value from getting the frame, frame = the current frame being projected in the video
    ret, frame = cap.read()
    canny = do_canny(frame)
    cv2.imshow("canny", canny)
    # plt.imshow(frame)
    # plt.show()
    
    # Frames are read by intervals of 10 milliseconds. The programs breaks out of the while loop when the user presses the 'q' key
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break
# The following frees up resources and closes all windows
cap.release()
cv2.destroyAllWindows()

print("\n[INFO] Finished!\n")
