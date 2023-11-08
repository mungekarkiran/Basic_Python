import time
from datetime import datetime
from plyer import notification
import pyttsx3
import logging
logging.basicConfig(
    filename='app.log', 
    filemode='a', 
    level=logging.INFO, format='%(asctime)s | [%(name)s : %(levelname)s] | %(message)s'
    )

def get_greeting(user_name:str) -> str:
    '''
    This function is used to greeting the user as per current time.
    '''
    now = datetime.now()
    # current_time = now.strftime("%H:%M:%S")
    # print("Current Time =", current_time)
    hrs = int(now.strftime("%H"))
    if 6 <= hrs <= 11:
        msg = f"Good morning {user_name}."  
    elif 12 <= hrs <= 17:  
        msg = f"Good afternoon {user_name}."
    elif 18 <= hrs <= 20:
        msg = f"Good evening {user_name}."
    else:  
        msg = f"Good night {user_name}."
    return msg

def say(msg:str) -> None:
    '''
    This function is used to convert text message to speech.
    '''
    print(msg)
    engine = pyttsx3.init()
    engine.say(msg)
    engine.runAndWait()

def show_notification(user_name:str) -> None:
    '''
    This function is used to show the notification on screen.
    '''
    global water_level
    msg = f"Please drink a glass of water at least 100 milliliters."
    notification.notify(
        title = "Stay Healthy and Happy",
        message = msg,
        timeout = 10 # displaying time
        )
    time.sleep(5)
    say(msg)
    # print(msg)
    time.sleep(15)
    water_level += 100
    water_level_pct = round((water_level/daily_max_limit)*100, 1)
    msg1 = f"Congratulations!! You successfully achieved {water_level_pct} percent of your daily water drinking target. Till now you have drank a total of {water_level} milliliters of water. Have a nice day dear."
    say(msg1)
    # print(msg1)
    logging.info(f"user_name : {user_name}, water_level : {water_level} milliliters, water_level_pct : {water_level_pct} percent.")

def task_reminder(user_name:str) -> None:
    '''
    This function is used to run in loop for showing the task reminder to user after every 1 hrs. 
    '''
    while True:
        say(get_greeting(user_name)) # function call greeting and text to speech
        show_notification(user_name) # function call show notification
        # time.sleep(3600) # sleep for 1 hrs.
        # time.sleep(1800) # sleep for 1/2 hrs.
        time.sleep(60*2) # sec * min * hrs

if __name__ == "__main__":
    water_level = 0 # variable used to store water level information
    daily_max_limit = 4000
    user_name = input("Dear user please enter your name : ") # get the input from user 
    task_reminder(user_name) # function call for task reminder