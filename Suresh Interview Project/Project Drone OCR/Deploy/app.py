# # To unzip main files
# from zipfile import ZipFile
# file_name = "/content/drive/MyDrive/Colab Notebooks/Project_Files.zip"
# print(file_name)
# with ZipFile(file_name, 'r') as zip:
#   zip.extractall()
#   print('done')

import os, time, random, datetime
import pandas as pd
import numpy as np
import cv2
import easyocr
import imutils
import sqlite3 as sql

# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
from local_info import *
# from pyngrok import ngrok

# Define a flask app
app = Flask(__name__)

# # start ngrok when app is run
# port_no = 5000
# ngrok.set_auth_token("2KdKVvWPZia5YkGnclMcSmJGTjF_7XRGo19n8sau4r29JNaPL")
# public_url =  ngrok.connect(port_no).public_url

@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')

@app.route('/predict', methods=['GET', 'POST'])
def upload():
    # sql connection
    connection = sql.connect("car_data.db")
    cursor = connection.cursor()
    
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']
        
        img_file_path = os.path.join(IMG_DIR_PATH, secure_filename(f.filename))
        # Save the file to ./uploads
        f.save(img_file_path)

        try:
            img = cv2.imread(img_file_path)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            bfilter = cv2.bilateralFilter(gray, 11, 17, 17) # Noise reduction
            edged = cv2.Canny(bfilter, 30, 200) # Edge detection
            # Find Contours and Apply Mask
            keypoints = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            contours = imutils.grab_contours(keypoints)
            contours = sorted(contours, key = cv2.contourArea,reverse=True)[:10]
            location = None
            for contour in contours:
                approx = cv2.approxPolyDP(contour,10,True)
                if len(approx) == 4:
                    location = approx
                    break
            mask = np.zeros(gray.shape, np.uint8)
            new_image = cv2.drawContours(mask, [location], 0, 255, -1)
            new_image = cv2.bitwise_and(img, img, mask=mask)
            (x, y) = np.where(mask == 255)
            (x1, y1) = (np.min(x), np.min(y))
            (x2, y2) = (np.max(x), np.max(y))
            cropped_image = gray[x1:x2+1, y1:y2+1]

            cropped_image_filename = "cropped_image.jpeg"
            cropped_image_file_path = os.path.join(IMG_DIR_PATH, secure_filename(cropped_image_filename))
            # Save the file to ./uploads
            # new_image.save(cropped_image_file_path)
            cv2.imwrite(cropped_image_file_path, new_image)
            
            # use easy ocr to read text
            reader = easyocr.Reader(['en'])
            result = reader.readtext(cropped_image)
            # print(f"result : {result}")

            if len(result)>0:
                number_plate = result[0][1]
                number_plate = number_plate.replace(" ", "").replace("-","")
                cursor.execute("select * from car_info where number_plate=:np;", {"np":number_plate})
                get_number_plate_info = cursor.fetchall()
                if len(get_number_plate_info)>0:
                    owner_name = get_number_plate_info[0][1]
                    address = get_number_plate_info[0][2]
                    phone_number = get_number_plate_info[0][3]
                    email_id = get_number_plate_info[0][4]
                # close sql connection
                connection.close()

                return render_template('index.html', flag=True, warning_flag=False, number_plate=number_plate, img_file_path=img_file_path, cropped_image_file_path=cropped_image_file_path, owner_name=owner_name, address=address, phone_number=phone_number, email_id=email_id)
            else:
                return render_template('index.html', flag=True, warning_flag=True)
        
        except Exception as e:
            print(f"Exception : {e}")
            return render_template('index.html', flag=True, warning_flag=True)

    return render_template('index.html', flag=False, warning_flag=False)

@app.route('/admin', methods=['GET'])
def admin():
    return render_template('admin.html')

@app.route('/insert_data', methods=['GET', 'POST'])
def insert_data():
    # sql connection
    connection = sql.connect("car_data.db")
    cursor = connection.cursor()
    
    if request.method == 'POST':
        number_plate = request.form.get('number_plate')
        owner_name = request.form.get('owner_name')
        address = request.form.get('address')
        phone_number = int(request.form.get('phone_number'))
        email_id = request.form.get('email_id')
        try:
            car_info_tuple = (number_plate, owner_name, address, phone_number, email_id)
            cursor.execute("insert into car_info values (?,?,?,?,?);", car_info_tuple)
            connection.commit()
            flag = True
            msg = "Data inserted successfully !!!"
        except Exception as e:
            print(f"Exception : {e}")
            flag = False
            msg = f"Error [403] : {e}"
        # close sql connection
        connection.close()
    return render_template('admin.html', flag=flag, msg=msg)

if __name__ == '__main__':
    # print(f"To acces the Gloable link please click {public_url}")
    # app.run(port=port_no)
    app.run(debug=True)

