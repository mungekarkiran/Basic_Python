import cv2
import face_recognition
import os
import numpy as np
from datetime import datetime

# Load the video file
video_capture = cv2.VideoCapture('video_data/v1.mp4')

# Get the video dimensions and frame rate
width = int(video_capture.get(3))
height = int(video_capture.get(4))
fps = video_capture.get(cv2.CAP_PROP_FPS)

# Create a directory to save the cropped face images
# os.makedirs("face_images", exist_ok=True)

# Create a directory to save the modified video
os.makedirs("output_videos", exist_ok=True)

video_now = str(datetime.now()).replace('-','').replace(':','').replace(' ','_').replace('.','_')
video_file_path = f'output_videos/output_video_{video_now}.avi'
# Define the codec and create a VideoWriter object to save the modified video
fourcc = cv2.VideoWriter_fourcc(*'XVID') 
output_video = cv2.VideoWriter(video_file_path, fourcc, fps, (width, height))

frame_count = 0

while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    if not ret:
        break

    frame_count += 1

    # Find all the faces and face encodings in the current frame
    face_locations = face_recognition.face_locations(frame)

    # Loop through each face in this frame
    for i, (top, right, bottom, left) in enumerate(face_locations):
        # Crop the face from the frame
        # face_image = frame[top:bottom, left:right]

        # Save the cropped face image
        # face_filename = f"face_images/face_{frame_count}_{i}.jpg"
        # cv2.imwrite(face_filename, face_image)

        # Draw a rectangle around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

    # Write the frame to the modified video
    output_video.write(frame)

    # Display the resulting image
    # cv2.imshow('Video', frame)

    # Break the loop when the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close the window
video_capture.release()
output_video.release()
cv2.destroyAllWindows()
