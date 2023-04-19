import tkinter as tk
import tkinter.messagebox as msgbox
import tkinter.ttk as ttk
import tkinter.scrolledtext as scrolledtext
import tkinter.simpledialog as simpledialog
import tkinter.filedialog as filedialog
import tkinter.font as font
import pyperclip

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.geometry("400x400")
        self.create_widgets()

    def create_widgets(self):
        # Create a label for the textbox
        self.label = tk.Label(self.master, text="Enter Text:")
        self.label.pack(padx=10, pady=10)

        # Create a textbox for the user to enter text
        self.textbox = scrolledtext.ScrolledText(self.master, width=40, height=10)
        self.textbox.pack(padx=10, pady=10)

        # Create a button to copy text to the clipboard
        self.copy_button = ttk.Button(self.master, text="Copy to Clipboard", command=self.copy_to_clipboard)
        self.copy_button.pack(pady=10)

    def copy_to_clipboard(self):
        # Get the text from the textbox
        text = self.textbox.get("1.0", tk.END)

        # Copy the text to the clipboard
        pyperclip.copy(text)

        # Show a message box to confirm that the text has been copied
        msgbox.showinfo("Success", "Text copied to clipboard")

root = tk.Tk()
app = Application(master=root)
app.mainloop()
