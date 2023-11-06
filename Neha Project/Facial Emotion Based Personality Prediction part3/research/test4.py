import cv2
import keras.utils as image # => not working (from keras.preprocessing import image )
import numpy as np
from tensorflow.keras.models import load_model

# Load pre-trained emotion detection model
emotion_model = load_model('models\model_18_0.636_0.994.h5')  # You need to have a pre-trained model file

# Load the pre-trained Haar Cascade for face detection
# face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Load the input video
cap = cv2.VideoCapture('output_videos/output_video_20230926_133859_779686.avi')

# Get the video dimensions and frame rate
width = int(cap.get(3))
height = int(cap.get(4))
fps = cap.get(cv2.CAP_PROP_FPS)

# Define the codec for the output video
fourcc = cv2.VideoWriter_fourcc(*'XVID')

# Create VideoWriter object to save the modified video
out = cv2.VideoWriter('output_video.avi', fourcc, fps, (width, height))

while True:
    ret, frame = cap.read()
    
    if not ret:
        break
    
    # Convert the frame to grayscale for face detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    print(faces)
    # Loop through the detected faces
    for (x, y, w, h) in faces:
        if w > 100 and h > 100:
            # Crop the face region
            face = frame[y:y+h, x:x+w]

            gray_img = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
            roi_gray = cv2.resize(gray_img, (48, 48))
            img_pixels = image.img_to_array(roi_gray)
            img_pixels = np.expand_dims(img_pixels, axis=0)
            img_pixels /= 255
            
            predictions = emotion_model.predict(img_pixels)

            # find max indexed array
            max_index = np.argmax(predictions[0])

            emotions = ['Angry', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']
            predicted_emotion = emotions[max_index]

            cv2.putText(frame, predicted_emotion, (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            print(x+w, y+h, predicted_emotion)
        
        # Draw a square around the face
        # cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        
        # Save the cropped face image
        # cv2.imwrite('face_{}.jpg'.format(len(faces)), face)
    
    # Write the frame with marked faces to the output video
    out.write(frame)

    # Display the resulting image
    # cv2.imshow('Video', frame)

    # Break the loop when the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# Release the video objects
cap.release()
out.release()
cv2.destroyAllWindows()
