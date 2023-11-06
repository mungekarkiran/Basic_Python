import cv2
import numpy as np
import face_recognition
from PIL import Image
from tensorflow.keras.models import load_model

# Load pre-trained emotion detection model
emotion_model = load_model('models\model_18_0.636_0.994.h5')  # You need to have a pre-trained model file

# Initialize video capture from webcam or a video file
cap = cv2.VideoCapture('video1.mp4')  # Replace with your video file

# Define the list of emotions
emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']

# Define a function to detect emotions from a frame
def detect_emotion(face_image):
    
    face_frame = cv2.imread(face_image)

    # Preprocess the frame for emotion detection
    face_frame = cv2.cvtColor(face_image, cv2.COLOR_BGR2GRAY)
    face_frame = cv2.resize(face_frame, (48, 48))
    face_frame = face_frame/255.0
    face_frame = np.expand_dims(face_frame, axis=0)
    face_frame = np.expand_dims(face_frame, axis=-1)

    # Predict the emotion label
    emotion_prediction = emotion_model.predict(face_frame)
    emotion_index = np.argmax(emotion_prediction)
    print(f"emotion_index : {emotion_index} || emotion_labels : {emotion_labels[emotion_index]}")

    return emotion_labels[emotion_index]

# Define video writer to save the output
fourcc = cv2.VideoWriter_fourcc(*'MJPG') # cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output_video.avi', fourcc, 32.0, (640, 480))

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    # save frame in image formate
    cv2.imwrite("images/img.jpg", frame)

    # save face image
    image = face_recognition.load_image_file("images/img.jpg")
    # print(f"image : {image}")
    try:
        face_locations = face_recognition.face_locations(image)
        print(f"face_locations : {face_locations}")
        encoding = face_recognition.face_encodings(face_locations)[0]
        print(f"encoding : {encoding}")

        for face_location in face_locations:
            top, right, bottom, left = face_location
            print(f"{top}, {right}, {bottom}, {left}")
            try:
                face_image = image[top-100:bottom+100, left-100:right+100]
                pil_image = Image.fromarray(face_image)
            except Exception as e:
                face_image = image[top:bottom, left:right]
                pil_image = Image.fromarray(face_image)
            pil_image.save(f'images/face.jpg')

        emotion = detect_emotion('images/face.jpg')

        # Display emotion text on the frame
        cv2.putText(frame, emotion, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    except Exception as e:
        pass

    # Write frame to the output video
    out.write(frame)

    # Display the frame
    cv2.imshow('Emotion Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
out.release()
cv2.destroyAllWindows()
