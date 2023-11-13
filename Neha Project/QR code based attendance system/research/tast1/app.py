from flask import Flask, render_template, request, redirect, url_for
import cv2
import os
import uuid

app = Flask(__name__)

# Create a folder to store captured images
if not os.path.exists('captured_images'):
    os.makedirs('captured_images')

# Function to capture and save an image
def capture_image():
    cap = cv2.VideoCapture(0)

    # Capture a single frame
    ret, frame = cap.read()
    if ret:
        # Generate a unique filename using UUID
        filename = f'captured_images/{str(uuid.uuid4())}.jpg'
        
        # Save the captured frame as an image
        cv2.imwrite(filename, frame)
        cap.release()
        return filename
    else:
        cap.release()
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/capture', methods=['POST'])
def capture():
    image_path = capture_image()
    if image_path:
        return render_template('capture.html', image_path=image_path)
    else:
        return "Failed to capture an image."

if __name__ == '__main__':
    app.run(debug=True)
