""" Implements the Phrase class

This class contains all methods and attributes for the Phrase widget.

Classes: Phrase
"""

import tkinter as tk
from AutoText import AutoText
import config
import database as db

class Phrase(AutoText):
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
        self.active_list_index=None #Current active_list index
        
    def create_list(self, key_list):
        """ Get list of valid phrases for key list | list(str) -> None """
        if key_list and not key_list == ['']:
            print('key list', key_list)
            phrase_list = db.get_phrase_list(key_list)
            if phrase_list:
                self.active_list = phrase_list
                self.active_list_index = 0
                return 'VALID KEY'
        return 'INVALID KEY'

    def display_current(self):
        """ Display current active phrase | None -> None """
        self.insert('1.0', self.active_list[self.active_list_index])

    def not_last_index(self):
        """ If current self.active_list index isn't the last | None -> Bool """
        if self.active_list and (self.active_list_index <
                                 (len(self.active_list) - 1)):
              return True
        return False

    def next(self):
        """ Displays next phrase in self.active_list | None -> None """
        if self.not_last_index():
            self.active_list_index += 1
            self.clear()
            self.display_current()
            
    def not_first_index(self):
        """ If current self.active_list index isn't the first | None -> Bool """
        if self.active_list and (self.active_list_index >= 1):
            return True
        return False
            
    def previous(self):
        """ Displays previous phrase in self.active_list | None -> None """
        if self.not_first_index():
            self.active_list_index -= 1
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

    def get_suggestion(self):
        """ Complete current input with valid phrase from db | None -> None

        TO BE IMPLEMENTED
        """
        self.debug('get_suggestion')
        partial_phrase = self.get_contents() #Get partial phrase
        if self.suggestion_list:
            suggestion_list = self.suggestion_list
        else:
            suggestion_list = ['INSERT DB METHOD HERE'] #All valid possible phrase
            suggestion_list = [s for s in suggestion_list if not s == partial_key]
        print('suggestion_list', suggestion_list)
        if suggestion_list: #If current input can be completed with a valid phrase: 
            suggestion = suggestion_list[0] #TODO: Rank suggestions
            print('suggestion', suggestion)
            #Save suggested chars
            self.suggestion_text = suggestion[len(partial_phrase):]
            self.suggestion_list = suggestion_list
            self.update_display()
        self.debug('get_suggestion', out=True)
        
    def debug(self, name, out=False):
        if not config.config_dict['debug']:
            return
        super().debug(name, out=out)
