from urllib.request import urlopen
#import urllib.request
#import urllib
import cv2
import numpy as np
import time

url='http://192.168.1.3:8080/shot.jpg'

while True:
    imgResp=urlopen(url)
    #imgResp=urllib.urlopen(url)
    #s = imgResp.read()
    #print(s)
    imgNp=np.array(bytearray(imgResp.read()),dtype=np.uint8)
    img=cv2.imdecode(imgNp,-1)
    #time.sleep(3)

    # all the opencv processing is done here
    cv2.imshow('test',img)
    if ord('q')==cv2.waitKey(10):
        exit(0)
