import cv2
import os
import time

cap = cv2.VideoCapture(0)
address = "http://192.168.1.6:8080/video"#"http://192.168.1.2:8080/video" # Your address might be different

cap.open(address)

if (cap.isOpened()== False):
    print("Error opening video stream or file")

# Read and display video frames until video is completed or 
# user quits by pressing ESC
cv2.startWindowThread()
while(cap.isOpened()):
# Capture frame-by-frame
    ret, frame = cap.read()
    if ret == True:
        # Display the resulting frame
        #cv2.namedWindow('Frame', cv2.WINDOW_AUTOSIZE)
        cv2.namedWindow('Frame',cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Frame', 200,200)#('abc', width, height)
        cv2.imshow('Frame',frame)
        time.sleep(1)
        if (cv2.waitKey(1) & 0xFF == 27):
            break
    else:
        break
    
cap.release()
cv2.destroyAllWindows()
