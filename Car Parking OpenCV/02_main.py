import numpy as np
import cv2
import cvzone
import pickle

# load video
cam = cv2.VideoCapture('data\carPark.mp4')

# width = 156 - 50
# height = 240 - 193
width, height = 106, 47

# load the position list
with open('CarParkPos.pkl', 'rb') as f:
    postList = pickle.load(f)

# functions

def checkParkingSpace():
    # draw rectrangle
    # cv2.rectangle(img, (50,193), (156,240), (255,0,255), 2)
    for pos in postList:
        cv2.rectangle(img, pos, (pos[0] + width , pos[1] + height), (255,0,255), 2)

        # crop the position one by one
        x, y = pos
        imgCrop = img[y:y+height, x:x+width]
        cv2.imshow(str(x*y), imgCrop)


while 1:
    # check the frame count to reset the frame
    if cam.get(cv2.CAP_PROP_POS_FRAMES) == cam.get(cv2.CAP_PROP_FRAME_COUNT):
        cam.set(cv2.CAP_PROP_POS_FRAMES,0)

    # read frame from video
    success, img = cam.read()
    
    checkParkingSpace()
    
    # show image 
    cv2.imshow('Image', img)


    
    if cv2.waitKey(32) & 0xFF == ord('q'):
        break