from __future__ import division, print_function
import sys, os, glob, re, time

# Flask utils
from flask import Flask, redirect, url_for, request, render_template, Response
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer

# Ngrok
from flask_ngrok import run_with_ngrok

# camera
from camera import VideoCamera
import cv2

# firebase
# !pip install Pyrebase4
from pyrebase import pyrebase

import warnings
warnings.filterwarnings('ignore')


# Define a flask app
app = Flask(__name__)

# start ngrok when app is run
# run_with_ngrok(app)


# route's
@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.htm')

def gen(camera):
    #get camera frame
    while True:
        frame = camera.get_frame()
        frame = frame[0]
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(debug=True)
    # app.run()
