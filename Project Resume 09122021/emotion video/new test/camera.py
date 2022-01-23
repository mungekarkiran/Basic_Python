import cv2
from imutils.video import WebcamVideoStream
import numpy as np
from keras.models import  load_model
from keras.preprocessing import image


# load model
model = load_model("best_model.h5")
face_haar_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')


class VideoCamera(object):
    def __init__(self):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        self.stream = WebcamVideoStream(src=0).start()
        # self.stream = WebcamVideoStream(src=1).start()
        # self.stream = WebcamVideoStream(src='http://192.168.31.194:8080/video').start()

    def __del__(self):
        self.stream.stop()

    def get_frame(self):
        image1 = self.stream.read()

        # additional code
        cv2.putText(image1, 'Score : ', (5, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)

        gray_img = cv2.cvtColor(image1, cv2.COLOR_BGR2RGB)
        faces_detected = face_haar_cascade.detectMultiScale(gray_img, 1.32, 5)

        for (x, y, w, h) in faces_detected:
            cv2.rectangle(image1, (x, y), (x + w, y + h), (255, 0, 0), thickness=7)
            roi_gray = gray_img[y:y + w, x:x + h]  # cropping region of interest i.e. face area from  image
            roi_gray = cv2.resize(roi_gray, (224, 224))
            img_pixels = image.img_to_array(roi_gray)
            img_pixels = np.expand_dims(img_pixels, axis=0)
            img_pixels /= 255

            predictions = model.predict(img_pixels)

            # find max indexed array
            max_index = np.argmax(predictions[0])

            emotions = ('Angry', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise')
            predicted_emotion = emotions[max_index]

            cv2.putText(image1, predicted_emotion, (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    


        _, jpeg = cv2.imencode('.jpg', image1)
        data = []
        data.append(jpeg.tobytes())
        return data