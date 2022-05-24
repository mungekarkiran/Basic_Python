import numpy as np
import cv2
import cvzone
import pickle

# load video
cam = cv2.VideoCapture('data\carPark.mp4')

while 1:
    # check the frame count to reset the frame
    if cam.get(cv2.CAP_PROP_POS_FRAMES) == cam.get(cv2.CAP_PROP_FRAME_COUNT):
        cam.set(cv2.CAP_PROP_POS_FRAMES,0)

    # read frame from video
    success, img = cam.read()
    # show image 
    cv2.imshow('Image', img)

    
    if cv2.waitKey(32) & 0xFF == ord('q'):
        break