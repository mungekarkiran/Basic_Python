import tkinter as tk

def save_note():
    note = text.get("1.0", "end-1c")
    with open("sticky_note.txt", "w") as file:
        file.write(note)

# Create a tkinter window
root = tk.Tk()
root.title("Sticky Note")

# Create a text widget for the note
text = tk.Text(root, wrap=tk.WORD, width=40, height=30)
text.pack()

# Load saved note if available
try:
    with open("sticky_note.txt", "r") as file:
        saved_note = file.read()
        text.insert("1.0", saved_note)
except FileNotFoundError:
    pass

# Create a "Save" button
save_button = tk.Button(root, text="Save Note", command=save_note)
save_button.pack()

# Start the tkinter main loop
root.mainloop()
