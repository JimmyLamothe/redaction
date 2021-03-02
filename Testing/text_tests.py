import tkinter as tk
from Phrase import Phrase

def setup():
    global root
    root = tk.Tk()
    global phrase
    phrase = Phrase(root)
    phrase.pack()
