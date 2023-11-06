import cv2
import os
import time
import numpy as np
from datetime import datetime
import keras.utils as image 
# from tensorflow.keras.models import load_model

# def detect_emotion(video_file_path:str, model_file_path:str) -> str:
def detect_emotion(video_file_path:str, emotion_model) -> str:

    key_counts = {'Angry':0, 'Disgust':0, 'Fear':0, 'Happy':0, 'Neutral':0, 'Sad':0, 'Surprise':0}
    personalitys_data = {
        'Angry': 'Frequent anger might be associated with low agreeableness. Individuals who often experience anger might be less agreeable, meaning they are less likely to be cooperative or friendly.', 
        'Disgust': 'High disgust levels may be related to neuroticism. Disgust and neuroticism often go hand in hand, as individuals with high neuroticism tend to experience more disgust.', 
        'Fear': 'Frequent fear may be related to neuroticism. Individuals who experience fear more often may have higher levels of neuroticism.', 
        'Happy': 'High levels of happiness may be associated with extroversion and openness. Happy individuals might be more sociable (extroversion) and open to new experiences (openness).', 
        'Neutral': 'Neutral may be associated with agreeableness and conscientiousness. Content individuals may be more agreeable (friendly) and conscientious (organized and responsible).', 
        'Sad': 'High levels of happiness may be associated with extroversion and openness. Happy individuals might be more sociable (extroversion) and open to new experiences (openness).', 
        'Surprise': 'Frequent surprise might indicate openness to experience. People who are often surprised by new things may have a higher degree of openness to experience.'}

    # Load pre-trained emotion detection model
    print('Load pre-trained emotion detection model')
    # emotion_model = load_model(model_file_path)  # You need to have a pre-trained model file

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
    fourcc = cv2.VideoWriter_fourcc(*"H264") # *'XVID'  *'mp4v'  *'H264'   *'MJPG'   *"vp80"   *'avc1'

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
            # x = top
            # y = right
            # w = bottom
            # h = left
            if w > 200 and h > 200:
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
                # Check if the key exists in the dictionary
                if predicted_emotion in key_counts:
                    # If it exists, increment the count
                    key_counts[predicted_emotion] += 1
                else:
                    # If it doesn't exist, initialize the count to 1
                    key_counts[predicted_emotion] = 1

                # Draw a rectangle around the face
                # cv2.rectangle(image, pt1, pt2, color, thickness)
                # where pt1 is starting point-->(x,y) and pt2 is end point-->(x+w,y+h).
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                time.sleep(1)
        
        # Write the frame with marked faces to the output video
        # print('Write the frame with marked faces to the output video')
        out.write(frame)

        # Break the loop when the 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Calculate the total sum of values
    total = sum(key_counts.values())

    # Convert values to percentages
    percentage_data = {key: (value / total) * 100 for key, value in key_counts.items()}

    result = [key for key, value in percentage_data.items() if value > 0]
    personalitys_list = [value for key, value in personalitys_data.items() if key in result]
    
    # Release the video objects
    print('Release the video objects and close the window')
    cap.release()
    out.release()
    cv2.destroyAllWindows()

    return saved_video_path, percentage_data, personalitys_list
