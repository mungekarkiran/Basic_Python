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

    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']
        
        img_file_path = os.path.join(IMG_DIR_PATH, secure_filename(f.filename))
        # Save the file to ./uploads
        f.save(img_file_path)

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
        number_plate = result[0][1]
        
        number_plate = number_plate.replace(" ", "")

        return render_template('index.html', flag=True, number_plate=number_plate, img_file_path=img_file_path, cropped_image_file_path=cropped_image_file_path)

    return render_template('index.html', flag=False)


if __name__ == '__main__':
    # print(f"To acces the Gloable link please click {public_url}")
    # app.run(port=port_no)
    app.run(debug=True)

