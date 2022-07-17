import cv2, os, random,sqlite3
import numpy as np
from deep_translator import GoogleTranslator
import keyboard
import speech_recognition as sr



r = sr.Recognizer()
m = sr.Microphone(0)
print('----')
while True:

	try:
		with m as source:

			r.adjust_for_ambient_noise(source)
			audio = r.listen(source)
			language = "en"
			if keyboard.read_key() == "p":
				print("You pressed p")
				language = "hi"

			value = r.recognize_google(audio, language=language)
			print(value)
			translated = GoogleTranslator(source='auto', target='en').translate(value)
			# print(translated)


		str1=translated.upper()
		cc=[]


		for j in str1:
			conn = sqlite3.connect("gesture_db.db")
			if j == ' ':
				cc.append(' ')
			else:
				cmd = "SELECT g_id FROM gesture WHERE g_name='{}'".format(j)

				cursor = conn.execute(cmd)

				for row in cursor:
					cc.append(row[0])




		col_img2 = None
		blk = np.zeros((50, 50, 3), dtype=np.uint8)
		for k in cc:
			if k ==' ':
				col_img2 = np.hstack((col_img2,blk))

			else:

				im1 = "gestures/%s/%d.jpg" % (k, random.randint(1, 1200))
				im2 = cv2.imread(im1)
				if np.any(im2 == None):
					im2 = np.zeros((image_y, image_x), dtype=np.uint8)
				if np.any(col_img2 == None):
					col_img2 = im2
				else:
					col_img2 = np.hstack((col_img2, im2))


		#cv2.imshow("letter", col_img2)

		x1, y1 ,z1= col_img2.shape

		blackboard2 = np.zeros((100, y1, 3), dtype=np.uint8)
		cv2.putText(blackboard2, " "+str1, (10, 50), cv2.FONT_HERSHEY_TRIPLEX, 1.5, (0, 255,0))

		res2 = np.vstack((blackboard2,col_img2))
		cv2.imshow("Txt to Sign", res2)

		if cv2.waitKey(1) == ord('q'):
			break

	except:
		print('Speak Again')


