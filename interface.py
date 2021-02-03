import tkinter as tk
from commands import copy_phrase, save_entry


#Configurable settings
INITIAL_SIZE = '600x250'
LANGUAGE = 'French'

french_dict = {
    'keywords':'Mots clés',
    'phrase':'Extrait',
    'copy':'Copier',
    'save':'Ajouter'
}
english_dict = {
    'keywords':'Keywords',
    'phrase':'Selection',
    'copy':'Copy',
    'save':'Save'
}
language_dict = {
    'French':french_dict,
    'English':english_dict
}

root = tk.Tk()

frame_main = tk.Frame(
    master=root,
    bg='#EEEEEE'
)

root.option_add('tearOff', tk.FALSE) #For modern menus

win = tk.Toplevel(root)
menubar = tk.Menu(win)
menu_options = tk.Menu(menubar)
def temp():
    pass
menu_options.add_command(label='Temp', command=temp)
menu_options.add_command(label='Temp 2', command=temp)
menu_options.add_command(label='Temp 3', command=temp)
menu_options.add_command(label='Temp 4', command=temp)
menubar.add_cascade(menu=menu_options, label='Options')
win['menu'] = menubar


label_keywords = tk.Label(
    master=frame_main,
    text=language_dict[LANGUAGE]['keywords'],
    bg='#EEEEEE'
)
entry_keywords = tk.Entry(
    master=frame_main,
    relief=tk.RIDGE,
    borderwidth=2,
    highlightbackground='#EEEEEE'
    #bg='BLUE'
)

label_phrase = tk.Label(
    master=frame_main,
    text=language_dict[LANGUAGE]['phrase'],
    bg='#EEEEEE'
)
text_phrase = tk.Text(
    master=frame_main,
    relief=tk.RIDGE,
    borderwidth=2,
    highlightbackground='#EEEEEE'
    #bg='GREEN'
)

button_save = tk.Button(
    master=frame_main,
    command=lambda: save_entry(root, entry_keywords, text_phrase),
    text=language_dict[LANGUAGE]['save'],
    relief=tk.RIDGE,
    borderwidth=2,
    fg='BLACK',
    bg='#DDDDDD',
    padx=10,
    pady=5
)
button_copy = tk.Button(
    master=frame_main,
    command=lambda:copy_phrase(root, text_phrase),
    text=language_dict[LANGUAGE]['copy'],
    relief=tk.RIDGE,
    borderwidth=2,
    fg='BLACK',
    bg='#DDDDDD',
    padx=10,
    pady=5
)


label_keywords.grid(
    row=0,
    column=0,
    pady=(10,0)
)
entry_keywords.grid(
    row=0,
    column=1,
    columnspan=2,
    sticky='ew',
    padx=(0,100),
    pady=(10,0)
)
label_phrase.grid(
    row=1,
    column=0
)
text_phrase.grid(
    row=1,
    column=1,
    columnspan=2,
    sticky='nsew',
    padx=(0,20),
    pady=(5,10)
)
button_save.grid(
    row=2,
    column=1,
    sticky='w',
    padx=(20,0),
    pady=(0,15)
)
button_copy.grid(
    row=2,
    column=1,
    sticky='e',
    padx=(0,40),
    pady=(0,15)
)

frame_main.columnconfigure(0, weight=1, pad=10)
frame_main.columnconfigure(1, weight=100, pad=10)
frame_main.rowconfigure(0, weight=0, pad=10)
frame_main.rowconfigure(1, weight=100, pad=10)

frame_main.grid(
    row=0,
    column=0,
    sticky='nsew'
)

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

root.geometry(INITIAL_SIZE) #TODO: Remember user settings
root.minsize(300, 180)
"""
def handle_event(event):
    print(event.__dict__)
    print(event)
    

# Bind keypress event to handle_keypress()
root.bind('<Key>', handle_event)
root.bind('<Button-1>', handle_event)
"""
root.mainloop()
