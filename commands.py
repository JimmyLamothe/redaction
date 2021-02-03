import tkinter as tk

def copy_phrase(root, text_phrase):
    phrase = text_phrase.get('1.0', tk.END)
    root.clipboard_clear()
    root.clipboard_append(phrase)
    #root.update() #Check what it does

def save_entry(root, entry_keywords, text_phrase):
    print(entry_keywords.get())
    print(text_phrase.get('1.0', tk.END))
