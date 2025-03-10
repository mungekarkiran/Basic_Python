from tkinter import *
import base64
from tkinter import messagebox
import tkinter.font as font
import tkinter as tk
import pyperclip

user_input = []

#Encoding Function
def encode(key, msg):
    enc = []
    for i in range(len(msg)):
        list_key = key[i % len(key)]
        list_enc = chr((ord(msg[i]) + ord(list_key)) % 256)
        enc.append(list_enc)
    return base64.urlsafe_b64encode("".join(enc).encode()).decode()

#Decoding Function
def decode(key, code):
    dec = []
    enc = base64.urlsafe_b64decode(code).decode()
    for i in range(len(enc)):
        list_key = key[i % len(key)]
        list_dec = chr((256 + ord(enc[i]) - ord(list_key)) % 256)
        dec.append(list_dec)
    return "".join(dec)

def input_verification(msg, k, i):
    global user_input
    if (i==1):
        encode_msg = encode(k, msg)
        Output.set(encode_msg)
        # append data to user_input list
        user_input.append([msg, k, encode_msg]) 
        print(f"user input list result : {user_input}")
    elif(i==2):
        # find in list
        if len(user_input) > 0:
            for user_data in user_input:
                if str(msg) == user_data[2] and k == user_data[1]:
                    Output.set(decode(k, msg))    
                    break    
                else:
                    messagebox.showinfo('Error', 'Wrong password. Please try again.')    
    else:
        messagebox.showinfo('Ishan', 'Please Choose one of Encryption or Decrption. Try again.')

#Function that executes on clicking Show Message function
def Result():
    msg = Message.get()
    k= key.get()
    i = mode.get()
    if len(msg)==0:
        messagebox.showinfo('Error', 'Enter a valid message.') 
    elif len(k)==0:
        messagebox.showinfo('Error', 'Enter a valid password.') 
    else:
        input_verification(msg, k, i)

#Function that executes on clicking Reset function
def Reset():
    Message.set("")
    key.set("")
    mode.set(0)
    Output.set("")
    
def copy_to_clipboard():
    # Get the text from the textbox
    text = Output.get() 
    # Copy the text to the clipboard
    pyperclip.copy(text)
    # Show a message box to confirm that the text has been copied
    messagebox.showinfo("Success", "Text copied to clipboard")

wn = Tk()
wn.geometry("500x500")
wn.configure(bg='azure2')
wn.title("Encrypt & Decryption Program")

Message = StringVar()
key = StringVar()
mode = IntVar()
Output = StringVar()

headingFrame1 = Frame(wn,bg="gray91",bd=5)
headingFrame1.place(relx=0.2,rely=0.1,relwidth=0.7,relheight=0.16)

headingLabel = Label(headingFrame1, text=" Welcome to \nEncryption and Decryption \nby Ishan Kapadia", fg='grey19', font=('Courier',13,'bold')) 
headingLabel.place(relx=0,rely=0, relwidth=1, relheight=1)

label1 = Label(wn, text='Enter the Message', font=('Courier',10))
label1.place(x=10,y=250)

msg = Entry(wn, textvariable=Message, width=35, font=('calibre',10,'normal'))
msg.place(x=200,y=250)

label2 = Label(wn, text='Enter the password', font=('Courier',10))
label2.place(x=10,y=300)

InpKey = Entry(wn, textvariable=key, width=35, font=('calibre',10,'normal'), show="*")
InpKey.place(x=200,y=300)

label4 = Label(wn, text='Do you want to...', font=('Courier',10))
label4.place(x=10, y=200)

Radiobutton(wn, text='Encrypt', variable=mode, value=1).place(x=200,y=200) 
Radiobutton(wn, text='Decrypt', variable=mode, value=2).place(x=300,y=200) 

label3 = Label(wn, text='Result', font=('Courier',10))
label3.place(x=10,y=350)

res = Entry(wn,textvariable=Output, width=35, font=('calibre',10,'normal'))
res.place(x=200,y=350)

ShowBtn = Button(wn, text="Show Message", bg='honeydew2', fg='black', width=15, height=1, command=Result)
ShowBtn['font'] = font.Font(size=12)
ShowBtn.place(x=180,y= 450)

ResetBtn = Button(wn, text='Reset', bg='old lace', fg='black', width=15,height=1,command=Reset)
ResetBtn['font'] = font.Font( size=12)
ResetBtn.place(x=15,y= 450)

QuitBtn = Button(wn, text='Exit', bg='lavender blush2', fg='black',width=15,height=1, command=wn.destroy)
QuitBtn['font'] = font.Font( size=12)
QuitBtn.place(x=345,y= 450)

# Create a button to copy text to the clipboard
copy_button = Button(wn, text="Copy to Clipboard", command=copy_to_clipboard)
copy_button['font'] = font.Font(size=12)
copy_button.place(x=180,y= 380)

wn.mainloop()