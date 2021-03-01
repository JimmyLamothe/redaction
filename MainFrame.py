import tkinter as tk
from PIL import ImageTk, Image
from Key import Key
from Phrase import Phrase
import config
if config.config_dict['db'] == 'def':
    import database as db
else:
    import database_alt as db

class MainFrame(tk.Frame):
    def __init__(self, master):
        self.master = master
        tk.Frame.__init__(
            self,
            master=master,
            bg='#EEEEEE'
        )
        self.key_label = self.create_key_label()
        self.key = Key(self)
        self.phrase_label = self.create_phrase_label()
        self.phrase = Phrase(self)
        if config.config_dict['show_buttons']:
            self.save_button = self.create_save_button()
            self.copy_button = self.create_copy_button()
            self.up_button = self.create_up_button()
            self.down_button = self.create_down_button()
        self.configure_gui()
        self.bind_event_handlers()
        self.active_phrase_list = None
        self.current_index = None
        
    def create_key_label(self):
        language_dict = config.get_language_dict()
        label = tk.Label(
            master=self,
            text=language_dict['key'],
            bg='#EEEEEE'
        )
        return label
    
    def create_phrase_label(self):
        language_dict = config.get_language_dict()
        label = tk.Label(
            master=self,
            text=language_dict['phrase'],
            bg='#EEEEEE'
        )
        return label

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
            command=self.phrase.previous,
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
            command=self.phrase.next,
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
        self.key.grid(
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
        self.phrase.grid(
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
        
    def switch_focus(self):
        print('Switch focus not implementend')
        
    def copy_phrase(self):
        phrase = self.phrase.get_contents()
        self.master.clipboard_clear()
        self.master.clipboard_append(phrase)
        
    def save_entry(self):
        key_list = self.key.get_display_key_list()
        print(key_list)
        phrase = self.phrase.get_contents()
        print(phrase)
        db.save_entry(key_list, phrase)
        print(db.key_df)
        #print(db.phrase_series)
        self.phrase.clear()
        self.key.clear()
        
    def handle_key_tab(self, event):
        if self.key.confirm_suggestion():
            return('break')

    def handle_phrase_tab(self, event):
        self.key.focus()
        return('break')
        
    def handle_key_release(self, event):
        delete_keysyms = ['Delete','KP_Delete','BackSpace']
        print(event.keysym)
        if self.key.compare_states():
            self.key.ignore_suggestion()
        elif event.char == '':
            return
        elif event.keysym in delete_keysyms:
            self.key.ignore_suggestion()
            return
        key_list = self.key.get_display_key_list()
        success = self.phrase.display_phrase(key_list)
        self.key.autocomplete()
        key_list = self.key.get_display_key_list()
        if not success:
            self.phrase.display_phrase(key_list)

    def handle_key_backspace(self, event):
        if event.state in [1,4,8,16]:
            self.key.delete_word()
            return 'break'
        
    def handle_phrase_backspace(self, event):
        if event.state in [1,4,8,16]:
            self.phrase.delete_word()
            return 'break'
    
    def handle_phrase_input(self, event):
        print(event.char)
        
    def bind_event_handlers(self):
        self.master.bind('<Control-c>', lambda event: self.copy_phrase())
        self.master.bind('<Command-c>', lambda event: self.copy_phrase())
        self.master.bind('<Control-s>', lambda event: self.save_entry())
        self.master.bind('<Command-s>', lambda event: self.save_entry())
        self.key.bind('<Tab>', self.handle_key_tab)
        self.key.bind('<BackSpace>', self.handle_key_backspace)
        self.key.bind('<KeyRelease>', self.handle_key_release)
        self.phrase.bind('<Tab>', self.handle_phrase_tab)
        self.phrase.bind('<BackSpace>', self.handle_phrase_backspace)
        #self.phrase.bind('<KeyRelease>', self.handle_phrase_input)
