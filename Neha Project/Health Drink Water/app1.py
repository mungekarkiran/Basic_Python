import tkinter as tk
import threading
import time

from datetime import datetime
from plyer import notification
import pyttsx3
import logging

# Config the log file
logging.basicConfig(
    filename='app.log', 
    filemode='a', 
    level=logging.INFO, format='%(asctime)s | [%(name)s : %(levelname)s] | %(message)s'
    )

# Global variable to store the note
note = ""

# Variable used to store water level information
water_level, daily_max_limit = 0, 4000

def save_note():
    global note
    note = text.get("1.0", "end-1c")
    with open("sticky_note.txt", "w") as file:
        file.write(note)

def display_time():
    current_time = time.strftime("%H:%M:%S")
    time_label.config(text=f"Current Time: {current_time}")
    root.after(60000, display_time)  # 1 minutes in milliseconds

def auto_save():
    while True:
        time.sleep(60)  # Auto-save every 60 seconds (adjust as needed)
        save_note()

def get_greeting() -> str:
    '''
    This function is used to greeting the user as per current time.
    '''
    now = datetime.now()
    hrs = int(now.strftime("%H"))
    if 6 <= hrs <= 11:
        msg = f"Good morning dear."  
    elif 12 <= hrs <= 17:  
        msg = f"Good afternoon dear."
    elif 18 <= hrs <= 20:
        msg = f"Good evening dear."
    else:  
        msg = f"Good night dear."
    return msg

def say(msg:str) -> None:
    '''
    This function is used to convert text message to speech.
    '''
    print(msg)
    engine = pyttsx3.init()
    engine.say(msg)
    engine.runAndWait()

def show_notification() -> None:
    '''
    This function is used to show the notification on screen.
    '''
    global water_level
    msg = f"Please drink a glass of water at least 100 milliliters."
    notification.notify(
        title = "Stay Healthy and Happy",
        message = msg,
        timeout = 15 # displaying time
        )
    time.sleep(5)
    say(msg)

    time.sleep(15)
    water_level += 100
    water_level_pct = round((water_level/daily_max_limit)*100, 1)
    msg1 = f"Congratulations!! You successfully achieved {water_level_pct} percent of your daily water drinking target. Till now you have drank a total of {water_level} milliliters of water. Have a nice day dear."
    say(msg1)

    logging.info(f"user_name : user, water_level : {water_level} milliliters, water_level_pct : {water_level_pct} percent.")

def show_lunch_notification():
    msg = f"Please have you lunch."
    notification.notify(
        title = "Stay Healthy and Happy",
        message = msg,
        timeout = 15 # displaying time
        )
    time.sleep(5)
    say(msg)
    time.sleep(15)

def task_reminder() -> None:
    '''
    This function is used to run in loop for showing the task reminder to user after every 1 hrs. 
    '''
    while True:
        # function call greeting and text to speech
        say(get_greeting()) 

        # function call show notification
        show_notification() 

        # function call lunch notification 
        now = datetime.now()
        hrs = int(now.strftime("%H"))
        if hrs == 1:
            show_lunch_notification() 
            time.sleep(1800) # sleep for 1/2 hrs.

        # time.sleep(3600) # sleep for 1 hrs.
        # time.sleep(1800) # sleep for 1/2 hrs.
        time.sleep(60*2) # sec * min * hrs

# Create a tkinter window
root = tk.Tk()
root.title("Sticky Note")

# Create a text widget for the note
text = tk.Text(root, wrap=tk.WORD, width=40, height=30)
text.pack()

# Create a label to display the time
time_label = tk.Label(root, text="")
time_label.pack()

# Load saved note if available
try:
    with open("sticky_note.txt", "r") as file:
        saved_note = file.read()
        text.insert("1.0", saved_note)
        note = saved_note
except FileNotFoundError:
    pass

# Create a "Save" button
save_button = tk.Button(root, text="Save Note", command=save_note)
save_button.pack()

# Start displaying the time
display_time()

# Start the auto-save function in the background
auto_save_thread = threading.Thread(target=auto_save)
auto_save_thread.daemon = True
auto_save_thread.start()

# Start the task_reminder function in the background
task_reminder_thread = threading.Thread(target=task_reminder)
task_reminder_thread.daemon = True
task_reminder_thread.start()

# Start the tkinter main loop
root.mainloop()
