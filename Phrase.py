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
            bg='#F5F5F5',#FFFFFF in put mode
            borderwidth=3, #2 in put mode
            highlightbackground='#EEEEEE',
            highlightcolor='#EEEEEE', #No border on focus
        )
        self.active_list=None, #Current valid phrases for current keys
        self.current_index=None #Current active_list index
        self.current_text = '' #Actual text input by user
        self.current_cursor = None #Current tracked cursor position
        self.suggestion_text = '' #Current autocomplete string
        self.suggestion_list = [] #Current possible autocompletions
        self.tag_configure('grey', foreground='#666666')
        
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

    def cursor_at_end(self, cursor=None, text= None):
        """ Check if cursor at end, ignore trailing whitespace | None -> bool """
        if not cursor:
            cursor = self.get_cursor()
        if not text:
            text = self.current_text
        if cursor >= len(text.rstrip()):
            return True
        return False
        
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

    def update_current(self):
        """ Display text and cursor become current | None -> None """
        self.debug('update_current')
        display_text = self.get_contents()
        if self.suggestion_text:
            self.current_text = display_text[:-len(self.suggestion_text)]
        else:
            self.current_text = display_text
        self.current_cursor = self.get_cursor()
        self.debug('update_current', out=True)

    def text_changed(self):
        """ Checks if user text changed since current_text | None -> bool """
        if self.suggestion_text:
            display_text = self.get_contents()
            return display_text[:-len(self.suggestion_text)] != self.current_text
        return self.get_contents() != self.current_text
        
    def get_difference(self):
        """ Gets lastest user input | None -> str """
        display_text = self.get_contents()
        text = display_text[len(self.current_text):] #Remove current text
        if self.suggestion_text: #If suggestion displayed
            text = text[:-len(self.suggestion_text)] #Remove suggestion text
        return text #Remaining characters is the current input

    def get_suggestion(self):
        """ Complete current key input with valid keys from db | None -> None """
        self.debug('get_suggestion')
        partial_key = self.current_text.split()[-1] #Get last partial key
        if self.suggestion_list:
            suggestion_list = self.suggestion_list
        else:
            suggestion_list = db.valid_keys(partial_key) #All valid possible keys
        print('suggestion_list', suggestion_list)
        if suggestion_list: #If current input can be completed with a valid key: 
            suggestion = suggestion_list[0] #TODO: Rank suggestions
            print('suggestion', suggestion)
            #Save suggested chars
            self.suggestion_text = suggestion[len(partial_key):]
            self.suggestion_list = suggestion_list
            self.update_display()
        self.debug('get_suggestion', out=True)

    def update_suggestions(self):
        """ Removes impossible suggestions as user types | None -> None """
        self.debug('update_suggestions')
        self.suggestion_list = [suggestion for suggestion in self.suggestion_list
                                if suggestion.startswith(self.current_text)
                                and not suggestion == self.current_text]
        self.debug('update_suggestions', out=True)
        
    def reset_suggestions(self):
        self.suggestion_list = []
        self.suggestion_text = ''
        
    def ignore_suggestion(self, cursor=None):
        """ Delete autocompleted char suggestion from display | None -> None """
        self.debug('ignore_suggestion')
        self.reset_suggestions()
        self.update_display()
        self.update_current()
        self.debug('ignore_suggestion', out=True)
        
    def confirm_suggestion(self, cursor=None):
        """ Keep autocompleted text and set cursor | None -> None """
        if not self.suggestion_text:
            return False #For tab autocomplete
        self.debug('confirm_suggestion')
        start = len(self.current_text)
        if cursor:
            end = cursor
        else:
            end = len(self.get_contents())
        chars = end - start
        self.current_text += self.suggestion_text[:chars]
        self.suggestion_text = self.suggestion_text[chars:]
        self.update_display()
        self.debug('confirm_suggestion', out=True)
        return True #For tab autocomplete
                   
    def debug(self, name, out=False):
        """ Test function to debug autocomplete logic | optional:str -> None """
        if not config.config_dict['debug']:
            return
        print('')
        if not out:
            print(f'Inside: {name}')
        print(f'current_text = {self.current_text}')
        print(f'current_cursor = {self.current_cursor}')
        print(f'display_text = {self.get_contents()}')
        print(f'display_cursor = {self.get_cursor()}')
        print(f'suggestion_text = {self.suggestion_text}')
        print(f'suggestion_list = {self.suggestion_list}')
        if out:
            print(f'Leaving: {name}')

        
