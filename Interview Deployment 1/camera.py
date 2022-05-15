from time import time
import time as tm
import cv2
from imutils.video import WebcamVideoStream
import numpy as np
from keras.models import load_model
from keras.preprocessing import image


# load model
model = load_model("best_model1.h5")
face_haar_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')


class VideoCamera(object):
    def __init__(self):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        self.stream = WebcamVideoStream(src=0).start()
        # self.stream = WebcamVideoStream(src=1).start()
        # self.stream = WebcamVideoStream(src='http://192.168.31.194:8080/video').start()

        self.dic = {'Angry':0, 'Disgust':0, 'Fear':0, 'Happy':0, 'Neutral':0, 'Sad':0, 'Surprise':0}

    def __del__(self):
        self.stream.stop()

    def get_frame(self):
        d = self.dic

        image1 = self.stream.read()

        # gray_img = cv2.cvtColor(image1, cv2.COLOR_BGR2RGB)
        gray_img = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
        faces_detected = face_haar_cascade.detectMultiScale(gray_img, 1.32, 5)

        try: 
            for (x, y, w, h) in faces_detected:
                cv2.rectangle(image1, (x, y), (x + w, y + h), (255, 0, 0), thickness=7)
                roi_gray = gray_img[y:y + w, x:x + h]  # cropping region of interest i.e. face area from image
                # roi_gray = cv2.resize(roi_gray, (224, 224))
                roi_gray = cv2.resize(roi_gray, (48, 48))
                img_pixels = image.img_to_array(roi_gray)
                img_pixels = np.expand_dims(img_pixels, axis=0)
                img_pixels /= 255

                predictions = model.predict(img_pixels)

                # find max indexed array
                max_index = np.argmax(predictions[0])

                emotions = ('Angry', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise')
                predicted_emotion = emotions[max_index]

                cv2.putText(image1, predicted_emotion, (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                
                d[predicted_emotion] += 1

                tm.sleep(0.5)

            # additional code
            # cv2.putText(image1, 'Score : '+str(d), (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 1)
            
            cv2.putText(image1, 'Angry : '+str(d['Angry']), (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 1)
            cv2.putText(image1, 'Disgust : '+str(d['Disgust']), (150, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 1)
            cv2.putText(image1, 'Fear : '+str(d['Fear']), (290, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 1)
            cv2.putText(image1, 'Happy : '+str(d['Happy']), (430, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 1)
            cv2.putText(image1, 'Neutral : '+str(d['Neutral']), (10, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 1)
            cv2.putText(image1, 'Sad : '+str(d['Sad']), (150, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 1)
            cv2.putText(image1, 'Surprise : '+str(d['Surprise']), (290, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 1)

        except Exception as e:
            print('Exception : ', e)
            pass

        _, jpeg = cv2.imencode('.jpg', image1)
        data = []
        data.append(jpeg.tobytes())
        return data