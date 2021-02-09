import tkinter as tk
from PIL import ImageTk, Image
import database as db

import config

class MainFrame(tk.Frame):
    def __init__(self, master):
        self.master = master
        tk.Frame.__init__(
            self,
            master=master,
            bg='#EEEEEE'
        )
        self.key_label = self.create_key_label()
        self.key_entry = self.create_key_entry()
        self.phrase_label = self.create_phrase_label()
        self.phrase_text = self.create_phrase_text()
        if config.config_dict['show_buttons']:
            self.save_button = self.create_save_button()
            self.copy_button = self.create_copy_button()
            self.up_button = self.create_up_button()
            self.down_button = self.create_down_button()
        self.configure_gui()
        self.bind_event_handlers()
        
    def create_key_label(self):
        language_dict = config.get_language_dict()
        label = tk.Label(
            master=self,
            text=language_dict['key'],
            bg='#EEEEEE'
        )
        return label
    
    def create_key_entry(self):
        entry = tk.Entry(
            master=self,
            relief=tk.RIDGE,
            borderwidth=2,
            highlightbackground='#EEEEEE',
            highlightcolor='#EEEEEE'
        )
        return entry

    def create_phrase_label(self):
        language_dict = config.get_language_dict()
        label = tk.Label(
            master=self,
            text=language_dict['phrase'],
            bg='#EEEEEE'
        )
        return label

    def create_phrase_text(self):
        text = tk.Text(
            master=self,
            relief=tk.RIDGE,
            borderwidth=2,
            highlightbackground='#EEEEEE',
            highlightcolor='#EEEEEE' #No border on focus
        )   
        return text

    def create_save_button(self):
        language_dict = config.get_language_dict()
        button = tk.Button(
            master=self,
            command=self.save_entry,
            text=language_dict['save'],
            relief=tk.RIDGE,
            borderwidth=2,
            fg='BLACK',
            bg='#DDDDDD',
            padx=10,
            pady=5
        )
        return button

    def create_copy_button(self):
        language_dict = config.get_language_dict()
        button = tk.Button(
            master=self,
            command=self.copy_phrase,
            text=language_dict['copy'],
            relief=tk.RIDGE,
            borderwidth=2,
            fg='BLACK',
            bg='#DDDDDD',
            padx=10,
            pady=5
        )
        return button

    def create_up_button(self):
        icon = Image.open('icons/noun_chevron up_730241.png')
        icon = icon.resize((20,20), Image.ANTIALIAS)
        icon = ImageTk.PhotoImage(icon)
        self.up_icon = icon
        button = tk.Button(
            master=self,
            command=db.previous_entry,
            image=icon,
            relief=tk.RIDGE,
            borderwidth=2,
            bg='#CCCCCC',
            #height=20,
            #width=20
        )
        return button

    def create_down_button(self):
        icon = Image.open('icons/noun_chevron down_730206.png')
        icon = icon.resize((20,20), Image.ANTIALIAS)
        icon = ImageTk.PhotoImage(icon)
        self.down_icon = icon
        button = tk.Button(
            master=self,
            command=db.next_entry,
            image=icon,
            relief=tk.RIDGE,
            borderwidth=2,
            bg='#CCCCCC',
            #height=20,
            #width=20
        )
        return button
        
    
    def configure_gui(self):
        self.columnconfigure(0, weight=1, pad=10)
        self.columnconfigure(1, weight=100, pad=10)
        self.rowconfigure(0, weight=0, pad=10)
        self.rowconfigure(1, weight=100, pad=10)
        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)
        self.key_label.grid(
            row=0,
            column=0,
            pady=(10,0)
        )
        self.key_entry.grid(
            row=0,
            column=1,
            sticky='ew',
            padx=(0,100),
            pady=(10,0)
        )
        self.phrase_label.grid(
            row=1,
            column=0
        )
        self.phrase_text.grid(
            row=1,
            column=1,
            sticky='nsew',
            padx=(0,20),
            pady=(5,10)
        )
        if config.config_dict['show_buttons']:
            self.save_button.grid(
                row=2,
                column=1,
                sticky='w',
                padx=(20,0),
                pady=(0,15)
            )
            self.copy_button.grid(
                row=2,
                column=1,
                sticky='e',
                padx=(0,40),
                pady=(0,15)
            )
            self.up_button.grid(
                row=1,
                column=2,
                sticky='n',
                padx=(0,15),
                pady=(15,0)
            )
            self.down_button.grid(
                row=1,
                column=2,
                sticky='s',
                padx=(0,15),
                pady=(0,15)
            )
        self.grid(
            row=0,
            column=0,
            sticky='nsew'
        )

    def copy_phrase(self):
        phrase = self.phrase_text.get('1.0', tk.END)
        self.master.clipboard_clear()
        self.master.clipboard_append(phrase)
        
    def save_entry(self):
        key_list = self.key_entry.get().split(' ')
        print(self.key_entry.get())
        phrase = self.phrase_text.get('1.0', tk.END)
        print(self.phrase_text.get('1.0', tk.END))
        db.save_entry(phrase, key_list)
        print(db.key_df)
        print(db.phrase_series)
        
    def handle_key_input(self, event):
        print(event.char)

    def handle_phrase_input(self, event):
        print(event.char)
        
    def bind_event_handlers(self):
        self.key_entry.bind('<KeyPress>', self.handle_key_input)
        self.phrase_text.bind('<KeyPress>', self.handle_phrase_input)
