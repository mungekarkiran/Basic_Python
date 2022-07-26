#working
#https://stackoverflow.com/questions/47527868/importerror-cannot-import-name-opentype-on-new-installation/47529800
#https://github.com/thisbejim/Pyrebase
import cv2
import os
import time
import pyrebase
#from pyrebase import pyrebase
import numpy as np

# change part FireBase ---
config = {
  "apiKey": "AIzaSyD2Xu8wZP8ZlhjJsf2QAU6qbtKKRJKlXwo",
  "authDomain": "rs5perday.firebaseapp.com",
  "databaseURL": "https://rs5perday.firebaseio.com",
  "storageBucket": "rs5perday.appspot.com"
}

firebase = pyrebase.initialize_app(config)
count = 0
#localtime = time.asctime(time.localtime(time.time()))
vidcap = cv2.VideoCapture(0)
# change part Camera IP Addr. ---
address = "http://192.168.1.3:8080/video"
vidcap.open(address)
success,image = vidcap.read()

# code for image store
storage = firebase.storage()

while (vidcap.isOpened()):
    localtime = time.asctime(time.localtime(time.time()))
    success,image = vidcap.read()
    imgSize = cv2.resize(image, (600, 400))
    print("Read a new frame%d : " % count, success)
    #cv2.imwrite("img/frame%d.jpg" % count, image)
    cv2.imwrite("img/frame0.jpg" , imgSize) #image)
    #storage.child("img/"+localtime+"--%d.jpg" % count).put("img/frame%d.jpg" % count)
    storage.child("img/"+localtime+"--%d.jpg" % count).put("img/frame0.jpg")
    count += 1
