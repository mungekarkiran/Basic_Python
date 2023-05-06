import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD) # gpio.setmode(gpio.BCM)
GPIO.setup(31, GPIO.IN) # pin number 31
GPIO.setup(33, GPIO.IN) # pin number 33
GPIO.setup(35, GPIO.IN) # pin number 35 
GPIO.setup(37, GPIO.IN) # pin number 37

while True:
    ir_val1 = GPIO.input(31)
    ir_val2 = GPIO.input(33)
    ir_val3 = GPIO.input(35)
    ir_val4 = GPIO.input(37)
    
    print("Val 1 : ", ir_val1," || Val 2 : ", ir_val2," || Val 3 : ", ir_val3,\
          " || Val 4 : ", ir_val4)
    print(abs((ir_val1+ir_val2+ir_val3+ir_val4)-4))
    time.sleep(1)
    
