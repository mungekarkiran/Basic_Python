import glob
import cv2
import time
from datetime import datetime
import face_recognition
from PIL import Image
import numpy as np
from tensorflow.keras.models import load_model

# Load pre-trained emotion detection model
emotion_model = load_model('models\model_18_0.636_0.994.h5')  # You need to have a pre-trained model file

# Define the list of emotions
emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']

count = 0
# for file in glob.glob("video_data/*.mp4"):
#     print(file)

file = "video_data/video1.mp4"
vidcap = cv2.VideoCapture(file)
while (vidcap.isOpened()):
    success, image = vidcap.read()
    if success == True:
        now = str(datetime.now()).replace('-','').replace(':','').replace(' ','_').replace('.','_') # .strftime("%Y%m%d_%H%M%S")
        print(now)
        
        try:
            image_path = f"images/video_{now}.jpg" 
            cv2.imwrite(image_path, image)     # save frame as JPEG file   

            image = face_recognition.load_image_file(image_path)
            face_locations = face_recognition.face_locations(image)
            print(face_locations)
            print(f'there are {len(face_locations)} people in this image. ')

        except Exception as e:
            break

    # time.sleep(.5)

print("Done")