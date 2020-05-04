# console input: python vid_resize.py -i "path\to\input.mp4" -o "path\to\outputfolder" -hi 720 -wi 1280

from moviepy.editor import VideoFileClip
import os
import glob
import argparse 
import shutil


ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", type=str, required=True,
	help="path to input video")
ap.add_argument("-o", "--output", type=str, required=True,
	help="path to output video")
ap.add_argument("-hi", "--height", type=int, required=True,
	help="path to output video")
ap.add_argument("-wi", "--width", type=int, required=True,
	help="path to output video")
args = vars(ap.parse_args())

print("\n[INFO] Loading...\n")

clip = VideoFileClip(args["input"])
clip_resized = clip.resize((args["width"], args["height"])) #(w,h)
clip_resized.write_videofile("movie_resized.mp4", audio=False)
shutil.move("movie_resized.mp4", args["output"])

print("\n[INFO] Finished!")
