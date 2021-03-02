""" Implements the Phrase class

This class contains all methods and attributes for the Phrase widget.

Classes: Phrase
"""

import tkinter as tk
import config
import database as db

class Phrase(tk.Text):
    """ Implements the interface and logic for the Phrase text widget

    The Phrase text widget is where the user types a phrase to be saved
    and associated with the keys entered in the Key widget.

    It is also where the top-ranked phrase associated with the current
    keys is displayed. Ranking is not currently implemented

    It will also be used as a general display for menu help info and startup
    messages.

    Args:
        master (tk.Frame): MainFrame object inheriting from tk.Frame 

    Methods:
        __init__(MainFrame)
        get_contents()
        create_list(list)
        clear()
        get_cursor()
        set_cursor(int, int)
        search_forwards(str)
        search_backwards(str)
        delete_word()
        display_current()
        not_last_index()
        next()
        not_first_index()
        previous()
        display_phrase(list)
    """
    
    def __init__(self, master):
        tk.Text.__init__(
            self,
            master=master, #MainFrame object
            relief=tk.RIDGE,
            borderwidth=2,
            highlightbackground='#EEEEEE',
            highlightcolor='#EEEEEE', #No border on focus
            active_list=None, #Current valid phrases for current keys
            current_index=None #Current active_list index
        )   
        
    def get_contents(self):
        """ Return text contents of widget | None -> str """
        return self.get('1.0', tk.END)[:-1] #Remove carriage return

    def create_list(self, key_list):
        """ Get list of valid phrases for key list | list(str) -> None """
        if key_list and not key_list == ['']:
            print('key list', key_list)
            phrase_list = db.get_phrase_list(key_list)
            if phrase_list:
                self.active_list = phrase_list
                self.current_index = 0
                return 'VALID KEY'
        return 'INVALID KEY'

    def clear(self):
        """ Delete text contents of widget | None -> None """
        self.delete('1.0', tk.END)

    def get_cursor(self):
        """ Get current cursor position | None -> str """
        return self.index(tk.INSERT)
        
    def set_cursor(self, line, column):
        """ Set cursor at specific position | int, int -> None """
        self.mark_set(tk.INSERT, f'{line}.{column}')
        
    def search_forwards(self, pattern):
        """ Get next start position of string pattern | str -> None """
        return self.search(pattern, tk.INSERT, forwards=True, stopindex=tk.END)

    def search_backwards(self, pattern):
        """ Get previous start position of string pattern | str -> None """
        index = self.search(pattern, tk.INSERT, backwards=True, stopindex='1.0')
        line = self.get_cursor()[0]
        if (not index) or (index[0] != line[0]):
            index = f'{line}.0'
        return index

    def delete_word(self):
        """ Delete prior characters until previous space or start | None -> None """
        start = self.search_backwards(' ')
        end = tk.INSERT
        if start == self.index(tk.INSERT):
            line = int(self.get_cursor()[0])
            if not line == 0:
                start = f'{line-1}.end'
        self.delete(start, end)
    
    def display_current(self):
        """ Display current active phrase | None -> None """
        self.insert('1.0', self.active_list[self.current_index])

    def not_last_index(self):
        """ If current self.active_list index isn't the last | None -> Bool """
        if self.active_list and (self.current_index < (len(self.active_list) - 1)):
              return True
        return False

    def next(self):
        """ Displays next phrase in self.active_list | None -> None """
        if self.not_last_index():
            self.current_index += 1
            self.clear()
            self.display_current()
            
    def not_first_index(self):
        """ If current self.active_list index isn't the first | None -> Bool """
        if self.active_list and (self.current_index >= 1):
            return True
        return False
            
    def previous(self):
        """ Displays previous phrase in self.active_list | None -> None """
        if self.not_first_index():
            self.current_index -= 1
            self.clear()
            self.display_current()
            
    def display_phrase(self, key_list):
        """ Displays current phrase in self.active_list | None -> None """
        if self.create_list(key_list) == 'VALID KEY':
            #print('Active phrase list:', self.phrase.active_list) #Testing code
            self.clear()
            self.display_current()
            return True
        else:
            self.clear()
            return False
            
