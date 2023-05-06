import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD) # gpio.setmode(gpio.BCM)
GPIO.setup(13, GPIO.IN) # pin number 13 
GPIO.setup(11, GPIO.IN) # pin number 11 

while True:
    val1 = GPIO.input(13)
    val2 = GPIO.input(11)
    
    print("Val 1 : ", val1," || Val 2 : ", val2)
    time.sleep(2)
    