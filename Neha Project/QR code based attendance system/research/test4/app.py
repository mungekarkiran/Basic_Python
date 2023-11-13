from flask import Flask, render_template, Response, request
import cv2
import os
import base64
import sqlite3
import uuid

app = Flask(__name__)

# Initialize the SQLite database
conn = sqlite3.connect('qr_codes.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS qr_codes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data TEXT
    )
''')
conn.commit()
conn.close()

# Initialize the webcam capture object
cap = cv2.VideoCapture(0)

def generate_frames():
    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            if not ret:
                continue
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/capture', methods=['POST'])
def capture():
    image_blob = request.files['image']

    if image_blob:
        # Generate a unique filename using UUID
        filename = os.path.join('captured_images', f'{str(uuid.uuid4())}.jpg')
        
        # Save the image to the file
        image_blob.save(filename)
        
        return f'Image captured and saved as {filename}'
    else:
        return 'Failed to capture an image'

@app.route('/scan', methods=['POST'])
def scan():
    image_blob = request.files['image']

    if image_blob:
        # Generate a unique filename using UUID
        filename = os.path.join('captured_images', f'QR_{str(uuid.uuid4())}.jpg')
        
        # Save the image to the file
        image_blob.save(filename)
        
        return f'Image captured and saved as {filename}'
    else:
        return 'Failed to capture an image'


if __name__ == '__main__':
    if not os.path.exists('captured_images'):
        os.makedirs('captured_images')
    app.run(debug=True)
