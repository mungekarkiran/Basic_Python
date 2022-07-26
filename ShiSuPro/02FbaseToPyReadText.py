# type NULL >> 02FbaseToPyReadText.py
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

# While loop to run until user kills program
while 1:
	# Get value of LED 
	all_users = db.child("Cam").get()
	for user in all_users.each():
		# name = user.key()
		# value = user.val()
		# each = all_users.each()
		# print(user.key()+" : "+ user.val())

		# test 1
		# the string is not oneP it is "oneP" therefor == '"oneP"'
		# Check value of child(which is 'state')
		if(user.key() == "PicStatus"):
			if(user.val() == '"oneP"'):
				print("Now PicStatus is "+ user.val())
				for x in range(2):
					print(x)
					time.sleep(1)
				db.child("Cam").child(user.key()).set("noP")
			elif(user.val() == '"tenP"'):
				print("Now PicStatus is "+ user.val())
				for x in range(10):
					print(x)
					time.sleep(1)
				db.child("Cam").child(user.key()).set("noP")
			elif(user.val() == '"nP"'):
				print("Now PicStatus is "+ user.val())
				for x in range(100):
					print(x)
					time.sleep(.5)
				db.child("Cam").child(user.key()).set("noP")
			else:
				print("else is "+ user.val())
		else:
			print("user.key() : "+ user.key())

		# test 2 
		# the string is not oneP it is "oneP" therefor == '"oneP"'
		# if(str(user.val()) == '"oneP"'):
		# 	print("Now PicStatus is "+ user.val())
		# 	for x in range(2):
		# 		print(x)
		# 		time.sleep(1)
		# elif(str(user.val()) == '"tenP"'):
		# 	print("Now PicStatus is "+ user.val())
		# 	for x in range(10):
		# 		print(x)
		# 		time.sleep(1)
		# elif(str(user.val()) == '"nP"'):
		# 	print("Now PicStatus is "+ user.val())
		# 	for x in range(100):
		# 		print(x)
		# 		time.sleep(.5)
		# else:
		# 	print("else is "+ user.val())