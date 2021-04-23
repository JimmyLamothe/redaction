""" Implements the MainFrame class

Classes: MainFrame
"""

import tkinter as tk
from PIL import ImageTk, Image
from Key import Key
from Phrase import Phrase
import config

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
        self.db = config.active_objects['db']
        self.key_label = self.create_key_label()
        self.key = Key(self)
        self.phrase_label = self.create_phrase_label()
        self.phrase = Phrase(self)
        if config.get_show_buttons():
            print('creating buttons')
            self.left_button = self.create_left_button()
            self.right_button = self.create_right_button()
            self.up_button = self.create_up_button()
            self.down_button = self.create_down_button()
        self.activate_get_mode()
        self.configure_gui()
        self.bind_event_handlers()
        if config.get_show_tutorial():
            self.load_tutorial()
        
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

    def create_left_button(self):
        """ Creates button on left of app window| None -> tk.Button """
        language_dict = config.get_language_dict() #Active language name dict
        button = tk.Button(
            master=self,
            command=config.change_mode,
            text=language_dict['new'], #Changes with config.change_mode
            relief=tk.RIDGE,
            borderwidth=2,
            fg='BLACK',
            bg='#DDDDDD',
            padx=10,
            pady=5
        )
        return button

    def create_right_button(self):
        """ Creates button on right of app window | None -> tk.Button """
        language_dict = config.get_language_dict() #Active language name dict
        button = tk.Button(
            master=self,
            command=self.copy_phrase, #Changes with config.change_mode
            text=language_dict['copy'], #Changes with config.change_mode
            relief=tk.RIDGE,
            borderwidth=2,
            fg='BLACK',
            bg='#DDDDDD',
            padx=10,
            pady=5
        )
        return button
    
    def activate_get_mode(self):
        """ Sets app to get entry from database | None -> None """
        if config.get_mode() == 'get':
            return
        language_dict = config.get_language_dict()
        for item in [self, self.key_label, self.phrase_label]:
            item.config(bg='#EEEEEE')
        self.phrase.config(
            bg='#F5F5F5',
            borderwidth=3
            )
        if config.get_show_buttons():
            self.left_button.config(
                text=language_dict['new'],
            )
            self.right_button.config(
                text=language_dict['copy'],
                command=self.copy_phrase
            )
        self.key.focus()
        self.key.full_clear()
        self.phrase.full_clear()
        config.set_mode('get')

    def activate_put_mode(self):
        """ Sets app to save entry to database | None -> None """
        if config.get_mode() == 'put':
            return
        language_dict = config.get_language_dict()
        for item in [self, self.key_label, self.phrase_label]:
            item.config(bg='#F5FCFF')
        self.phrase.config(
            bg='#FFFFFF',
            borderwidth=2
            )
        if config.get_show_buttons():
            self.left_button.config(
                text=language_dict['cancel'],
            )
            self.right_button.config(
                text=language_dict['save'],
                command=self.save_entry
            )
        self.phrase.focus()
        self.key.ignore_suggestion()
        self.phrase.full_clear()
        config.set_mode('put')
    
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

    def set_text(self, language_dict):
        """ Sets text of all widgets to config settings | None -> None """
        self.key_label.config(text=language_dict['key'])
        self.phrase_label.config(text=language_dict['phrase'])
        if config.get_mode() == 'get':
            self.left_button.config(text=language_dict['new'])
            self.right_button.config(text=language_dict['copy'])
        else:
            self.left_button.config(text=language_dict['cancel'])
            self.right_button.config(text=language_dict['save'])
    
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
        if config.get_show_buttons():
            self.left_button.grid(
                row=2,
                column=1,
                sticky='w',
                padx=(20,0),
                pady=(0,15)
            )
            self.right_button.grid(
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
        self.key.focus() #Focus on key widget
        
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
        self.db.prepare_undo()
        self.db.save_entry(key_list, phrase)
        print(self.db)
        #Clear widgets after save
        self.phrase.full_clear()
        self.key.full_clear()

    def block_key_new_line(self, event):
        """ Prevent new lines in key text widget | None -> str """
        print('blocking new line')
        return 'break' #Interrupt standard tkinter event processing
        
    def handle_key_tab(self, event):
        """ Handle tab keypress in Key text widget | None -> str """
        if config.get_mode() == 'put':
            if not self.key.suggestion_text:
                self.phrase.focus()
                return 'break'
        self.key.handle_tab(event)
        return 'break' #Interrupt standard tkinter event processing
    
    def handle_phrase_tab(self, event):
        """ Handle tab keypress in Phrase text widget | None -> str """
        if config.get_mode() == 'put':
            if not self.phrase.suggestion_text:
                self.key.focus()
                return 'break'
        self.phrase.handle_tab(event)
        return 'break' #Interrupt standard tkinter event processing

    def handle_key_backspace(self, event):
        """ Handles Backspace + modifier in Key widget | tk.Event -> str """
        return self.key.handle_backspace(event) #Returns None or 'break'
        
    def handle_phrase_backspace(self, event):
        """ Handles Backspace + modifier in Phrase widget | tk.Event -> str """
        return self.phrase.handle_backspace(event) #Returns None or 'break'

    def handle_key_button_release(self, event):
        """ Button release manager for key widget | tk.Event -> None 
        
        When in put mode, switch to get mode if both fields are empty.
        When in put mode, confirm suggestion before switching focus to key
        """
        self.clear_hints() #Clear hints if active and activate get mode
        key_contents = self.key.get_contents()
        phrase_contents = self.phrase.get_contents()
        if config.get_mode() == 'put':
            self.phrase.confirm_suggestion()
            if key_contents == '' == phrase_contents:
                    self.activate_get_mode() #Switch to get mode
        self.key.handle_button_release(event)
        
    def handle_phrase_button_release(self, event):
        self.clear_hints() #Clear hints if active and activate get mode
        if self.phrase.get_selection(): #If user selected text in phrase box
            self.key.confirm_suggestion()
            return
        elif not config.get_mode() == 'put':
            self.activate_put_mode()
            return
        else:
            self.phrase.handle_button_release(event)

    def debug(self, number):
        if not config.get_debug():
            return
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
        #No autocomplete for key widget in put mode
        if not config.get_mode() == 'put':
            self.key_autocomplete(event)
        else:
            self.key.current_text = self.key.get_contents()

    def handle_phrase_key_release(self, event):
        """ Autocomplete phrase and display related keys | tk.Event -> None
        
        If key field is not empty, do not autocomplete to avoid deleting
        user input
        """
        if not self.key.current_text: #If no user input in key field
            self.phrase_autocomplete(event)
    
    def key_autocomplete(self, event):
        """ Autocomplete key and suggest phrase | tk.Event -> None """
        self.key.autocomplete(event)
        self.suggest_phrase()
        
    def phrase_autocomplete(self, event):
        """ Autocomplete phrase and get saved keys | tk.Event -> None """
        self.phrase.autocomplete(event)
        saved_keys = self.phrase.get_saved_keys()
        self.key.set_contents(saved_keys)
        if saved_keys:
            print('saved keys:' , saved_keys)
            self.phrase.ignore_suggestion()
        else:
            print('no saved keys')
            self.key.full_clear()
            self.phrase.autocomplete(event)
        
    def suggest_phrase(self):
        key_list = self.key.get_display_key_list() #Includes suggestion if any
        success = self.phrase.display_phrase(key_list) #Display top valid phrase
        if not success: #If no valid phrase with autocompleted Key input:
            self.phrase.full_clear() #Clear phrase display

    def display_hint(self, event):
        """ NOT IMPLEMENTED """
        pass

    def load_tutorial(self):
        config.set_mode('hint')
        config.decrement_tutorial()
        self.focus()
        language_dict = config.get_language_dict()
        with open(language_dict['tutorial'], 'r') as source:
            tutorial = source.read().split('***\n')
            self.phrase.active_list = tutorial
            self.phrase.active_list_index = 0
            self.phrase.display_current()

    def clear_hints(self):
        print(f'clear hints if {config.get_mode() == "hint"}')
        if config.get_mode() == 'hint':
            self.activate_get_mode()

    def print_tracker_variables(self):
        print('Key variables:')
        print(f'Key - current_text: {self.key.current_text}')
        print(f'Key - current_text: {self.key.suggestion_text}')
        print(f'Key - current_text: {self.key.suggestion_list}')
        print(f'Key - current_text: {self.key.current_cursor}')
        print(f'Phrase - current_text: {self.phrase.current_text}')
        print(f'Phrase - current_text: {self.phrase.suggestion_text}')
        print(f'Phrase - current_text: {self.phrase.suggestion_list}')
        print(f'Phrase - current_text: {self.phrase.current_cursor}')
            
    def bind_event_handlers(self):
        """ Binds all event handlers for all widgets | None -> None """
        #Copy and save bindings - active in all focus states
        self.master.bind('<Control-c>', lambda event: self.copy_phrase())
        self.master.bind('<Command-c>', lambda event: self.copy_phrase())
        self.master.bind('<Control-s>', lambda event: self.save_entry())
        self.master.bind('<Command-s>', lambda event: self.save_entry())
        self.master.bind('<Command-z>', lambda event: self.db.undo())
        self.master.bind('<Control-z>', lambda event: self.db.undo())
        self.master.bind('<Control-y>', lambda event: self.db.redo())
        self.master.bind('<Command-y>', lambda event: self.db.redo())
        self.master.bind('<Control-Shift-z>', lambda event: self.db.redo())
        self.master.bind('<Command-Shift-z>', lambda event: self.db.redo())
        self.master.bind('<Escape>', lambda event: config.change_mode())
        self.master.bind('<Up>', lambda event: self.phrase.previous())
        self.master.bind('<Down>', lambda event: self.phrase.next())
        #Key bindings - active when focus on Key entry widget
        self.key.bind('<Return>', self.block_key_new_line)
        self.key.bind('<Tab>', self.handle_key_tab)
        self.key.bind('<BackSpace>', self.handle_key_backspace)
        self.key.bind('<KeyRelease>', self.handle_key_key_release)
        self.key.bind('<ButtonRelease>', self.handle_key_button_release)
        #Phrase bindings - active when focus on Phrase text widget
        self.phrase.bind('<Tab>', self.handle_phrase_tab)
        self.phrase.bind('<BackSpace>', self.handle_phrase_backspace)
        self.phrase.bind('<ButtonRelease>', self.handle_phrase_button_release)
        self.phrase.bind('<KeyRelease>', self.handle_phrase_key_release)
