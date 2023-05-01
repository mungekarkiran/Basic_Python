# import cv2

# # capture live video strime
# URL = "http://192.168.0.115:8080/video"
# capture = cv2.VideoCapture(0)

# while 1:

#     # read video strime
#     _, frame = capture.read()

#     # show the video strime
#     cv2.imshow('LiveStrimeScreen', frame)


#     # to stop the strime
#     if cv2.waitKey(1) == ord("q"):
#         break

# # close the resorces
# capture.release()
# cv2.destroyAllWindows()


# import cv2

# # Callback function to handle mouse events
# def on_click(event, x, y, flags, param):
#     if event == cv2.EVENT_LBUTTONDOWN:
#         print("Button clicked at ({}, {})".format(x, y))
#         cv2.putText(img, "Button clicked", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

# # Create a black image
# img = cv2.imread("blank_image.jpeg")

# # Create a window and set the mouse callback
# cv2.namedWindow("image")
# cv2.setMouseCallback("image", on_click)

# # Add a button to the window
# cv2.createButton("Button", lambda x: print("Button pressed"), None, cv2.QT_PUSH_BUTTON)

# while True:
#     # Display the image and wait for a key press
#     cv2.imshow("image", img)
#     key = cv2.waitKey(1)

#     # Exit if the 'q' key is pressed
#     if key == ord('q'):
#         break

# # Clean up
# cv2.destroyAllWindows()



# import cv2

# # define a callback function to handle button clicks
# def on_button_click(state):
#     if state == 0:
#         print("Button clicked!")

# # create a window
# cv2.namedWindow("My Window")

# # create a button and add it to the window
# # cv2.createButton("My Button", on_button_click, None, cv2.QT_PUSH_BUTTON)
# cv2.createButton("My Button", on_button_click, None, cv2.QT_PUSH_BUTTON, 1)

# # show the window and wait for a key event
# cv2.imshow("My Window", cv2.imread("blank_image.jpeg"))
# cv2.waitKey(0)

# # destroy the window
# cv2.destroyWindow("My Window")




# #!/usr/bin/env python

# from __future__ import print_function
# import cv2
# print(cv2.__version__)

# class Button(object):

#     def __init__(self, text, x, y, width, height, command=None):
#         self.text = text
#         self.x = x
#         self.y = y
#         self.width = width
#         self.height = height
        
#         self.left = x
#         self.top  = y
#         self.right  = x + width - 1 
#         self.bottom = y + height - 1
        
#         self.hover = False
#         self.clicked = False
#         self.command = command
        
#     def handle_event(self, event, x, y, flags, param):
#         self.hover = (self.left <= x <= self.right and \
#             self.top <= y <= self.bottom)
            
#         if self.hover and flags == 1:
#             self.clicked = False
#             print(event, x, y, flags, param)
            
#             if self.command:
#                 self.command()
        
#     def draw(self, frame):
#         if not self.hover:
#             cv2.putText(frame, "???", (40,40), FONT, 3 , (0,0,255), 2)
#             cv2.circle(frame, (20,20), 10 , (0,0,255), -1)
#         else:
#             cv2.putText(frame, "REC", (40,40), FONT, 3 , (0,255,0), 2)
#             cv2.circle(frame, (20,20), 10 , (0,255,0), -1)
        
# # ---------------------------------------------------------------------

# # keys 
# KEY_ESC = 27

# # font
# FONT = cv2.FONT_HERSHEY_PLAIN

# # ---------------------------------------------------------------------

# # states
# running = True 

# # ---------------------------------------------------------------------

# # create button instance
# button = Button('QUIT', 0, 0, 100, 30)

# # ---------------------------------------------------------------------

# # create VideoCapture
# vcap = cv2.VideoCapture(0) # 0=camera
 
# # check if video capturing has been initialized already
# if not vcap.isOpened(): 
#     print("ERROR INITIALIZING VIDEO CAPTURE")
#     exit()
# else:
#     print("OK INITIALIZING VIDEO CAPTURE")
 
#     # get vcap property 
#     width = int(vcap.get(cv2.CAP_PROP_FRAME_WIDTH))
#     height = int(vcap.get(cv2.CAP_PROP_FRAME_HEIGHT))
#     #fps = float(vcap.get(cv2.CAP_PROP_FPS))
#     fps = 15.0 # use different value to get slowmotion or fastmotion effect
    
#     print('VCAP width :', width)
#     print('VCAP height:', height)
#     print('VCAP fps   :', fps)
 
# while running:
#     # grab, decode and return the next video frame (and "return" status)
#     ret, frame = vcap.read()

#     if not ret:
#         running = False
#     else:
#         # add REC to frame
#         #cv2.putText(frame, "REC", (40,40), FONT, 3 , (0,0,255), 2)
#         #cv2.circle(frame, (20,20), 10 , (0,0,255), -1)

#         # add instruction to frame
#         cv2.putText(frame,"ESC - QUIT",(width - 200,20), FONT, 1 ,(255,255,255))

#         # add button to frame
#         button.draw(frame)
        
#         # displays frame
#         cv2.imshow('x', frame)         
#         # assign mouse click to method in button instance
#         cv2.setMouseCallback("x", button.handle_event)

     
#         # get key (get only lower 8-bits to work with chars)
#         key = cv2.waitKey(1) & 0xFF

#         if key == KEY_ESC:
#             print("EXIT")
#             running = False
     
# # release everything 
# vcap.release()
# cv2.destroyAllWindows()

# import re

# text = "  mh.04.ab 1007   "
# print(text.upper().replace(' ', ''))

# text = text.upper().replace(' ', '')
# print(re.sub(r'[^\w\s]', '', text))



# import sqlite3

# # Connecting to a database
# conn = sqlite3.connect('mydb.db')

# # Creating a cursor object
# cursor = conn.cursor()


# # Creating a table
# cursor.execute('''CREATE TABLE IF NOT EXISTS students (id INTEGER PRIMARY KEY, name TEXT, age INTEGER, gender TEXT)''')
# # Committing the changes
# conn.commit()

# try:
#     # Inserting data into the table
#     cursor.execute("INSERT INTO students (id, name, age, gender) VALUES (1, 'John', 22, 'Male')")
#     cursor.execute("INSERT INTO students (id, name, age, gender) VALUES (2, 'Sam', 23, 'Male')")
#     # Committing the changes
#     conn.commit()
# except:
#     pass

# # Retrieving data from the table
# cursor.execute("SELECT * FROM students")
# # Fetching the data
# data = cursor.fetchall()
# print(data)
# for row in data:
#     print(row)


# # Retrieving data from the table
# cursor.execute("SELECT * FROM students where name='Sam'")
# # Fetching the data
# data = cursor.fetchall()
# print(data)
# for row in data:
#     print(row)


# # Closing the connection
# conn.close()



# import datetime

# now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# # print the formatted value
# print("Formatted date:", now, type(now))



# print(0%2, 1%2, 2%2, 3%2, 4%2)

# text = "MH04AJ1212"
# print(text[:2], text[:2].isalpha())
# print(text[2:4], text[2:4].isnumeric())
# print(text[4:6], text[4:6].isalpha())
# print(text[6:], text[6:].isnumeric())