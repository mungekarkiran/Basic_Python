import tkinter as tk
from tkinter import Menu, Toplevel, messagebox, filedialog
from tkinter.ttk import *
from tkinter.scrolledtext import ScrolledText
import threading
import time
from datetime import datetime, timedelta
import pyttsx3
import logging
from plyer import notification
from tkinter import Canvas, Scrollbar

# Global variables
water_level_ml = 0
water_level_cups = 0
daily_water_target_ml = 4000  # 4 liters
glass_size_ml = 250  # Standard glass size of 250ml
save_location = "sticky_note.snt"
greetings = {
    "morning": "Good morning, Today is a blank canvas; paint a masterpiece.",
    "afternoon": "Good afternoon, You are left with half day; keep pushing forward.",
    "evening": "Good evening, Finish the day strong, and tomorrow will thank you.",
    "night": "Good night, Dream big, tomorrow is a new chance to make it real."
}

food_intake = 0
lunch_notification_time = "12:00 PM"  # Example initial value
bedtime_notification_time = "10:00 PM"  # Example initial value
task_reminder_notification_time = "Every 2 hours"  # Example initial value

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Function to open text file
def open_text_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        try:
            with open(file_path, "r") as file:
                text.delete("1.0", tk.END)
                text.insert(tk.END, file.read())
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open file: {str(e)}")

# Function to save the note
def save_note():
    note = text.get("1.0", "end-1c")
    with open(save_location, "w") as file:
        file.write(note)

# Function to change the save location
        
def change_save_location(new_location):
    global save_location
    save_location = new_location

# Function to change greetings
def change_greeting(time_of_day, new_greeting):
    global greetings
    greetings[time_of_day] = new_greeting
    save_settings()  # Save modified greetings

# Function to save settings
def save_settings():
    with open("greetings_settings.txt", "w") as file:
        for time_of_day, greeting in greetings.items():
            file.write(f"{time_of_day}:{greeting}\n")

# Function to display current time
def display_time():
    current_time = time.strftime("%H:%M:%S")
    time_label.config(text=f"Time: {current_time}")
    root.after(1000, display_time)

# Function to get the appropriate greeting based on the time
def get_greeting():
    now = datetime.now()
    hrs = int(now.strftime("%H"))
    if 6 <= hrs < 12:
        greeting = greetings["morning"]
    elif 12 <= hrs < 18:
        greeting = greetings["afternoon"]
    elif 18 <= hrs < 21:
        greeting = greetings["evening"]
    else:
        greeting = greetings["night"]
    
    # Speak the greeting message
    say(greeting)
    
    return greeting


# Function to speak the given message
def say(msg):
    print(msg)
    voice = engine.getProperty('voices')
    engine.setProperty('voice', voice[2].id)
    engine.say(msg)


# Function to show notification
def show_notification(title, message):
    notification.notify(
        title=title,
        message=message,
        timeout=5
    )
    time.sleep(5)
    say(message)
    engine.runAndWait()  # This should be called only once after all messages are added to the queue

# Function to show lunch notification
def show_lunch_notification():
    msg = "Please have your lunch."
    show_notification("Stay Healthy and Happy", msg)
    time.sleep(5)

# Function to show bedtime notification
def show_bedtime_notification():
    msg = "It's bedtime. Have a good night's sleep!"
    show_notification("Bedtime Reminder", msg)
    time.sleep(5)

# Function to show task reminder notification
def show_task_reminder_notification():
    msg = "Hey hard worker, don't forget to take breaks and stay hydrated!"
    show_notification("Task Reminder", msg)
    time.sleep(5)

# Function to calculate seconds until a specific time
def seconds_until_specific_time(target_time):
    current_time = time.localtime()
    target_time = time.strptime(target_time, "%H:%M")  # Convert target time to struct_time
    target_time = time.struct_time((current_time.tm_year, current_time.tm_mon, current_time.tm_mday,
                                    target_time.tm_hour, target_time.tm_min, 0, current_time.tm_wday,
                                    current_time.tm_yday, current_time.tm_isdst))
    time_difference = time.mktime(target_time) - time.mktime(current_time)
    if time_difference < 0:
        time_difference += 24 * 3600  # Add one day if target time is in the past
    return time_difference

