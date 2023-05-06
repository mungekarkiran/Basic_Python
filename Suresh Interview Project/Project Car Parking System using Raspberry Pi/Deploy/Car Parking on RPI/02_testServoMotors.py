import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD) # gpio.setmode(gpio.BCM)
GPIO.setup(12, GPIO.OUT) # pin number 12
GPIO.setup(16, GPIO.OUT) # pin number 16
# board == pin number
# bcm == GPIO number

p = GPIO.PWM(12, 50)
p.start(90)

q = GPIO.PWM(16, 50)
q.start(90)

print("Wait for 1 sec.")
time.sleep(1)

def move_moter(moter):
    moter.ChangeDutyCycle(7.5) # for 90 deg. and 12.5 is 180 deg.
    time.sleep(1)
    moter.ChangeDutyCycle(3)
    time.sleep(1)
    
    # moter.stop()
    # GPIO.cleanup()
    
while True:
    move_moter(p)
    time.sleep(2)
    
    move_moter(q)
    time.sleep(2)
    
    
    #p.ChangeDutyCycle(7.5) # for 90 deg.
    #time.sleep(3/2)
    #p.ChangeDutyCycle(11.5)
    #time.sleep(3/2)
    
    
    #p.ChangeDutyCycle(10)
    #time.sleep(0.5)
