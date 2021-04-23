""" Implements the TranslationMainFrame class

Classes: TranslationMainFrame
"""

import tkinter as tk
from PIL import ImageTk, Image
from Phrase import Language1, Language2
import config

class TranslationMainFrame(tk.Frame):
    """ Implements the widget interface and logic.

    Displays a lang1 and lang 2 text widget with their own internal logic,
    and four optional buttons.
    
    Implements user-input logic not specific to the lang1 and lang 2 widgets.
    
    Handles keyboard and mouse events.

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
        copy()
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
        self.lang1_label = self.create_lang1_label()
        self.lang1 = Language1(self)
        self.lang2_label = self.create_lang2_label()
        self.lang2 = Language2(self)
        if config.get_show_buttons():
            print('creating buttons')
            self.left_button = self.create_left_button()
            self.right_button = self.create_right_button()
            self.up_button = self.create_up_button()
            self.down_button = self.create_down_button()
        self.configure_gui()
        self.bind_event_handlers()
        
    def create_lang1_label(self):
        """ Creates a label for the lang1 text widget | None -> tk.Label """
        label = tk.Label(
            master=self,
            text=config.get_lang1(),
            bg='#EEEEEE'
        )
        return label
    
    def create_lang2_label(self):
        """ Creates a label for the lang2 text widget | None -> tk.Label """
        label = tk.Label(
            master=self,
            text=config.get_lang2(),
            bg='#EEEEEE'
        )
        return label

    def create_left_button(self):
        """ Creates button on left of app window| None -> tk.Button """
        language_dict = config.get_language_dict() #Active language name dict
        button = tk.Button(
            master=self,
            command=self.save_entry, #TO BE DETERMINED
            text=language_dict['save'], #TO BE DETERMINED
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
            command=self.copy, #TO BE DETERMINED
            text=language_dict['copy'], #TO BE DETERMINED
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
            command=self.previous_match, #Displays previous phrase
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
            command=self.next_match, #Displays next phrase
            image=icon,
            relief=tk.RIDGE,
            borderwidth=2,
            bg='#CCCCCC',
        )
        return button

    def set_text(self, language_dict):
        """ Sets text of all widgets to config settings | None -> None """
        self.lang1_label.config(text=language_dict['language_pair'][0])
        self.lang2_label.config(text=language_dict['language_pair'][1])
        self.left_button.config(text=language_dict['save'])
        self.right_button.config(text=language_dict['copy'])
    
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
        self.lang1_label.grid(
            row=0,
            column=0,
            pady=(10,0)
        )
        self.lang1.grid(
            row=0,
            column=1,
            sticky='ew', #Stretches horizontally with window
            padx=(0,20),
            pady=(10,0)
        )
        self.lang2_label.grid(
            row=1,
            column=0,
            sticky='n',
            pady=(10,0)
        )
        self.lang2.grid(
            row=1,
            column=1,
            sticky='new', #Stretches horizontally with window
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
                row=0,
                column=2,
                sticky='s',
                padx=(0,15),
                pady=(30,0)
            )
            self.down_button.grid(
                row=1,
                column=2,
                sticky='n',
                padx=(0,15),
                pady=(30,0)
            )
        #Place self in Root object
        self.grid(
            row=0,
            column=0,
            sticky='nsew' #Stretches with window
        )
        self.lang1.focus() #Focus on key widget

    def get_active_lang(self):
        if self.lang2.active_list:
            return self.lang2
        elif self.lang1.active_list:
            return self.lang1
        return None

    def next_match(self):
        active_lang = self.get_active_lang()
        if active_lang:
            active_lang.next()

    def previous_match(self):
        active_lang = self.get_active_lang()
        if active_lang:
            active_lang.previous()
    
    def copy(self):
        """ Copy active translation to clipboard | None -> None """
        active_lang = self.get_active_lang()
        if active_lang:
            translation = active_lang.get_contents()
        else:
            translation = None
        if translation:
            self.master.clipboard_clear()
            self.master.clipboard_append(translation)
        
    def save_entry(self):
        """ Save active key/phrase combination to db | None -> None """
        #Get key and phrase
        lang1_key = self.lang1.get_contents()
        print(lang1_key)
        lang2_key = self.lang2.get_contents()
        print(lang2_key)
        #Save combination
        self.db.prepare_undo()
        self.db.save_entry(lang1_key, lang2_key)
        print(self.db)
        #Clear widgets after save
        self.lang1.full_clear()
        self.lang2.full_clear()

    def block_new_line(self, event):
        """ Prevent new lines in lang1 and lang 2 text widgets | None -> str """
        print('blocking new line')
        return 'break' #Interrupt standard tkinter event processing
        
    def handle_lang1_tab(self, event):
        """ Handle tab keypress in lang1 text widget | None -> str """
        if self.lang1.suggestion_text:
            self.lang1.handle_tab(event)
            return 'break' 
        self.lang2.focus()
        return 'break' #Interrupt standard tkinter event processing
    
    def handle_lang2_tab(self, event):
        """ Handle tab keypress in lang2 text widget | None -> str """
        if self.lang2.suggestion_text:
            self.lang2.handle_tab(event)
            return 'break' 
        self.lang1.focus()
        return 'break' #Interrupt standard tkinter event processing

    def handle_lang1_backspace(self, event):
        """ Handles Backspace + modifier in lang1 widget | tk.Event -> str """
        return self.lang1.handle_backspace(event) #Returns None or 'break'
        
    def handle_lang2_backspace(self, event):
        """ Handles Backspace + modifier in lang2 widget | tk.Event -> str """
        return self.lang2.handle_backspace(event) #Returns None or 'break'

    def handle_lang1_button_release(self, event):
        """ Button release manager for lang1 widget | tk.Event -> None """
        if self.lang1.get_selection(): #If user selected text in lang1 box
            self.lang2.confirm_suggestion()
            return
        self.lang1.handle_button_release(event)
        
    def handle_lang2_button_release(self, event):
        if self.lang2.get_selection(): #If user selected text in lang2 box
            self.lang1.confirm_suggestion()
            return
        self.lang2.handle_button_release(event)

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
        
    def handle_lang1_key_release(self, event):
        """ Key release manager for key widget | tk.Event -> None """
        #No autocomplete for key widget in put mode
        self.lang1_autocomplete(event)

    def handle_lang2_key_release(self, event):
        """ Autocomplete phrase and display related keys | tk.Event -> None """
        self.lang2_autocomplete(event)
    
    def lang1_autocomplete(self, event):
        """ Autocomplete lang1 and suggest lang2 match | tk.Event -> None """
        if not self.lang2.current_text:
            self.lang1.autocomplete(event)
            self.suggest_lang2()

    def lang2_autocomplete(self, event):
        """ Autocomplete lang1 and suggest lang2 match | tk.Event -> None """
        if not self.lang1.current_text:
            self.lang2.autocomplete(event)
            self.suggest_lang1()
        
    def suggest_lang1(self):
        key = self.lang2.get_contents() #Includes suggestion if any
        success = self.lang1.display_phrase(key) #Display top valid phrase
        if not success: #If no valid phrase with autocompleted Key input:
            self.lang1.full_clear() #Clear phrase display
        
    def suggest_lang2(self):
        key = self.lang1.get_contents() #Includes suggestion if any
        success = self.lang2.display_phrase(key) #Display top valid phrase
        if not success: #If no valid phrase with autocompleted Key input:
            self.lang2.full_clear() #Clear phrase display

    def load_tutorial(self):
        """ NOT IMPLEMENTED """
        pass
            
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
        self.master.bind('<Control-c>', lambda event: self.copy())
        self.master.bind('<Command-c>', lambda event: self.copy())
        self.master.bind('<Control-s>', lambda event: self.save_entry())
        self.master.bind('<Command-s>', lambda event: self.save_entry())
        self.master.bind('<Command-z>', lambda event: self.db.undo())
        self.master.bind('<Control-z>', lambda event: self.db.undo())
        self.master.bind('<Control-y>', lambda event: self.db.redo())
        self.master.bind('<Command-y>', lambda event: self.db.redo())
        self.master.bind('<Control-Shift-z>', lambda event: self.db.redo())
        self.master.bind('<Command-Shift-z>', lambda event: self.db.redo())
        self.master.bind('<Up>', lambda event: self.phrase.previous())
        self.master.bind('<Down>', lambda event: self.phrase.next())
        #Key bindings - active when focus on Key entry widget
        self.lang1.bind('<Return>', self.block_new_line)
        self.lang1.bind('<Tab>', self.handle_lang1_tab)
        self.lang1.bind('<BackSpace>', self.handle_lang1_backspace)
        self.lang1.bind('<KeyRelease>', self.handle_lang1_key_release)
        self.lang1.bind('<ButtonRelease>', self.handle_lang1_button_release)
        #Phrase bindings - active when focus on Phrase text widget
        self.lang2.bind('<Return>', self.block_new_line)
        self.lang2.bind('<Tab>', self.handle_lang2_tab)
        self.lang2.bind('<BackSpace>', self.handle_lang2_backspace)
        self.lang2.bind('<ButtonRelease>', self.handle_lang2_button_release)
        self.lang2.bind('<KeyRelease>', self.handle_lang2_key_release)
