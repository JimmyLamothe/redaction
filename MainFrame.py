""" Implements the MainFrame class 

Classes: MainFrame
"""

import tkinter as tk
from PIL import ImageTk, Image
from Key import Key
from Phrase import Phrase
import config
import database as db

class MainFrame(tk.Frame):
    """ Implements the widget interface and logic.

    Displays a Key object and a Phrase object with their own internal logic,
    and four optional buttons.
    
    Implements user-input logic not specific to the Key or Phrase object.
    
    Handles widget keyboard and mouse events.

    Args:
        master (tk.Tk): Root object inheriting from tk.Tk

    Methods:
        create_key_label() -> tk.Label
        create_phrase_label() -> tk.Label
        create_copy_button() -> tk.Button
        create_save_button() -> tk.Button
        create_up_button() -> tk.Button
        create_down_button() -> tk.Button
        configure_gui()
        copy_phrase()
        save_entry()
        handle_key_tab(tk.Event) -> str
        handle_phrase_tab(tk.Event) -> str
        handle_key_backspace(tk.Event) -> str
        handle_phrase_backspace(tk.Event) -> str
        handle_key_release(tk.Event)
        handle_phrase_input(tk.Event) - NOT IMPLEMENTED
        bind_event_handlers()
    """
    def __init__(self, master):
        self.master = master
        tk.Frame.__init__(
            self,
            master=master,
            bg='#EEEEEE' #Background color
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
        
    def create_key_label(self):
        """ Creates a label for the key entry widget | None -> tk.Label """
        language_dict = config.get_language_dict() #Active language name dict
        label = tk.Label(
            master=self,
            text=language_dict['key'],
            bg='#EEEEEE'
        )
        return label
    
    def create_phrase_label(self):
        """ Creates a label for the phrase text widget | None -> tk.Label """
        language_dict = config.get_language_dict() #Active language name dict
        label = tk.Label(
            master=self,
            text=language_dict['phrase'],
            bg='#EEEEEE'
        )
        return label

    def create_copy_button(self):
        """ Creates a copy button | None -> tk.Button """
        language_dict = config.get_language_dict() #Active language name dict
        button = tk.Button(
            master=self,
            command=self.copy_phrase, #Copies active phrase to clipboard
            text=language_dict['copy'],
            relief=tk.RIDGE,
            borderwidth=2,
            fg='BLACK',
            bg='#DDDDDD',
            padx=10,
            pady=5
        )
        return button
    
    def create_save_button(self):
        """ Creates a save button | None -> tk.Button """
        language_dict = config.get_language_dict() #Active language name dict
        button = tk.Button(
            master=self,
            command=self.save_entry, #Saves active key/phrase combination to db
            text=language_dict['save'],
            relief=tk.RIDGE,
            borderwidth=2,
            fg='BLACK',
            bg='#DDDDDD',
            padx=10,
            pady=5
        )
        return button
    
    def create_up_button(self):
        """ Creates previous phrase button | None -> tk.Button """
        icon = Image.open('icons/noun_chevron up_730241.png')
        icon = icon.resize((20,20), Image.ANTIALIAS)
        icon = ImageTk.PhotoImage(icon)
        self.up_icon = icon
        button = tk.Button(
            master=self,
            command=self.phrase.previous, #Displays previous phrase
            image=icon,
            relief=tk.RIDGE,
            borderwidth=2,
            bg='#CCCCCC',
        )
        return button

    def create_down_button(self):
        """ Creates next phrase button | None -> tk.Button """
        icon = Image.open('icons/noun_chevron down_730206.png')
        icon = icon.resize((20,20), Image.ANTIALIAS)
        icon = ImageTk.PhotoImage(icon)
        self.down_icon = icon
        button = tk.Button(
            master=self,
            command=self.phrase.next, #Displays next phrase
            image=icon,
            relief=tk.RIDGE,
            borderwidth=2,
            bg='#CCCCCC',
        )
        return button
            
    def configure_gui(self):
        """ Configures tkinter GUI | None -> None """
        #Define rows and columns
        self.columnconfigure(0, weight=1, pad=10)
        self.columnconfigure(1, weight=100, pad=10)
        self.rowconfigure(0, weight=0, pad=10)
        self.rowconfigure(1, weight=100, pad=10)
        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)
        #Place widgets
        self.key_label.grid(
            row=0,
            column=0,
            pady=(10,0)
        )
        self.key.grid(
            row=0,
            column=1,
            sticky='ew', #Stretches horizontally with window
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
            sticky='nsew', #Stretches with window
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
        #Place self in Root object
        self.grid(
            row=0,
            column=0,
            sticky='nsew' #Stretches with window
        )
        
    def copy_phrase(self):
        """ Copy phrase text widget contents to clipboard | None -> None """ 
        phrase = self.phrase.get_contents()
        self.master.clipboard_clear()
        self.master.clipboard_append(phrase)
        
    def save_entry(self):
        """ Save active key/phrase combination to db | None -> None """
        #Get key and phrase
        key_list = self.key.get_display_key_list()
        print(key_list)
        phrase = self.phrase.get_contents()
        print(phrase)
        #Save combination
        db.save_entry(key_list, phrase)
        print(db.key_df)
        #Clear widgets after save
        self.phrase.clear()
        self.key.clear()
        
    def handle_key_tab(self, event):
        """ Handle tab keypress in Key entry widget | None -> str """
        if self.key.confirm_suggestion():
            return('break') #Interrupt standard tkinter event processing

    def handle_phrase_tab(self, event):
        """ Handle tab keypress in Phrase text widget | None -> str """
        self.key.focus()
        return('break') #Interrupt standard tkinter event processing

    def handle_key_backspace(self, event):
        """ Handles Backspace + modifier in Key widget | tk.Event -> str """
        if event.state in [1,4,8,16]: #If any key modifier + backspace
            self.key.delete_word() #Delete previous word in Key widget
            return 'break' #Interrupt standard tkinter event processing
        
    def handle_phrase_backspace(self, event):
        """ Handles Backspace + modifier in Phrase widget | tk.Event -> str """
        if event.state in [1,4,8,16]: #If any key modifier + backspace
            self.phrase.delete_word() #Delete previous word in Key widget
            return 'break' #Interrupt standard tkinter event processing
    
    def handle_key_release(self, event):
        """ Keypress manager | tk.Event -> None """
        delete_keysyms = ['Delete','KP_Delete','BackSpace']
        print(event.keysym)
        if self.key.compare_states(): #If user typed next letter in autocomplete:
            self.key.ignore_suggestion() #Delete the autocomplete from display
        elif event.char == '': #If keypress was not a character input:
            return #Ignore
        elif event.keysym in delete_keysyms: #If keypress was a delete character:
            self.key.ignore_suggestion() #Delete the autocomplete from display
            return
        key_list = self.key.get_display_key_list() #Get input from Key widget
        self.key.autocomplete() #Autocomplete with top ranked key from database
        key_list = self.key.get_display_key_list() #Get autocompleted input
        success = self.phrase.display_phrase(key_list) #Display top valid phrase
        if not success: #If no valid phrase with autocompleted Key input:
            self.phrase.clear() #Clear phrase display
     
    def handle_phrase_input(self, event):
        """ To be implemented - only prints input for now | tk.Event -> None """
        print(event.char)
        
    def bind_event_handlers(self):
        """ Binds all event handlers for all widgets | None -> None """
        #Copy and save bindings - active in all focus states
        self.master.bind('<Control-c>', lambda event: self.copy_phrase())
        self.master.bind('<Command-c>', lambda event: self.copy_phrase())
        self.master.bind('<Control-s>', lambda event: self.save_entry())
        self.master.bind('<Command-s>', lambda event: self.save_entry())
        #Key bindings - active when focus on Key entry widget
        self.key.bind('<Tab>', self.handle_key_tab)
        self.key.bind('<BackSpace>', self.handle_key_backspace)
        self.key.bind('<KeyRelease>', self.handle_key_release)
        #Phrase bindings - active when focus on Phrase text widget
        self.phrase.bind('<Tab>', self.handle_phrase_tab)
        self.phrase.bind('<BackSpace>', self.handle_phrase_backspace)
        #self.phrase.bind('<KeyRelease>', self.handle_phrase_input)
