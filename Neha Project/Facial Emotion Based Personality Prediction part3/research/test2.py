import cv2
import face_recognition

# Load the video file
video_capture = cv2.VideoCapture('video_data/video1.mp4')

# Load a sample picture and learn how to recognize it.
known_image = face_recognition.load_image_file("images\img.jpg")
known_face_encoding = face_recognition.face_encodings(known_image)[0]

# Initialize variables
face_locations = []
face_encodings = []
face_names = []

while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    # Find all the faces and face encodings in the current frame
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    # Loop through each face in this frame
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # See if the face matches any known face(s)
        matches = face_recognition.compare_faces([known_face_encoding], face_encoding)

        name = "Unknown"

        if True in matches:
            name = "Known Person"

        # Draw a rectangle around the face and display the name
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Break the loop when the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close the window
video_capture.release()
cv2.destroyAllWindows()
