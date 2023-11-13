from flask import Flask, render_template, request, redirect, url_for
import cv2
import os
import uuid

app = Flask(__name__)

# Initialize the webcam capture object
# cap = cv2.VideoCapture(0) # , cv2.CAP_DSHOW

# Replace 'CAMERA_URL' with the actual URL of your IP camera stream.
CAMERA_URL = 'http://192.0.0.4:8080/video' # 'http://192.168.0.100:8080/video'
cap = cv2.VideoCapture(CAMERA_URL)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/capture', methods=['POST'])  # Changed to accept POST requests
def capture():
    ret, frame = cap.read()
    if ret:
        # Generate a unique filename using UUID
        filename = f'captured_images/{str(uuid.uuid4())}.jpg'
        # Save the captured frame as an image
        cv2.imwrite(filename, frame)
        return 'Image captured and saved as ' + filename
    else:
        return 'Failed to capture an image'

if __name__ == '__main__':
    app.run(debug=True)

# mhd tv world
# https://andisearch.com/