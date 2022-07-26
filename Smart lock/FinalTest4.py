import RPi.GPIO as GPIO
import time, datetime, os, cv2, pyrebase, smtplib, way2sms
import numpy as np
from email.mime.text import MIMEText
from gpiozero import Buzzer
from time import sleep

# adjust for where your switch is connected
buttonPin = 17
buzzer = Buzzer(18)
GPIO.setmode(GPIO.BCM)
GPIO.setup(buttonPin,GPIO.IN)

# Set relay pins as output
GPIO.setup(5, GPIO.OUT)
GPIO.setup(6, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)

# Turn all relays OFF
GPIO.output(5, GPIO.LOW)
GPIO.output(6, GPIO.LOW)
GPIO.output(13, GPIO.LOW)
GPIO.output(19, GPIO.LOW) 

# mail part
smtp_ssl_host = 'smtp.gmail.com'  # smtp.mail.yahoo.com
smtp_ssl_port = 465
# 'mungekarkiran05@gmail.com', 'shubhamneve2015@gmail.com','panpatilabhijeet66@gmail.com'
username = 'shubhamneve2015@gmail.com'
password = 'ShuBhaM2015'
sender = 'shubhamneve2015@gmail.com'
targets = ['panpatilabhijeet66@gmail.com',
           'mungekarkiran05@gmail.com',
           'shubhamneve2015@gmail.com']

msg = MIMEText('Hi, How Are You Today? Someone Is Trying To Open Your Door Now.')
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
smsCount = 0
vidcap = cv2.VideoCapture(0)
# change part Camera IP Addr. ---
address = "http://192.168.43.1:8080/video"
vidcap.open(address)
success,image = vidcap.read()
# code for image store
storage = firebase.storage()
mylist = []

if (vidcap.isOpened()== False):
    print("Error Opening Video Stream Or File.")

cv2.startWindowThread()

while True:
    # assuming the script to call is long enough we can ignore bouncing
    if (GPIO.input(buttonPin)):
        #
        # this is the script that will be called (as root)
        print("Door Is Open.")
        #time.sleep(.15)
        # mali send
        server = smtplib.SMTP_SSL(smtp_ssl_host, smtp_ssl_port)
        server.login(username, password)
        server.sendmail(sender, targets, msg.as_string())
        server.quit()
        
        # buzzer beep type 1 
        buzzer.on()
        sleep(1)
        buzzer.off()
        sleep(1)
        # buzzer beep type 2
        buzzer.beep()

        #  light on
        GPIO.output(5, GPIO.HIGH)
        GPIO.output(6, GPIO.HIGH)
        GPIO.output(13, GPIO.HIGH)
        GPIO.output(19, GPIO.HIGH)


        #  send sms 
        if (smsCount < 3):
            q=way2sms.Sms('7743939980','sshubhamm')
            # kiran '8108412112', abhijit '9359082883', shubham '8983930994' 
            q.send('7743939980','Hi, how are you today? Someone is trying to open your door now') 
            # receiver ph no.:0987654321, message=hello
            q.logout()

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
            print("Read A New Frame%d : " % count, success)
            #cv2.imwrite("img/frame%d.jpg" % count, image)
            cv2.imwrite("img/frame0.jpg" , imgSize)
            storage.child(date+"/UserName/"+localtime+"--%d.jpg" % count).put("img/frame0.jpg")
            count += 1
        else:
            print("Error Connecting To Camera. Issue #6")
    else:
        print("Door Is Close.")
        