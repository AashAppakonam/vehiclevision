#console input: python yolo_imageGlob.py -y yolo-coco -c _ -t _

# import the necessary packages
import numpy as np
import argparse
import time
import cv2
import os
import glob
import random

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
#ap.add_argument("-i", "--image", required=True,
	#help="path to input image")
ap.add_argument("-y", "--yolo", required=True,
	help="base path to YOLO directory")
ap.add_argument("-c", "--confidence", type=float, default=0.55,
	help="minimum probability to filter weak detections")
ap.add_argument("-t", "--threshold", type=float, default=0.3,
	help="threshold when applyong non-maxima suppression")
args = vars(ap.parse_args())

# load the COCO class labels our YOLO model was trained on
labelsPath = os.path.sep.join([args["yolo"], "coco.names"])
LABELS = open(labelsPath).read().strip().split("\n")

# initialize a list of colors to represent each possible class label
np.random.seed(42)
COLORS = np.random.randint(0, 255, size=(len(LABELS), 3),
	dtype="uint8")

# derive the paths to the YOLO weights and model configuration
weightsPath = os.path.sep.join([args["yolo"], "yolov3.weights"])
configPath = os.path.sep.join([args["yolo"], "yolov3.cfg"])

# load our YOLO object detector trained on COCO dataset (80 classes)
print("\n[INFO] loading YOLO from disk...")
net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)

# determine only the *output* layer names that we need from YOLO
ln = net.getLayerNames()
ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]


# load our input image and grab its spatial dimensions
#image = cv2.imread(args["image"])
images_path = glob.glob(r"C:\Users\Aashish\Documents\My Received Files\School\12th Grade\Senior Project\Projects\ObjectDetection\yolo-object-detection\final_project\datasets\AZ_drive\images\\*.jpg")
#random.shuffle(images_path)

for img_path in images_path:
	# Loading image
	image = cv2.imread(img_path)
	
	# preprocessing image data with resizing algorithm
	# height, width, number of channels in image before potential resizing
	height, width, channels = image.shape
	print("\n[INFO] Image Dimensions \n", "Height: %s   Width: %s   Channels: %s" % (height, width, channels))
	
	if (height>=1500) and (width>=1800):
	    #scaling down
	    image = cv2.resize(image, None, fx=0.3, fy=0.3) 
	    print("Down-sized Image for Analysis")
	    # dimension values after resizing 
	    height, width, channels = image.shape
	elif (height<=400) and (width<=400): 
	    #scaling down
	    image = cv2.resize(image, None, fx=3, fy=3) 
	    print("Up-sized Image for Analysis")
	    # dimension values after resizing 
	    height, width, channels = image.shape
	else:
	    print("No resizing needed")

	(H, W) = height, width 


	# construct a blob from the input image and then perform a forward
	# pass of the YOLO object detector, giving us our bounding boxes and
	# associated probabilities
	blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416),
		swapRB=True, crop=False)
	net.setInput(blob)
	start = time.time()
	layerOutputs = net.forward(ln)
	end = time.time()

	# show timing information on YOLO
	print("[INFO] YOLO took {:.3f} seconds to processs and analyze".format(end - start))

	# initialize our lists of detected bounding boxes, confidences, and
	# class IDs, respectively
	boxes = []
	confidences = []
	classIDs = []

	# loop over each of the layer outputs
	for output in layerOutputs:
		# loop over each of the detections
		for detection in output:
			# extract the class ID and confidence (i.e., probability) of
			# the current object detection
			scores = detection[5:]
			classID = np.argmax(scores)
			confidence = scores[classID]

			# filter out weak predictions by ensuring the detected
			# probability is greater than the minimum probability
			if confidence > args["confidence"]:
				# scale the bounding box coordinates back relative to the
				# size of the image, keeping in mind that YOLO actually
				# returns the center (x, y)-coordinates of the bounding
				# box followed by the boxes' width and height
				box = detection[0:4] * np.array([W, H, W, H])
				(centerX, centerY, width, height) = box.astype("int")

				# use the center (x, y)-coordinates to derive the top and
				# and left corner of the bounding box
				x = int(centerX - (width / 2))
				y = int(centerY - (height / 2))

				# update our list of bounding box coordinates, confidences,
				# and class IDs
				boxes.append([x, y, int(width), int(height)])
				confidences.append(float(confidence))
				classIDs.append(classID)

	# apply non-maxima suppression to suppress weak, overlapping bounding
	# boxes
	idxs = cv2.dnn.NMSBoxes(boxes, confidences, args["confidence"], args["threshold"])
	#print(idxs)

	objects = []
	# ensure at least one detection exists
	if len(idxs) > 0:
		# loop over the indexes we are keeping
		for i in idxs.flatten():
			# extract the bounding box coordinates
			(x, y) = (boxes[i][0], boxes[i][1])
			(w, h) = (boxes[i][2], boxes[i][3])

			# draw a bounding box rectangle and label on the image
			color = [int(c) for c in COLORS[classIDs[i]]]
			cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
			text = "{}: {:.4f}".format(LABELS[classIDs[i]], confidences[i])
			conout = LABELS[classIDs[i]], str("{:.3f}".format(confidences[i]))
			objects.append(conout)
			cv2.putText(image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

	print("\n",  len(objects), " Object(s) Detected w/ confidences: ", objects)

	# show the output image
	cv2.imshow("Image", image)
	cv2.waitKey(0)

#calling object detection scripts for custom objects

cv2.destroyAllWindows()
print("\n[INFO] Finished")
