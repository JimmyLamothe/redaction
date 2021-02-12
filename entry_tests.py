import tkinter as tk
from Key import Key

def setup():
    global root
    root = tk.Tk()
    global key
    key = Key(root)
    key.pack()
