import cv2
import os
import time
#working

#path = 'D:\test'
#path1 = 'D:\test1'
vidcap = cv2.VideoCapture(0)
address = "http://192.168.1.6:8080/video"
vidcap.open(address)
success,image = vidcap.read()
count = 0
success = True
while (vidcap.isOpened()): #success:
  #time.sleep(3)
  success,image = vidcap.read()
  imgSize = cv2.resize(image, (600, 400)) # (w*h)
  print('Read a new frame: ', success)
  cv2.imwrite("img/frame%d.jpg" % count, imgSize) #image)
  #cv2.imwrite(os.path.join(path, "straight%d.jpg" % count), image)     # save frame as JPEG file
  #gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  #cv2.imwrite(os.path.join(path1, "straightbw%d.jpg" % count), gray)  # save frame as JPEG file
  count += 1
  
