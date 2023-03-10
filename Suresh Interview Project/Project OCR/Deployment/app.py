import numpy as np
import sys, os, glob, re, time, random
import uuid

# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename

# lib's for OCR
import easyocr
import cv2

# Keras
# from keras.models import load_model
# from keras.preprocessing import image

import warnings
warnings.filterwarnings('ignore')

# Define a flask app
app = Flask(__name__)

# Easy OCR English words reader
reader = easyocr.Reader(['en'], gpu=False)

# print('\nModel loaded. Start serving...')
# print('\nModel loaded. Check http://127.0.0.1:5000/')

@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')

@app.route('/predict', methods=['GET', 'POST'])
def upload():

    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']
        
        file_path = os.path.join('static', secure_filename(f.filename))
        # Save the file to ./uploads
        f.save(file_path)

        # read image
        img = cv2.imread(file_path)
        # resize image
        img = cv2.resize(img, (0, 0), fx = 0.6, fy = 0.6)

        # read text from image
        result = reader.readtext(img)
        detected_words = {word[1]:round(word[2]*100,2) for word in result}
        # print(f"result : {detected_words}")

        # draw bounding box
        spacer = 100
        font = cv2.FONT_HERSHEY_SIMPLEX
        for detection in result: 
            top_left = tuple(detection[0][0])
            bottom_right = tuple(detection[0][2])
            text = detection[1]
            img = cv2.rectangle(img,top_left,bottom_right,(0,255,0),1)
            img = cv2.putText(img,text,(20,spacer), font, 0.5,(0,255,0),1,cv2.LINE_AA)
            spacer+=15

        # Filename
        output_filename = os.path.join("static", f"img_{uuid.uuid4()}.jpg")

        # Using cv2.imwrite() method, Saving the image
        cv2.imwrite(output_filename, img)
        print('Successfully saved')


        return render_template('index.html', file_path=file_path[7:], output_file_path=output_filename[7:], detected_words=detected_words, download_file="example.jpg")
    return None

if __name__ == '__main__':
    app.run(debug=True)
    # app.run()

