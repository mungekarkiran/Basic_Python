import RPi.GPIO as GPIO
import time
import datetime
import os
import cv2
import time
import pyrebase
import numpy as np
import smtplib
from email.mime.text import MIMEText

#adjust for where your switch is connected
buttonPin = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(buttonPin,GPIO.IN)

#mail part
smtp_ssl_host = 'smtp.gmail.com'  # smtp.mail.yahoo.com
smtp_ssl_port = 465
#'mungekarkiran05@gmail.com', 'shubhamneve2015@gmail.com','panpatilabhijeet66@gmail.com'
username = 'shubhamneve2015@gmail.com'
password = 'ShuBhaM2015'
sender = 'shubhamneve2015@gmail.com'
targets = ['panpatilabhijeet66@gmail.com',
           'mungekarkiran05@gmail.com',
           'shubhamneve2015@gmail.com']

msg = MIMEText('Hi, how are you today? Someone is trying to open your door now')
msg['Subject'] = 'Alert'
msg['From'] = sender
msg['To'] = ', '.join(targets)

# change part FireBase ---
config = {
    "apiKey": "AIzaSyCRH0FfgsmBdeZ_7b9rOz6IJT_A0T6UNm4",
    "authDomain": "smartlock-3f1a0.firebaseapp.com",
    "databaseURL": "https://smartlock-3f1a0.firebaseio.com",
    "storageBucket": "smartlock-3f1a0.appspot.com"
    }

firebase = pyrebase.initialize_app(config)
count = 0
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

cv2.startWindowThread()

while True:
    #assuming the script to call is long enough we can ignore bouncing
    if (GPIO.input(buttonPin)):
        #
        #this is the script that will be called (as root)
        print("door is open")
        #time.sleep(.15)
        #mali send
        server = smtplib.SMTP_SSL(smtp_ssl_host, smtp_ssl_port)
        server.login(username, password)
        server.sendmail(sender, targets, msg.as_string())
        server.quit()

        #while (vidcap.isOpened()):
        if (vidcap.isOpened() == True):
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
            storage.child(date+"/UserName/"+localtime+"--%d.jpg" % count).put("img/frame0.jpg")
            count += 1
            #
            #if (GPIO.input(buttonPin)):
            #    print("door is open")
            # add else statement
	else:
            print("cam connection problem")
    else:
        print("door is close")

    
            
