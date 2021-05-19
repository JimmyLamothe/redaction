""" Implements the MainFrame class

*** NOTE *** - New version being tested to replace MainFrame.py

Classes: MainFrame
         TranslationMainFrame
"""

import tkinter as tk
from PIL import ImageTk, Image
from Key import Key
from Phrase import Phrase, Language1, Language2
import config

class MainFrame(tk.Frame):
    """ Implements the widget interface and logic.

    Displays two text widget with their own internal logic,
    and four optional buttons.
    
    Implements user-input logic not specific to the text widgets.
    
    Handles keyboard and mouse events.

    Args:
        master (tk.Tk): Root object inheriting from tk.Tk

    Methods:
        create_label_1() -> tk.Label
        create_label_2() -> tk.Label
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
        self.db_type = config.get_db_type()
        self.label_1 = self.create_label_1()
        self.label_2 = self.create_label_2()
        if self.db_type == 'standard':
            self.box_1 = Key(self)
            self.box_2 = Phrase(self)
        else:
            self.box_1 = Language1(self)
            self.box_2 = Language2(self)
        if config.get_show_buttons():
            print('creating buttons')
            self.save_button = self.create_save_button()
            self.copy_button = self.create_copy_button()
            self.up_button = self.create_up_button()
            self.down_button = self.create_down_button()
        self.configure_gui()
        self.bind_event_handlers()

    def get_label_1_text(self):
        """ Gets correct text for label 1 None -> str """
        if self.db_type == 'standard':
            text = config.get_language_dict()['key']
        else:
            text = config.get_lang1()
        return text
            
    def get_label_2_text(self):
        """ Gets correct text for label 1 None -> str """
        if self.db_type == 'standard':
            text = config.get_language_dict()['phrase']
        else:
            text = config.get_lang2()
        return text
            
    def create_label_1(self):
        """ Creates a label for the top text widget | None -> tk.Label """
        label = tk.Label(
            master=self,
            text=self.get_label_1_text(),
            bg='#EEEEEE'
        )
        return label
    
    def create_label_2(self):
        """ Creates a label for the bottom text widget | None -> tk.Label """
        label = tk.Label(
            master=self,
            text=self.get_label_2_text(),
            bg='#EEEEEE'
        )
        return label

    def create_save_button(self):
        """ Creates save button on left of app window| None -> tk.Button """
        language_dict = config.get_language_dict() #Active language name dict
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
        """ Creates copy button on right of app window | None -> tk.Button """
        language_dict = config.get_language_dict() #Active language name dict
        button = tk.Button(
            master=self,
            command=self.copy,
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
        """ Creates previous suggestion button | None -> tk.Button """
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
        """ Creates next suggestion button | None -> tk.Button """
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
        self.lang1_label.config(text=self.get_label_1_text())
        self.lang2_label.config(text=self.get_label_2_text())
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
        self.label_1.grid(
            row=0,
            column=0,
            pady=(10,0)
        )
        self.box_1.grid(
            row=0,
            column=1,
            sticky='ew', #Stretches horizontally with window
            padx=(0,100),
            pady=(10,0)
        )
        self.label_2.grid(
            row=1,
            column=0
        )
        self.box_2.grid(
            row=1,
            column=1,
            sticky='nsew', #Stretches with window
            padx=(0,20),
            pady=(5,10)
        )
        if config.get_show_buttons():
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
        self.box_1.focus() #Focus on top text widget

    def get_active_box(self):
        if self.box_2.active_list:
            print('box_2 active')
            return self.box_2
        elif self.box_1.active_list:
            print('box_1 active')
            return self.box_1
        return None

    def next_match(self):
        active_box = self.get_active_box()
        if active_box:
            active_box.next()
        return 'break'

    def previous_match(self):
        active_box = self.get_active_box()
        if active_box:
            active_box.previous()
        return 'break'
    
    def copy(self):
        """ Copy active suggestion to clipboard | None -> None """
        active_box = self.get_active_box()
        if active_lang:
            suggestion = active_box.get_contents()
        else:
            suggestion = None
        if suggestion:
            self.master.clipboard_clear()
            self.master.clipboard_append(suggestion)

    def save_entry(self):
        """ Save combination to database | None -> None """
        error_message = 'save_entry must be overridden by subclass'
        raise NotImplementedError(error_message)

    def delete_entry(self):
        """ Delete combination from database | None -> None """
        error_message = 'delete_entry must be overridden by subclass'
        raise NotImplementedError(error_message)
    
    def block_new_line(self, event):
        """ Prevent new lines in text box | None -> str """
        print('blocking new line')
        return 'break' #Interrupt standard tkinter event processing
        
    def handle_box_1_tab(self, event):
        """ Handle tab keypress in top text box | None -> str """
        if self.box_1.suggestion_text:
            self.box_1.handle_tab(event)
            return 'break' 
        self.box_2.focus()
        return 'break' #Interrupt standard tkinter event processing
    
    def handle_box_2_tab(self, event):
        """ Handle tab keypress in bottom text box | None -> str """
        if self.box_2.suggestion_text:
            self.box_2.handle_tab(event)
            return 'break' 
        self.box_1.focus()
        return 'break' #Interrupt standard tkinter event processing

    def handle_box_1_backspace(self, event):
        """ Handles Backspace + modifier in top text box | tk.Event -> str """
        return self.box_1.handle_backspace(event) #Returns None or 'break'
        
    def handle_box_2_backspace(self, event):
        """ Handles Backspace + modifier in bottom text box | tk.Event -> str """
        return self.box_2.handle_backspace(event) #Returns None or 'break'

    def handle_box_1_button_release(self, event):
        """ Button release manager for top text box | tk.Event -> None """
        if self.box_1.get_selection(): #If user selected text in lang1 box
            self.box_2.confirm_suggestion()
            return
        self.box_1.handle_button_release(event)
        
    def handle_box_2_button_release(self, event):
        """ Button release manager for bottom text box | tk.Event -> None """
        if self.box_2.get_selection(): #If user selected text in lang2 box
            self.box_1.confirm_suggestion()
            return
        self.box_2.handle_button_release(event)
        
    def handle_box_1_key_release(self, event):
        """ Key release manager for top text box | tk.Event -> None """
        if event.keysym in ('Up', 'Down'):
            return 'break'
        self.box_1_autocomplete(event)

    def handle_box_2_key_release(self, event):
        """ Key release manager for bottom text box | tk.Event -> None """
        if event.keysym in ('Up', 'Down'):
            return 'break'
        self.box_2_autocomplete(event)
    
    def box_1_autocomplete(self, event):
        """ Autocomplete box_1 and suggest box_2 match | tk.Event -> None """
        if not self.box_2.current_text:
            self.box_1.autocomplete(event)
            self.suggest_box_2()

    def box_2_autocomplete(self, event):
        """ Autocomplete box_2 and suggest box_1 match | tk.Event -> None """
        if not self.box_1.current_text:
            self.box_2.autocomplete(event)
            self.suggest_box_1()
        
    def suggest_box_1(self):
        error_message = 'suggest_box_1 must be overridden by subclass'
        raise NotImplementedError(error_message)

    def suggest_box_2(self):
        error_message = 'suggest_box_2 must be overridden by subclass'
        raise NotImplementedError(error_message)

    def load_tutorial(self):
        """ NOT IMPLEMENTED """
        pass

    def print_tracker_variables(self):
        print('Key variables:')
        print(f'Box_1 - current_text: {self.key.current_text}')
        print(f'Box_1 - suggestion_text: {self.key.suggestion_text}')
        print(f'Box_1 - suggestion_list: {self.key.suggestion_list}')
        print(f'Box_1 - current_cursor: {self.key.current_cursor}')
        print(f'Box_2 - current_text: {self.phrase.current_text}')
        print(f'Box_2 - suggestion_text: {self.phrase.suggestion_text}')
        print(f'Box_2 - suggestion_list: {self.phrase.suggestion_list}')
        print(f'Box_2 - current_cursor: {self.phrase.current_cursor}')
            
    def bind_event_handlers(self):
        """ Binds all event handlers for all widgets | None -> None """
        #Copy and save bindings - active in all focus states
        self.master.bind('<Control-c>', lambda event: self.copy())
        self.master.bind('<Command-c>', lambda event: self.copy())
        self.master.bind('<Control-s>', lambda event: self.save_entry())
        self.master.bind('<Command-s>', lambda event: self.save_entry())
        self.master.bind('<Control-d>', lambda event: self.delete_entry())
        self.master.bind('<Command-d>', lambda event: self.delete_entry())
        self.master.bind('<Command-z>', lambda event: self.db.undo())
        self.master.bind('<Control-z>', lambda event: self.db.undo())
        self.master.bind('<Control-y>', lambda event: self.db.redo())
        self.master.bind('<Command-y>', lambda event: self.db.redo())
        self.master.bind('<Control-Shift-z>', lambda event: self.db.redo())
        self.master.bind('<Command-Shift-z>', lambda event: self.db.redo())
        self.master.bind('<Up>', lambda event: self.next_match())
        self.master.bind('<Down>', lambda event: self.previous_match())
        #Box_1 bindings - active when focus on Key entry widget
        self.box_1.bind('<Return>', self.block_new_line)
        self.box_1.bind('<Tab>', self.handle_box_1_tab)
        self.box_1.bind('<BackSpace>', self.handle_box_1_backspace)
        self.box_1.bind('<KeyRelease>', self.handle_box_1_key_release)
        self.box_1.bind('<ButtonRelease>', self.handle_box_1_button_release)
        #Box_2 bindings - active when focus on Phrase text widget
        if self.db_type == 'translation':
            self.box_2.bind('<Return>', self.block_new_line)
        self.box_2.bind('<Tab>', self.handle_box_2_tab)
        self.box_2.bind('<BackSpace>', self.handle_box_2_backspace)
        self.box_2.bind('<ButtonRelease>', self.handle_box_2_button_release)
        self.box_2.bind('<KeyRelease>', self.handle_box_2_key_release)

class StandardMainFrame(MainFrame):
    """ Implements the widget interface and logic.

    Displays two text widget with their own internal logic,
    and four optional buttons.
    
    Implements user-input logic not specific to the text widgets.
    
    Handles keyboard and mouse events.

    Args:
        master (tk.Tk): Root object inheriting from tk.Tk

    Methods:
        create_label_1() -> tk.Label
        create_label_2() -> tk.Label
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
        MainFrame.__init__(self, master)

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
        self.label_1.grid(
            row=0,
            column=0,
            pady=(10,0)
        )
        self.box_1.grid(
            row=0,
            column=1,
            sticky='ew', #Stretches horizontally with window
            padx=(0,100),
            pady=(10,0)
        )
        self.label_2.grid(
            row=1,
            column=0
        )
        self.box_2.grid(
            row=1,
            column=1,
            sticky='nsew', #Stretches with window
            padx=(0,20),
            pady=(5,10)
        )
        if config.get_show_buttons():
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
        self.box_1.focus() #Focus on top text widget

    def save_entry(self):
        """ Save active key/phrase combination to db | None -> None """
        #Get key and phrase
        key_list = self.box_1.get_display_key_list()
        print(key_list)
        phrase = self.box_2.get_contents()
        print(phrase)
        #Save combination
        self.db.prepare_undo()
        self.db.save_entry(key_list, phrase)
        print(self.db)
        #Clear widgets after save
        self.box_1.full_clear()
        self.box_2.full_clear()

    def delete_entry(self):
        """ Delete active phrase from db and unused keys | None -> None """
        phrase = self.box_2.get_contents()
        self.db.prepare_undo()
        self.db.delete_phrase(phrase)

    def suggest_box_1(self):
        phrase = self.box_2.get_contents() #Includes suggestion if any
        success = self.box_1.display_matching_keys(phrase) #Display matching keys
        if not success: #If no valid autocompleted phrase:
            self.box_1.full_clear() #Clear key display

    def suggest_box_2(self):
        """ Overrides parent method to work with key lists | None -> None """
        key_list = self.box_1.get_display_key_list() #Includes suggestion if any
        success = self.box_2.display_match(key_list) #Display top valid phrase
        if not success: #If no valid phrase with autocompleted key list:
            self.box_2.full_clear() #Clear phrase display

    def bind_extra_handlers(self):
        """ Bind event handlers specific to subclass | None -> None """
        pass
            
