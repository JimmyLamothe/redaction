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
        self.delete_keysyms = ['Delete','KP_Delete','BackSpace']
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

    def block_key_new_line(self, event):
        """ Prevent new lines in key text widget | None -> str """
        return('break') #Interrupt standard tkinter event processing
        
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

    def handle_key_button_release(self, event):
        """ Button release manager for key widget | tk.Event -> None """
        if self.key.suggestion_text: #If suggestion displayed
            if self.key.cursor_moved() == 'LEFT': #If cursor moved left
                self.key.ignore_suggestion() #Delete suggestion text
            elif self.key.cursor_moved() == 'RIGHT': #If cursor moved right
                #Confirm suggestion up to cursor position
                self.key.confirm_suggestion(cursor=self.key.get_cursor())

    def debug(self, number):
        print('')
        print(number)
        print(f'current_text = {self.key.current_text}')
        print(f'current_cursor = {self.key.current_cursor}')
        print(f'display_text = {self.key.get_contents()}')
        print(f'display_cursor = {self.key.get_cursor()}')
        print(f'suggestion_text = {self.key.suggestion_text}')
        print(f'suggestion_list = {self.key.suggestion_list}')
        
    def handle_key_key_release(self, event):
        """ Key release manager for key widget | tk.Event -> None """
        if event.keysym in self.delete_keysyms: #If input was a delete character:
            self.debug(1)
            if self.key.suggestion_text:
                self.key.ignore_suggestion() #Delete suggestion text
            self.key.update_current() #Update current user text
            self.debug(1.0)
        elif not self.key.suggestion_text: #If no suggestion displayed
            self.debug(2)
            if self.key.text_changed(): #If input received
                self.debug(2.1)
                self.key.update_current()
                if self.key.cursor_at_end(): #If cursor at end
                    self.debug(2.11)
                    self.key.autocomplete() #Get suggestion
            self.debug(2.0)
        elif not self.key.text_changed(): #If no new input char
            self.debug(3)
            if self.key.cursor_moved() == 'LEFT': #If cursor moved left
                self.debug(3.1)
                self.key.ignore_suggestion() #Delete suggestion text
            elif self.key.cursor_moved() == 'RIGHT': #If cursor moved right
                self.debug(3.2)
                #Confirm suggestion up to cursor position
                self.key.confirm_suggestion(cursor=self.key.get_cursor())
            self.key.update_current()
            self.debug(3.0)
        else: #If suggestion active and text changed
            self.debug(4)
            current_input = self.key.get_difference() #Get new user input
            self.key.update_current()
            print(f'current_input = {current_input}')
            print(f'len(current_input) = {len(current_input)}')
            if not len(current_input) == 1: #If user input more than one char
                self.debug(4.1)
                self.key.ignore_suggestion() #Delete suggestion text
                #self.key.update_current()
            #If input char was next char in suggestion
            elif current_input == self.key.suggestion_text[0]:
                self.debug(4.2)
                #Confirm suggestion up to cursor
                self.key.suggestion_text = self.key.suggestion_text[1:]
                self.key.confirm_suggestion(self.key.current_cursor) 
                #self.key.update_current() 
            else:
                self.debug(4.3)
                self.key.ignore_suggestion() #Delete suggestion text
                #self.key.update_current()
                self.key.autocomplete() #Get suggestion
            self.debug(4.0)
        self.autocomplete()
        
    def autocomplete(self):
        key_list = self.key.get_display_key_list() #Includes suggestion if any
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
        self.key.bind('<Return>', self.block_key_new_line)
        self.key.bind('<Tab>', self.handle_key_tab)
        self.key.bind('<BackSpace>', self.handle_key_backspace)
        self.key.bind('<KeyRelease>', self.handle_key_key_release)
        self.key.bind('<ButtonRelease>', self.handle_key_button_release)
        #Phrase bindings - active when focus on Phrase text widget
        self.phrase.bind('<Tab>', self.handle_phrase_tab)
        self.phrase.bind('<BackSpace>', self.handle_phrase_backspace)
        #self.phrase.bind('<KeyRelease>', self.handle_phrase_input)
