# type NULL >> 01PyToFbaseText.py
import time, pyrebase, os, datetime, pprint 

#Firebase Configuration
config = {
  "apiKey": "AIzaSyD2Xu8wZP8ZlhjJsf2QAU6qbtKKRJKlXwo",
  "authDomain": "rs5perday.firebaseapp.com",
  "databaseURL": "https://rs5perday.firebaseio.com",
  "storageBucket": "rs5perday.appspot.com"
}
firebase = pyrebase.initialize_app(config)

#Firebase Database Intialization
db = firebase.database()

while 1:
	x = datetime.datetime.now()
	data = {"Date": str(x), "Time": x.strftime("%I-%M-%S"), "Day": str(x.strftime("%A"))}
	db.child("Today").set(data)
	print(data)
	time.sleep(.5)