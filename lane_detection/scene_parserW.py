# console input: python lane_detect.py -i ""

import cv2
import imutils
import numpy as np
import argparse
import datetime
import tkinter as tk
from tkinter import messagebox as mb

# import matplotlib.pyplot as plt

# sets up console inputs
inp = argparse.ArgumentParser()
inp.add_argument("-i", "--input", type=str, required=True,
	help="path to input video")
inp.add_argument("-o", "--output", type=str, required=True,
	help="path to output video")
inp.add_argument("-f", "--fps", type=int, default=30,
	help="frame rate for output video")
inp.add_argument("-c", "--codec", type=str, default="MJPG",
	help="codec of output video")
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
writer = None

# try to determine the total number of frames in the video file
try:
	prop = cv2.cv.CV_CAP_PROP_FRAME_COUNT if imutils.is_cv2() \
		else cv2.CAP_PROP_FRAME_COUNT
	total = int(cap.get(prop))
	print("\n[INFO] {} total frames in video\n".format(total))
	currentDT1 = datetime.datetime.now()
	print("[INFO] Start:", currentDT1.strftime("%I:%M:%S %p"), "\n")

# an error occurred while trying to determine the total
# number of frames in the video file
except:
	print("[INFO] could not determine # of frames in video")
	print("[INFO] no approx. completion time can be provided")
	total = -1
	currentDT1 = datetime.datetime.now()
	print("[INFO] Start:", currentDT1.strftime("%I:%M:%S %p"), "\n")


while True:
	# grabbed = a boolean return value from getting the frame, frame = the current frame being projected in the video
	(grabbed, frame) = cap.read()

	# if the frame was not grabbed, then we have reached the end of the stream
	if not grabbed:
		break

	canny = do_canny(frame)
	#cv2.imshow("canny", canny)
	# plt.imshow(frame)
	# plt.show()
	
	if writer is None:
		# initialize our video writer
		fourcc = cv2.VideoWriter_fourcc(*args["codec"])
		writer = cv2.VideoWriter(args["output"], fourcc, args["fps"],
			(canny.shape[1], canny.shape[0]), True)

	writer.write(canny)
    
# The following frees up resources and closes all windows
writer.release()
cap.release()

# display info to console
currentDT2 = datetime.datetime.now()
print("\n[INFO] Finished:", currentDT2.strftime("%I:%M:%S %p"), "\n")
mb.showinfo("YOLO Video Output", "Finished Analyzing")

