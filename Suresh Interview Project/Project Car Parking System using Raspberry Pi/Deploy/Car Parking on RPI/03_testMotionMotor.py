import RPi.GPIO as GPIO
import time
from threading import Thread

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD) # gpio.setmode(gpio.BCM)

GPIO.setup(13, GPIO.IN) # pin number 13 MS1 
GPIO.setup(11, GPIO.IN) # pin number 11 Ms2

GPIO.setup(12, GPIO.OUT) # pin number 12 give you PWM MT1
GPIO.setup(16, GPIO.OUT) # pin number 16 give you PWM MT2

def move_moter(moter):
    moter.ChangeDutyCycle(7.5) # for 90 deg. and 12.5 is 180 deg.
    time.sleep(3)
    moter.ChangeDutyCycle(3)
    time.sleep(3)
    
def entery_door():
    global entry_counter
    while True:
        #print(".")
        # step 1 get data from motion sensor
        val1 = GPIO.input(13)
        print("val1 : ", val1, " entry_counter : ", entry_counter)
        if val1 == 1:
            entry_counter += val1
            if entry_counter > 15:
                print("Car entring")
                # step 2 scan number plate  
                
                # step 3 store into db
                
                # step 4 open door
                print("Door 1 opening...")
                move_moter(p)
                time.sleep(1)
                entry_counter = 0
        time.sleep(1)
        
def exit_door():
    global exit_counter
    while True:
        #print(".")
        # step 1 get data from motion sensor
        val2 = GPIO.input(11)
        print("val2 : ", val2, " exit_counter : ", exit_counter)
        if val2 == 1:
            exit_counter += val2
            if exit_counter > 15:  
                print("Car exiting")
                # step 2 scan number plate  
                
                # step 3 store into db
                
                # step 4 open door
                print("Door 2 opening...")
                move_moter(q)
                time.sleep(1)
                exit_counter = 0
        time.sleep(1)
    
if __name__ == "__main__":
    p = GPIO.PWM(12, 50)
    p.start(90)

    q = GPIO.PWM(16, 50)
    q.start(90)

    entry_counter = 0
    exit_counter = 0

    print("Wait for 1 sec.")
    time.sleep(1)
    
    entry_door_thread = Thread(target=entery_door, args=(), name='entry_door_thread')
    exit_door_thread = Thread(target=exit_door, args=(), name='exit_door_thread')
    
    entry_door_thread.start()
    exit_door_thread.start()
    