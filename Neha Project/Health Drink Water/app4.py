import tkinter as tk

def update_timer():
    global minutes
    minutes += 1
    timer_label.config(text=f"Timer: {minutes:02d}:00")
    root.after(60000, update_timer)  # Update every minute (60,000 milliseconds)

# Initialize minutes
minutes = 0

# Create the Tkinter application window
root = tk.Tk()
root.title("Timer App")

# Set the logo (icon) for the application window
root.iconbitmap("icon.ico")

# Set the background color of the application window
root.configure(bg="light blue")

# Create a label widget to display the timer
timer_label = tk.Label(root, text="Timer: 00:00", font=("Helvetica", 16))
timer_label.pack(pady=20)

# Start the timer
update_timer()

# Start the Tkinter event loop
root.mainloop()
