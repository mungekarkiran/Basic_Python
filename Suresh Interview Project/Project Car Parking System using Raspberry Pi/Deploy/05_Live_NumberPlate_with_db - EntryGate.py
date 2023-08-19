import numpy as np
import cv2
import easyocr
import imutils
import time
import sqlite3
import datetime
import re

# FUNCTIONS
def preprocess_number_plate(text:str) -> str:
    """
    This function is used to do pre-processing on the number plate.
    """
    if len(text)>8:
        text = text.upper().replace(' ', '')
        text = re.sub(r'[^\w\s]', '', text)
        
        # Strong validation 
        # if text[:2].isalpha() and text[2:4].isnumeric() and text[4:6].isalpha() and text[6:].isnumeric():
        #     return text
        return text
    else:
        return None

def car_registry(text:str) -> str:
    """
    This function is used to insert in and out car records.
    """
    # Connecting to a database
    conn = sqlite3.connect('car_parking_db.db')
    # Creating a cursor object
    cursor = conn.cursor()

    # Creating a table
    cursor.execute("""CREATE TABLE IF NOT EXISTS parking (id INTEGER PRIMARY KEY, in_out_status TEXT, timestamp TEXT, number_plate TEXT); """)
    # Committing the changes
    conn.commit()
    
    # Retrieving data from the table
    cursor.execute(f"""SELECT * FROM parking where number_plate='{text}'; """)
    # Fetching the data
    data = cursor.fetchall()
    # print(data)
    if len(data) < 1:
        # Get required data 
        status = "IN"
        ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Inserting data into the table
        cursor.execute(f"""INSERT INTO parking (in_out_status, timestamp, number_plate) VALUES ('{status}', '{ts}', '{text}'); """)
        # Committing the changes
        conn.commit()

        display_message = f"Car number {text} enter {status.lower()} @ {ts}."
        return display_message
    
    else:
        display_message = f"Car number {text} enter {status.lower()} @ {ts}."
        return display_message

# Call reader for english words
reader = easyocr.Reader(['en'])

# capture live video strime
# URL = "http://192.168.0.115:8080/video" 
capture = cv2.VideoCapture(0)

while True:

    # read video strime
    _, frame = capture.read()
    frame = imutils.resize(frame, width=640, height=480) # set frame size

    # Convert colored image into grayscale formate
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply Filter and Edge Detection
    bfilter = cv2.bilateralFilter(gray, 11, 17, 17) # Noise reduction
    edged = cv2.Canny(bfilter, 30, 200) # Edge detection

    # Find Contours and Apply Mask
    keypoints = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(keypoints)
    contours = sorted(contours, key = cv2.contourArea,reverse=True)[:10]

    # Get the number plate location from image
    location = None
    for contour in contours:
        approx = cv2.approxPolyDP(contour,10,True)
        if len(approx) == 4:
            location = approx
            break

    result = []
    # print(f"location : {location}")
    if location is not None:
        mask = np.zeros(gray.shape, np.uint8)
        new_image = cv2.drawContours(mask, [location], 0, 255, -1)
        new_image = cv2.bitwise_and(frame, frame, mask=mask)

        (x, y) = np.where(mask == 255)
        (x1, y1) = (np.min(x), np.min(y))
        (x2, y2) = (np.max(x), np.max(y))
        cropped_image = gray[x1:x2+1, y1:y2+1]

        # use easy ocr to read text
        result = reader.readtext(cropped_image)
        # print(f"Number Plate : {result}")

    # Render Result
    try:
        text = result[0][-2]
        text = preprocess_number_plate(text)
        # print(f"text Plate : {text}")
        if text != None:
            font = cv2.FONT_HERSHEY_SIMPLEX
            res = cv2.putText(frame, 
                            text=text, 
                            # org=(approx[0][0][0]-25, approx[1][0][1]-20), 
                            org=(30,30), 
                            fontFace=font, 
                            fontScale=1, 
                            color=(0,255,0), 
                            thickness=1, 
                            lineType=cv2.LINE_AA)
            res = cv2.rectangle(frame, tuple(approx[0][0]), tuple(approx[2][0]), (0,255,0), 3)

            #  insert into table 
            display_message = car_registry(text)

            # display message on screen
            res = cv2.putText(frame, 
                            text=display_message, 
                            # org=(approx[0][0][0]-25, approx[1][0][1]-20), 
                            org=(30,30*3), 
                            fontFace=font, 
                            fontScale=0.5, 
                            color=(0,255,0), 
                            thickness=1, 
                            lineType=cv2.LINE_AA)
            
            res = cv2.putText(frame, 
                            text="Wait for 15 sec.", 
                            # org=(approx[0][0][0]-25, approx[1][0][1]-20), 
                            org=(30,30*4), 
                            fontFace=font, 
                            fontScale=0.5, 
                            color=(0,255,0), 
                            thickness=1, 
                            lineType=cv2.LINE_AA)

            # show the video strime
            cv2.imshow('LiveStrimeScreen1', res)
            time.sleep(0.3)
        else:
            # show the video strime
            cv2.imshow('LiveStrimeScreen1', frame)
            time.sleep(0.3)
    except:
        # show the video strime
        cv2.imshow('LiveStrimeScreen1', frame)
        time.sleep(0.3)

    # to stop the strime
    if cv2.waitKey(1) == ord("q"):
        break

# close the resorces
capture.release()
cv2.destroyAllWindows()
# # Closing the connection
# conn.close()