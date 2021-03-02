import tkinter as tk
from Key import Key

def setup():
    global root
    root = tk.Tk()
    global key
    key = Key(root)
    key.pack()
    root.bind('<KeyPress>', handle_key_press)
    root.bind('<KeyRelease>', handle_key_release)

def handle_key_press(event):
    if event.keysym == 'Tab':
        key.confirm_suggestion()
    else:
        key.ignore_suggestion()
            
def handle_key_release(event):
    key_list = key.get_user_key_list()
    key.autocomplete(testing=True)
    key_list = key.get_display_key_list()
