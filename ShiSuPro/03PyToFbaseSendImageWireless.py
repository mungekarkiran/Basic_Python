import cv2, os, time, pyrebase
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
# code for image store
storage = firebase.storage()

for x in range(10):
	vidcap = cv2.VideoCapture(0)
	# change part Camera IP Addr. ---
	address = "http://192.168.1.5:8080/video"
	vidcap.open(address)

	success,image = vidcap.read()
	imgSize = cv2.resize(image, (600, 400))
	print("Read a new frame%d : " % x, success)
	cv2.imwrite("img/frame0.jpg" , imgSize) 
	storage.child("img/--%d.jpg" % count).put("img/frame0.jpg")
	storage.child("ImgOut/MyHome.jpg").put("img/frame0.jpg")
	count += 1
	time.sleep(5)
