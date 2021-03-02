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

    Methods:
        __init__(MainFrame)
        get_cursor()
        set_cursor(int)
        clear()
        delete_word()
        get_key_list(str) @static
        get_display_key_list()
        get_key_start(int)
        get_key_end(int)
        compare_states()
        autocomplete()
        reset_auto_vars()
        ignore_suggestion()
        confirm_suggestion()
        print_attributes(optional:str)
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
        self.previous_display = '' # Display text before most recent char input
        self.auto_text='' #Current autocomplete text
        self.auto_cursor=None #Current autocomplete cursor position

    def get_cursor(self):
        """ Get index value of current cursor position | None -> int """
        return self.index(tk.INSERT)
        
    def set_cursor(self, index):
        """ Set cursor at specific index | int -> None """
        self.icursor(index)
    
    def clear(self):
        """ Delete all text from Key widget | None -> None """
        self.delete(0, len(self.get()))

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

    def compare_states(self):
        """ Check if user typed suggested next letter | None -> Bool
        
        If user typed next letter in suggestion, the display will currently
        include that extra letter. For example, if 'ba' was autocompleted to 'baby',
        typing a 'b' will display 'babby'. This method checks ('comparison' variable')
        if removing the autocompleted 'b' (at index 3 in the example)
        from the current display text would match with the previous autocomplete
        suggestion ('self.previous_display'). If so, the user must have typed
        the char we just removed for the check.
        """
        self.print_attributes('compare_states')
        if self.auto_text == '': #If keypress did not input a new char:
            return False
        previous_cursor = self.get_cursor() - 1 #BUG: Will fail if clicked elsewhere
        current = self.get() #Current displayed text
        comparison = current[:previous_cursor] + current[previous_cursor+1:]
        print('comparison', comparison)
        print('previous_display', self.previous_display)
        self.print_attributes()
        return comparison == self.previous_display
        
    def autocomplete(self):
        """ Complete current key input with valid keys from db | None -> None """
        self.print_attributes('autocomplete')
        cursor = self.get_cursor()
        start = self.get_key_start(cursor)
        end = self.get_key_end(cursor)
        partial_key = self.get()[start:end] #Current key being typed
        print(partial_key)
        suggestion_list = db.valid_keys(partial_key) #All valid possible keys
        print('suggestion_list', suggestion_list)
        if suggestion_list: #If current input can be completed with a valid key: 
            suggestion = suggestion_list[0] #TODO: Rank suggestions
            print('suggestion', suggestion)
            self.delete(start, end) #Delete current key from display
            self.insert(start, suggestion) #Replace with suggestion
            self.previous_display = self.get() #Save suggestion for comparison
            self.set_cursor(cursor) #Set cursor to previous position
            self.auto_cursor = cursor #Save cursor position for comparison
            self.auto_text = suggestion[len(partial_key):] #Save autocompleted chars
        self.print_attributes()

    def reset_auto_vars(self):
        """ Forget autocompleted text and cursor position | None -> None """
        self.auto_text = ''
        self.auto_cursor = None
        
    def ignore_suggestion(self):
        """ Delete autocompleted char suggestion from display | None -> None """
        self.print_attributes('ignore_suggestion')
        cursor = self.get_cursor()
        self.delete(cursor, cursor + len(self.auto_text))
        self.reset_auto_vars()
        self.print_attributes()
        
    def confirm_suggestion(self):
        """ Keep autocompleted text and set cursor | None -> Bool """
        if not self.auto_text:
            return False
        self.print_attributes('confirm_suggestion')
        self.set_cursor(self.get_cursor() + len(self.auto_text))
        self.insert(self.get_cursor(), ' ') 
        self.reset_auto_vars()
        self.print_attributes()
        return True
                   
    def print_attributes(self, func_string=None):
        """ Test function to debug autocomplete logic | optional:str -> None """
        if func_string:
            print('Inside:', func_string)
        print('auto_text', self.auto_text)
        print('auto_cursor', self.auto_cursor)
        print('display text', self.get())
        print('display cursor', self.get_cursor())
        if not func_string:
            print('Leaving function')
