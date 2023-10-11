import os
import cv2
import time
import face_recognition
from datetime import datetime

def detect_face(video_file_path:str) -> str:
    # Load the video file
    print('Load the video file')
    video_capture = cv2.VideoCapture(video_file_path)
    # cv2.resize(image, (new_w, new_h))

    # Get the video dimensions and frame rate
    # print('Get the video dimensions and frame rate')
    width = int(video_capture.get(3))
    height = int(video_capture.get(4))
    fps = video_capture.get(cv2.CAP_PROP_FPS)

    # Create a directory to save the modified video
    # print('Create a directory to save the modified video')
    # os.makedirs("output_videos", exist_ok=True)

    # Generate a file name
    # print('Generate a file name')
    video_now = str(datetime.now()).replace('-','').replace(':','').replace(' ','_').replace('.','_')
    face_detect_video_file_path = os.path.join('static', 'style', 'video', f'face_detect_output_video_{video_now}.mp4') # avi

    # Define the codec and create a VideoWriter object to save the modified video
    # print('Define the codec and create a VideoWriter object to save the modified video')
    fourcc = cv2.VideoWriter_fourcc(*'avc1') # *'XVID'   *'mp4v'
    output_video = cv2.VideoWriter(face_detect_video_file_path, fourcc, fps, (width, height))
    # output_video = cv2.VideoWriter(face_detect_video_file_path, fourcc, 20.0, (320, 240))

    while True:
        # Capture frame-by-frame
        # print('Capture frame-by-frame')
        ret, frame = video_capture.read()

        if not ret:
            break

        # Find all the faces and face encodings in the current frame
        # print('Find all the faces and face encodings in the current frame')
        face_locations = face_recognition.face_locations(frame)
        time.sleep(0.3)

        # Loop through each face in this frame
        # print('Loop through each face in this frame')
        for i, (top, right, bottom, left) in enumerate(face_locations):

            # Draw a rectangle around the face
            # print(f'Draw a rectangle around the face : {i}')
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

        # Write the frame to the modified video
        # print('Write the frame to the modified video')
        output_video.write(frame)

        # Break the loop when the 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture object and close the window
    print('Release the video capture object and close the window')
    video_capture.release()
    output_video.release()
    cv2.destroyAllWindows()

    return face_detect_video_file_path