# Function to run the timer
def run_timer(minutes):
    remaining_seconds = minutes * 60
    timer_label.config(text=f"Timer: {minutes:02d}:00")

    while remaining_seconds >= 0:
        # Calculate remaining minutes and seconds
        mins, secs = divmod(remaining_seconds, 60)

        # Format the time as MM:SS
        timer_text = f"{mins:02d}:{secs:02d}"

        # Update the label text with the remaining time
        timer_label.config(text=f"Timer: {timer_text}")

        # Wait for one second
        time.sleep(1)

        # Decrement the remaining time by one second
        remaining_seconds -= 1

    # When the timer is up, show a message
    messagebox.showinfo("Timer", "Timer is up!")

# Get the time to start the timer
start_time = "10:00"  # Example time (10:00 AM)

# Calculate the seconds until the specific time
seconds_until_start = seconds_until_specific_time(start_time)
print(f"seconds_until_start : {seconds_until_start}")
# Wait until the specific time
# time.sleep(seconds_until_start)

# Call your existing function to start the timer with a duration of 10 minutes (for example)
run_timer(10)

# Function to set the timer
def set_timer(minutes):
    threading.Thread(target=run_timer, args=(minutes,), daemon=True).start()

# Function to run the timer
def run_timer(minutes):
    remaining_seconds = minutes * 60
    timer_label.config(text=f"Timer: {minutes:02d}:00")
    
    while remaining_seconds >= 0:
        # Calculate remaining minutes and seconds
        mins, secs = divmod(remaining_seconds, 60)

        # Format the time as MM:SS
        timer_text = f"{mins:02d}:{secs:02d}"

        # Update the label text with the remaining time
        timer_label.config(text=f"Timer: {timer_text}")

        # Wait for one second
        time.sleep(1)

        # Decrement the remaining time by one second
        remaining_seconds -= 1

    # When the timer is up, show a message
    messagebox.showinfo("Timer", "Timer is up!")

# Function to mark water intake
def mark_water_intake():
    global water_level_ml, water_level_cups
    intake_amount_str = intake_entry.get()
    try:
        intake_amount_ml = int(intake_amount_str)
    except ValueError:
        intake_amount_ml = 0
    
    water_level_ml += intake_amount_ml
    water_level_cups += intake_amount_ml / glass_size_ml
    
    water_level_pct = round((water_level_ml / daily_water_target_ml) * 100, 1)
    msg = f"Water intake marked. You have consumed {intake_amount_ml}ml of water " \
          f"({water_level_cups:.2f} cups, {water_level_ml}ml in total, {water_level_pct}% of your daily target)."
    logging.info(msg)
    show_notification("Water Intake", msg)

# Function to remind about tasks
def task_reminder():
    while True:
        # Perform task reminder logic here
        time.sleep(60)  # Sleep for 60 seconds before checking again

# Function to display additional information
def show_info(event=None):
    info_message = "1 glass of water is approximately 250ml.\n\n" \
                   "General guidelines:\n" \
                   "- Drink water throughout the day to stay hydrated.\n" \
                   "- Stay mindful of your water intake during meals.\n" \
                   "- Avoid excessive consumption of sugary drinks.\n" \
                   "- Incorporate hydrating foods into your diet such as fruits and vegetables.\n STAY SAFE AND HEALTHY"
    messagebox.showinfo("Information", info_message)

