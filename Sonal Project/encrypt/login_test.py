import tkinter as tk

def verify_login():
    username = username_entry.get()
    password = password_entry.get()
    if username == "user" and password == "password":
        login_label.config(text="Login successful")
    else:
        login_label.config(text="Login failed")

# Create main window
root = tk.Tk()
root.title("Login")

# Create username label and entry
username_label = tk.Label(root, text="Username:")
username_label.pack()
username_entry = tk.Entry(root)
username_entry.pack()

# Create password label and entry
password_label = tk.Label(root, text="Password:")
password_label.pack()
password_entry = tk.Entry(root, show="*")
password_entry.pack()

# Create login button
login_button = tk.Button(root, text="Login", command=verify_login)
login_button.pack()

# Create login status label
login_label = tk.Label(root, text="")
login_label.pack()

# Start main loop
root.mainloop()