class TranslationMainFrame(MainFrame):
    """ Implements the widget interface and logic.

    Displays a lang1 and lang 2 text widget with their own internal logic,
    and four optional buttons.
    
    Implements user-input logic not specific to the lang1 and lang 2 widgets.
    
    Handles keyboard and mouse events.

    Args:
        master (tk.Tk): Root object inheriting from tk.Tk

    Methods overriden from MainFrame:
        configure_gui()
        save_entry()
    """
    def __init__(self, master):
        MainFrame.__init__(self, master)
        
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
        self.label_1.grid(
            row=0,
            column=0,
            pady=(10,0)
        )
        self.box_1.grid(
            row=0,
            column=1,
            sticky='ew', #Stretches horizontally with window
            padx=(0,20),
            pady=(10,0)
        )
        self.label_2.grid(
            row=1,
            column=0,
            sticky='n',
            pady=(10,0)
        )
        self.box_2.grid(
            row=1,
            column=1,
            sticky='new', #Stretches horizontally with window
            padx=(0,20),
            pady=(5,10)
        )
        if config.get_show_buttons():
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
        self.box_1.focus() #Focus on key widget

    def save_entry(self):
        """ Save active lang1/lang2 combination to db | None -> None """
        #Get key and phrase
        lang1_key = self.box_1.get_contents()
        print(lang1_key)
        lang2_key = self.box_2.get_contents()
        print(lang2_key)
        #Save combination
        self.db.prepare_undo()
        self.db.save_entry(lang1_key, lang2_key)
        print(self.db)
        #Clear widgets after save
        self.box_1.full_clear()
        self.box_2.full_clear()

    def delete_entry(self):
        """ Delete active combination from db | None -> None """
        lang1_key = self.box_1.get_contents()
        lang2_key = self.box_2.get_contents()
        self.db.prepare_undo()
        self.db.delete_match(lang1_key, lang2_key)

    def suggest_box_1(self):
        key = self.box_2.get_contents() #Includes suggestion if any
        success = self.box_1.display_match(key) #Display top valid phrase
        if not success: #If no valid phrase with autocompleted Key input:
            self.box_1.full_clear() #Clear phrase display

    def suggest_box_2(self):
        key = self.box_1.get_contents() #Includes suggestion if any
        success = self.box_2.display_match(key) #Display top valid phrase
        if not success: #If no valid phrase with autocompleted Key input:
            self.box_2.full_clear() #Clear phrase display
        
    def bind_extra_handlers(self):
        """ Bind event handlers specific to subclass | None -> None """
        pass
