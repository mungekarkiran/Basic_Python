from flask import Flask, render_template, Response, request
import cv2
import os
import base64
import uuid

app = Flask(__name__)

# Replace 'CAMERA_URL' with the actual URL of your IP camera stream.
CAMERA_URL = 'http://192.0.0.4:8080//video'

cap = cv2.VideoCapture(CAMERA_URL)

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
    image_data_url = request.form.get('image_data')
    if image_data_url:
        # Decode the base64 image data
        image_data = base64.b64decode(image_data_url.split(',')[1])
        
        # Generate a unique filename using UUID
        filename = os.path.join('captured_images', f'{str(uuid.uuid4())}.jpg')
        
        # Save the image to the file
        with open(filename, 'wb') as f:
            f.write(image_data)
        
        return 'Image captured and saved as ' + filename
    else:
        return 'Failed to capture an image'

if __name__ == '__main__':
    if not os.path.exists('captured_images'):
        os.makedirs('captured_images')
    app.run(debug=True)