## Function to open settings window
def open_settings_window():
    global greetings, food_intake, lunch_notification_time, bedtime_notification_time, task_reminder_notification_time

    settings_window = Toplevel(root)
    settings_window.title("Settings")
    settings_window.geometry("400x400")

    # Morning Greeting Setup
    morning_frame = Frame(settings_window)
    morning_frame.pack(pady=10)

    morning_label = Label(morning_frame, text="Morning Greeting:")
    morning_label.grid(row=0, column=0, padx=10)

    morning_entry = Entry(morning_frame, width=30)
    morning_entry.insert(tk.END, greetings["morning"])
    morning_entry.grid(row=0, column=1, padx=10)

    morning_save_button = Button(morning_frame, text="Save", command=lambda: change_greeting("morning", morning_entry.get()))
    morning_save_button.grid(row=0, column=2, padx=10)

    # Afternoon Greeting Setup
    afternoon_frame = Frame(settings_window)
    afternoon_frame.pack(pady=10)

    afternoon_label = Label(afternoon_frame, text="Afternoon Greeting:")
    afternoon_label.grid(row=0, column=0, padx=10)

    afternoon_entry = Entry(afternoon_frame, width=30)
    afternoon_entry.insert(tk.END, greetings["afternoon"])
    afternoon_entry.grid(row=0, column=1, padx=10)

    afternoon_save_button = Button(afternoon_frame, text="Save", command=lambda: change_greeting("afternoon", afternoon_entry.get()))
    afternoon_save_button.grid(row=0, column=2, padx=10)

    # Evening Greeting Setup
    evening_frame = Frame(settings_window)
    evening_frame.pack(pady=10)

    evening_label = Label(evening_frame, text="Evening Greeting:")
    evening_label.grid(row=0, column=0, padx=10)

    evening_entry = Entry(evening_frame, width=30)
    evening_entry.insert(tk.END, greetings["evening"])
    evening_entry.grid(row=0, column=1, padx=10)

    evening_save_button = Button(evening_frame, text="Save", command=lambda: change_greeting("evening", evening_entry.get()))
    evening_save_button.grid(row=0, column=2, padx=10)

    # Night Greeting Setup
    night_frame = Frame(settings_window)
    night_frame.pack(pady=10)

    night_label = Label(night_frame, text="Night Greeting:")
    night_label.grid(row=0, column=0, padx=10)

    night_entry = Entry(night_frame, width=30)
    night_entry.insert(tk.END, greetings["night"])
    night_entry.grid(row=0, column=1, padx=10)

    night_save_button = Button(night_frame, text="Save", command=lambda: change_greeting("night", night_entry.get()))
    night_save_button.grid(row=0, column=2, padx=10)

    # Save Button
    save_button = Button(settings_window, text="Save Settings", command=save_settings)
    save_button.pack(pady=10)

    # Food Intake Setup
    food_frame = Frame(settings_window)
    food_frame.pack(pady=10)

    food_label = Label(food_frame, text="Food Intake (calories):")
    food_label.grid(row=0, column=0, padx=10)

    food_entry = Entry(food_frame, width=30)
    food_entry.insert(tk.END, food_intake)
    food_entry.grid(row=0, column=1, padx=10)

    food_save_button = Button(food_frame, text="Save", command=lambda: save_food_intake(food_entry.get()))
    food_save_button.grid(row=0, column=2, padx=10)

    # Lunch Notification Setup
    lunch_frame = Frame(settings_window)
    lunch_frame.pack(pady=10)

    lunch_label = Label(lunch_frame, text="Lunch Notification:")
    lunch_label.grid(row=0, column=0, padx=10)

    lunch_entry = Entry(lunch_frame, width=30)
    lunch_entry.insert(tk.END, lunch_notification_time)
    lunch_entry.grid(row=0, column=1, padx=10)

    lunch_save_button = Button(lunch_frame, text="Save", command=lambda: save_notification_time("lunch", lunch_entry.get()))
    lunch_save_button.grid(row=0, column=2, padx=10)

    # Bedtime Notification Setup
    bedtime_frame = Frame(settings_window)
    bedtime_frame.pack(pady=10)

    bedtime_label = Label(bedtime_frame, text="Bedtime Notification:")
    bedtime_label.grid(row=0, column=0, padx=10)

    bedtime_entry = Entry(bedtime_frame, width=30)
    bedtime_entry.insert(tk.END, bedtime_notification_time)
    bedtime_entry.grid(row=0, column=1, padx=10)

    bedtime_save_button = Button(bedtime_frame, text="Save", command=lambda: save_notification_time("bedtime", bedtime_entry.get()))
    bedtime_save_button.grid(row=0, column=2, padx=10)

    canvas = Canvas(settings_window)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Add a scrollbar to the canvas
    scrollbar = Scrollbar(settings_window, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Configure the canvas to use the scrollbar
    canvas.configure(yscrollcommand=scrollbar.set)

# Create a frame inside the canvas to hold the settings widgets
    settings_frame = Frame(canvas)
    canvas.create_window((0, 0), window=settings_frame, anchor=tk.NW)

# Add widgets to the settings_frame as before

    # Task Reminder Notification Setup
    task_reminder_frame = Frame(settings_window)
    task_reminder_frame.pack(pady=10)

    task_reminder_label = Label(task_reminder_frame, text="Task Reminder Notification:")
    task_reminder_label.grid(row=0, column=0, padx=10)

    task_reminder_entry = Entry(task_reminder_frame, width=30)
    task_reminder_entry.insert(tk.END, task_reminder_notification_time)
    task_reminder_entry.grid(row=0, column=1, padx=10)

    task_reminder_save_button = Button(task_reminder_frame, text="Save", command=lambda: save_notification_time("task_reminder", task_reminder_entry.get()))
    task_reminder_save_button.grid(row=0, column=2, padx=10)

    # Start the task reminder function in the background
    task_reminder_thread = threading.Thread(target=task_reminder)
    task_reminder_thread.daemon = True
    task_reminder_thread.start()

# Function to save food intake
def save_food_intake(intake):
    global food_intake
    try:
        food_intake = int(intake)
        messagebox.showinfo("Food Intake", f"Food intake saved: {food_intake} calories.")
    except ValueError:
        messagebox.showerror("Food Intake", "Please enter a valid integer for food intake.")

# Function to save notification time
def save_notification_time(notification_type, time_str):
    global lunch_notification_time, bedtime_notification_time, task_reminder_notification_time
    try:
        datetime.strptime(time_str, "%I:%M %p")  # Check if the time string is in valid format
        if notification_type == "lunch":
            lunch_notification_time = time_str
        elif notification_type == "bedtime":
            bedtime_notification_time = time_str
        elif notification_type == "task_reminder":
            task_reminder_notification_time = time_str
        messagebox.showinfo("Notification Time", f"{notification_type.capitalize()} notification time saved: {time_str}")
    except ValueError:
        messagebox.showerror("Notification Time", "Please enter a valid time in format HH:MM AM/PM.")

# Create the main tkinter window
root = tk.Tk()
root.title("Sticky Note")
root.configure(bg="#F0F0F0")

# Set the font styles
label_font = ('Arial', 12)
button_font = ('Arial', 10)

# Menu Bar
menu_bar = Menu(root)
root.config(menu=menu_bar)

# File Menu
file_menu = Menu(menu_bar, tearoff=False)
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New")
file_menu.add_command(label="Open", command=open_text_file)
file_menu.add_command(label="Save", command=save_note)  # Changed to call save_note function
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

# Settings Menu
settings_menu = Menu(menu_bar, tearoff=False)
menu_bar.add_cascade(label="Settings", menu=settings_menu)
settings_menu.add_command(label="Open Settings", command=open_settings_window)

# Help Menu
help_menu = Menu(menu_bar, tearoff=False)
menu_bar.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(label="User Manual", command=show_info)

# Text Widget
text = ScrolledText(root, wrap=tk.WORD, width=50, height=20, font=label_font)
text.pack()

# Time Label
time_label = tk.Label(root, text="", bg="#F0F0F0", font=label_font)
time_label.pack()

# Water Intake Entry
intake_label = tk.Label(root, text="Water Intake (ml):", bg="#F0F0F0", font=label_font)
intake_label.pack()
intake_entry = tk.Entry(root, font=label_font)
intake_entry.pack()

# Button to mark water intake
water_intake_button = tk.Button(root, text="Mark Water Intake", command=mark_water_intake, font=button_font)
water_intake_button.pack()

# Info Button
info_button = tk.Button(root, text="Info", command=show_info, font=button_font)
info_button.pack()

# Countdown Timer Label
timer_label = tk.Label(root, text="Timer: 00:00", bg="#F0F0F0", font=label_font)
timer_label.pack(pady=20)

# Start displaying the time
display_time()

# Start the tkinter event loop
root.mainloop()
