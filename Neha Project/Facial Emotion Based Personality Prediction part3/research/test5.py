# import time
from datetime import datetime
start_time = datetime.now() # time.time()
face_detection_time_start = datetime.now() # time.time()

import face_detection_from_video as fdv

video_file_path = 'video_data/v4.mp4'
face_video_path = fdv.detect_face(video_file_path)
print(f"face_video_path : {face_video_path}")

face_detection_time_end = datetime.now() # time.time()
print(f"Time to detect face is : {face_detection_time_end - face_detection_time_start} | Total time : {face_detection_time_end - start_time}")

emotion_detection_time_start = datetime.now() # time.time()

import emotion_detection_from_video as edv

model_file_path = 'models/model_18_0.636_0.994.h5'
# face_video_path = 'output_videos/face_detect_output_video_20231001_043815_878141.avi'
saved_video_path = edv.detect_emotion(face_video_path, model_file_path)
print(f"saved_video_path : {saved_video_path}")

emotion_detection_time_end = datetime.now() # time.time()
print(f"Time to detect emotion is : {face_detection_time_end - emotion_detection_time_start} | Total time : {face_detection_time_end - start_time}")
