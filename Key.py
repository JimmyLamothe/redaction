""" Implements the Key class

This class contains all the methods and attributes for the Key widget.

Classes: Key.
"""

import tkinter as tk
import config
import database as db

class Key(tk.Entry):
    """ Implements the logic and interface for the Key entry widget

    The Key entry widget is where the user enters one or more keys in order
    for the corresponding phrases to be displayed in the Phrase text widget,
    or to save the keys and associate them with the current phrase.


    It implements an autocomplete feature displaying a valid complete key
    corresponding to current input.

    Args:
        master (tk.Frame): MainFrame object inheriting from tk.Frame 

    Attributes:
        display_text = tk.StringVar
        current_text = str
        current_cursor = int
        suggestion_text = str
        suggestion_list = list

    Methods:
        __init__(MainFrame)
        get_cursor()
        cursor_at_end(optional:int, optional:str)
        set_cursor(int)
        clear()
        delete_word()
        get_key_list(str) @static
        get_display_key_list()
        get_key_start(int)
        get_key_end(int)
        compare_states()
        autocomplete()
        ignore_suggestion()
        confirm_suggestion()
        debug(str, opt:bool)
    """
    def __init__(self, master):
        self.display_text = tk.StringVar() #Text displayed in entry
        tk.Entry.__init__(
            self,
            master=master, #MainFrame object
            textvariable=self.display_text,
            relief=tk.RIDGE,
            borderwidth=2,
            highlightbackground='#EEEEEE',
            highlightcolor='#EEEEEE',
        )
        """
        NOTE: Current text and cursor do not include the input currently
              being processed. This is why they can differ from the display
              text and display cursor accessed by other methods.
        """
        self.current_text = '' #Actual text input by user
        self.current_cursor = None #Current tracked cursor position
        self.suggestion_text = '' #Current autocomplete string
        self.suggestion_list = []

    def get_cursor(self):
        """ Get index value of current cursor position | None -> int """
        return self.index(tk.INSERT)

    def cursor_at_end(self, cursor=None, text= None):
        """ Check if cursor at end, ignore trailing whitespace | None -> bool """
        if not cursor:
            cursor = self.get_cursor()
        if not text:
            text = self.current_text
        if cursor >= len(text.rstrip()):
            return True
        return False

    def cursor_moved(self):
        """ Check if cursor moved | None -> bool or str"""
        display_cursor = self.get_cursor()
        if self.current_cursor == display_cursor:
            return False
        if self.current_cursor > display_cursor:
            return 'LEFT'
        if self.current_cursor < display_cursor:
            return 'RIGHT'

    def set_cursor(self, index):
        """ Set cursor at specific index | int -> None """
        self.icursor(index)
    
    def clear(self):
        """ Delete all text from Key widget | None -> None """
        self.delete(0, len(self.get()))

    def update_display(self):
        self.debug('update_display')
        self.display_text.set(self.current_text + self.suggestion_text)
        self.set_cursor(len(self.current_text))
        self.debug('update_display', out=True)
        
    def delete_word(self):
        """ Delete prior characters until next space or start | None -> None """
        print('deleting')
        end = self.get_cursor()
        display = self.get()
        start = max(display.rfind(' '), 0)
        self.delete(start, end)
        
    @staticmethod
    def get_key_list(text):
        """ Create a list of keys from a string | str -> list """
        key_list = text.split(' ')
        key_list = [key for key in key_list if not key == '']
        return key_list

    def get_display_key_list(self):
        """ Get list of keys from Key display string | None -> list """
        return self.get_key_list(self.get())
    
    def get_key_start(self, cursor):
        """ Get start of key at current cursor position | None -> int """
        start = max(self.get()[:self.get_cursor()].rfind(' ') + 1, 0)
        return start

    def get_key_end(self, cursor):
        """ Get end of key at current cursor position | None -> int """
        display_text = self.get()
        next_space = display_text[self.get_cursor():].find(' ')
        if next_space == -1:
            end = len(display_text)
        else:
            end = next_space
        return end

    def update_current(self):
        """ Display text and cursor become current | None -> None """
        self.debug('update_current')
        display_text = self.get()
        if self.suggestion_text:
            self.current_text = display_text[:-len(self.suggestion_text)]
        else:
            self.current_text = display_text
        self.current_cursor = self.get_cursor()
        self.debug('update_current', out=True)

    def text_changed(self):
        """ Checks if user text changed since current_text | None -> bool """
        if self.suggestion_text:
            return self.get()[:-len(self.suggestion_text)] != self.current_text
        return self.get() != self.current_text
        
    def get_difference(self):
        """ Gets lastest user input | None -> str """
        display_text = self.get()
        text = display_text[len(self.current_text):] #Remove current text
        if self.suggestion_text: #If suggestion displayed
            text = text[:-len(self.suggestion_text)] #Remove suggestion text
        return text #Remaining characters is the current input

    def autocomplete(self):
        """ Complete current key input with valid keys from db | None -> None """
        self.debug('autocomplete')
        partial_key = self.current_text.split()[-1] #Get last partial key
        suggestion_list = db.valid_keys(partial_key) #All valid possible keys
        print('suggestion_list', suggestion_list)
        if suggestion_list: #If current input can be completed with a valid key: 
            suggestion = suggestion_list[0] #TODO: Rank suggestions
            print('suggestion', suggestion)
            #Save suggested chars
            self.suggestion_text = suggestion[len(partial_key):]
            self.suggestion_list = suggestion_list
            self.update_display()
        self.debug('autocomplete', out=True)

    def reset_suggestions(self):
        self.suggestion_list = []
        self.suggestion_text = ''
        
    def ignore_suggestion(self, cursor=None):
        """ Delete autocompleted char suggestion from display | None -> None """
        self.debug('ignore_suggestion')
        self.reset_suggestions()
        self.update_display()
        self.update_current()
        self.autocomplete()
        self.debug('ignore_suggestion', out=True)
        
    def confirm_suggestion(self, cursor=None):
        """ Keep autocompleted text and set cursor | None -> None """
        self.debug('confirm_suggestion')
        start = len(self.current_text)
        if cursor:
            end = cursor
        else:
            end = len(self.get())
        chars = end - start
        self.current_text += self.suggestion_text[:chars]
        self.suggestion_text = self.suggestion_text[chars:]
        self.update_display()
        self.debug('confirm_suggestion', out=True)
        return True #For tab autocomplete
                   
    def debug(self, name, out=False):
        """ Test function to debug autocomplete logic | optional:str -> None """
        print('')
        if not out:
            print(f'Inside: {name}')
        print(f'current_text = {self.current_text}')
        print(f'current_cursor = {self.current_cursor}')
        print(f'display_text = {self.get()}')
        print(f'display_cursor = {self.get_cursor()}')
        print(f'suggestion_text = {self.suggestion_text}')
        print(f'suggestion_list = {self.suggestion_list}')
        if out:
            print(f'Leaving: {name}')
