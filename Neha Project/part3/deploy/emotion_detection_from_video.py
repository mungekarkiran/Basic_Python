import cv2
import os
import time
import numpy as np
from datetime import datetime
import keras.utils as image 
from tensorflow.keras.models import load_model

def detect_emotion(video_file_path:str, model_file_path:str) -> str:
    # Load pre-trained emotion detection model
    print('Load pre-trained emotion detection model')
    emotion_model = load_model(model_file_path)  # You need to have a pre-trained model file

    # Load the pre-trained Haar Cascade for face detection
    print('Load the pre-trained Haar Cascade for face detection')
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Load the input video
    print('Load the input video')
    cap = cv2.VideoCapture(video_file_path)

    # Get the video dimensions and frame rate
    # print('Get the video dimensions and frame rate')
    width = int(cap.get(3))
    height = int(cap.get(4))
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Define the codec for the output video
    # print('Define the codec for the output video')
    fourcc = cv2.VideoWriter_fourcc(*'mp4v') # *'XVID'

    # Create VideoWriter object to save the modified video
    # print('Create VideoWriter object to save the modified video')
    video_now = str(datetime.now()).replace('-','').replace(':','').replace(' ','_').replace('.','_')
    saved_video_path = os.path.join('static', f'output_video_{video_now}.mp4')
    # os.path.join('static', 'style', 'video', f'output_video_{video_now}.avi')
    out = cv2.VideoWriter(saved_video_path, fourcc, fps, (width, height))
    # out = cv2.VideoWriter(saved_video_path, fourcc, 20.0, (320, 240))

    while True:
        # Capture frame-by-frame
        # print('Capture frame-by-frame')
        ret, frame = cap.read()
        
        if not ret:
            break
        
        # Convert the frame to grayscale for face detection
        # print('Convert the frame to grayscale for face detection')
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect faces in the frame
        # print('Detect faces in the frame')
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        # print(faces)
        
        # Loop through the detected faces
        # print('Loop through the detected faces')
        for (x, y, w, h) in faces:
            if w > 100 and h > 100:
                # Crop the face region
                # print('Crop the face region')
                face = frame[y:y+h, x:x+w]

                gray_img = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
                roi_gray = cv2.resize(gray_img, (48, 48))
                img_pixels = image.img_to_array(roi_gray)
                img_pixels = np.expand_dims(img_pixels, axis=0)
                img_pixels /= 255
                
                # Predict eomtions
                # print('Predict eomtions')
                predictions = emotion_model.predict(img_pixels)

                # Find max indexed array
                # print('Find max indexed array')
                max_index = np.argmax(predictions[0])

                emotions = ['Angry', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']
                predicted_emotion = emotions[max_index]

                cv2.putText(frame, predicted_emotion, (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                print(predicted_emotion)
                time.sleep(0.2)
        
        # Write the frame with marked faces to the output video
        # print('Write the frame with marked faces to the output video')
        out.write(frame)

        # Break the loop when the 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video objects
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    print('Release the video objects')

    return saved_video_path
