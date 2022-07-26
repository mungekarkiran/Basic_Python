import RPi.GPIO as GPIO
import time
import datetime
import os
import cv2
import time
import pyrebase
import numpy as np

#adjust for where your switch is connected
buttonPin = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(buttonPin,GPIO.IN)

# change part FireBase ---
config = {
    "apiKey": "AIzaSyCRH0FfgsmBdeZ_7b9rOz6IJT_A0T6UNm4",
    "authDomain": "smartlock-3f1a0.firebaseapp.com",
    "databaseURL": "https://smartlock-3f1a0.firebaseio.com",
    "storageBucket": "smartlock-3f1a0.appspot.com"
    }

firebase = pyrebase.initialize_app(config)
count = 0
#localtime = time.asctime(time.localtime(time.time()))
vidcap = cv2.VideoCapture(0)
# change part Camera IP Addr. ---
address = "http://192.168.1.5:8080/video"
vidcap.open(address)
success,image = vidcap.read()
# code for image store
storage = firebase.storage()
mylist = []

if (vidcap.isOpened()== False):
    print("Error opening video stream or file")

# Read and display video frames until video is completed or 
# user quits by pressing ESC
cv2.startWindowThread()

while True:
    #assuming the script to call is long enough we can ignore bouncing
    if (GPIO.input(buttonPin)):
        #
        #this is the script that will be called (as root)
        #os.system("python /home/pi/start.py")
        print("door is open")
        #time.sleep(.15)
        while (vidcap.isOpened()):
            #
            today = datetime.date.today()
            mylist.append(today)
            date = str(mylist[0])
            #date = print (mylist[0])
            #date = str(mylist[0])
            localtime = time.asctime(time.localtime(time.time()))
            success,image = vidcap.read()
            imgSize = cv2.resize(image, (500, 400))
            print("Read a new frame%d : " % count, success)
            #cv2.imwrite("img/frame%d.jpg" % count, image)
            cv2.imwrite("img/frame0.jpg" , imgSize)
	    #storage.child("img/"+localtime+"--%d.jpg" % count).put("img/frame%d.jpg" % count)
	    #storage.child("img/"+localtime+"--%d.jpg" % count).put("img/frame0.jpg")
            storage.child(date+"/UserName/"+localtime+"--%d.jpg" % count).put("img/frame0.jpg")
            count += 1
            #
	    #count += 1
	    #
	    #End code.
