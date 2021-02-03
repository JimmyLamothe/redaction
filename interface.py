import tkinter as tk

#Configurable settings
INITIAL_SIZE = '700x300'
LANGUAGE = 'French'

french_dict = {
    'keywords':'Mots clés',
    'selection':'Extrait',
    'copy':'Copier',
    'save':'Ajouter'
}
english_dict = {
    'keywords':'Keywords',
    'selection':'Selection',
    'copy':'Copy',
    'save':'Save'
}
language_dict = {
    'French':french_dict,
    'English':english_dict
}

root = tk.Tk()

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
    master=root,
    text=language_dict[LANGUAGE]['keywords'],
    #bg='RED'
)
entry_keywords = tk.Entry(
    master=root,
    relief=tk.RIDGE,
    borderwidth=2,
    #bg='BLUE'
)

label_selection = tk.Label(
    master=root,
    text=language_dict[LANGUAGE]['selection']
    #bg='YELLOW'
)
text_selection = tk.Text(
    master=root,
    relief=tk.RIDGE,
    borderwidth=2
    #bg='GREEN'
)

button_save = tk.Button(
    text=language_dict[LANGUAGE]['save'],
    relief=tk.RIDGE,
    borderwidth=2,
    fg='BLACK',
    bg='#EEEEEE',
    padx=10,
    pady=5
)
button_copy = tk.Button(
    text=language_dict[LANGUAGE]['copy'],
    relief=tk.RIDGE,
    borderwidth=2,
    fg='BLACK',
    bg='#EEEEEE',
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
label_selection.grid(
    row=1,
    column=0
)
text_selection.grid(
    row=1,
    column=1,
    columnspan=2,
    sticky='nsew',
    padx=(0,20),
    pady=(5,10))
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
tk.Frame().grid(row=0, rowspan=3)

root.columnconfigure(0, weight=1, pad=10)
root.columnconfigure(1, weight=100, pad=10)
root.rowconfigure(0, weight=0, pad=10)
root.rowconfigure(1, weight=100, pad=10)

root.geometry(INITIAL_SIZE) #TODO: Remember user settings
root.minsize(300, 180)

root.mainloop()
