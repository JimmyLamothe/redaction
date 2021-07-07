""" Implements the Key class

This class contains all the methods and attributes for the Key widget.

Classes: Key.
"""

import tkinter as tk
from AutoText import AutoText
import config

class Key(AutoText):
    """ Implements the logic and interface for the Key text widget

    The Key text widget is where the user enters one or more keys in order
    for the corresponding phrases to be displayed in the Phrase text widget,
    or to save the keys and associate them with the current phrase.

    It implements an autocomplete feature displaying a valid complete key
    corresponding to current input.

    It is limited to a single line and is a text widget rather than an
    entry widget to allow a different color for the aucompletion.

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
        get_suggestion()
        ignore_suggestion()
        confirm_suggestion()
        debug(str, opt:bool)
    """
    def __init__(self, master):
        AutoText.__init__(
            self,
            master=master, #MainFrame object
            height=1,
            width=40,
            relief=tk.RIDGE,
            bg='#FFFFFF', #F5F5F5 in put mode
            borderwidth=2, #3 in put mode
            highlightbackground='#EEEEEE',
            highlightcolor='#EEEEEE',
        )
        self.db = config.active_objects['db']

    @staticmethod
    def get_key_list(text):
        """ Create a list of keys from a string | str -> list """
        key_list = text.split(' ')
        key_list = [key for key in key_list if not key == '']
        return key_list

    def get_display_key_list(self):
        """ Get list of keys from Key display string | None -> list """
        return self.get_key_list(self.get_contents())

    def display_matching_keys(self, phrase):
        matching_keys_list = self.db.get_matching_keys(phrase)
        matching_keys_string = ' '.join(matching_keys_list)
        print(f'matching keys: {matching_keys_string}')
        if matching_keys_string:
            self.current_text = matching_keys_string
            self.set_contents(self.current_text)
            return True
        return False
    
    def get_suggestion(self):
        """ Complete current key input with valid keys from db | None -> None """
        self.debug('get_suggestion Key')
        partial_key = self.current_text.split()[-1] #Get last partial key
        if self.suggestion_list:
            suggestion_list = self.suggestion_list
        else:
            suggestion_list = self.db.valid_keys(partial_key) #All valid possible keys
            suggestion_list = [s for s in suggestion_list if not s == partial_key]
        print('suggestion_list', suggestion_list)
        if suggestion_list: #If current input can be completed with a valid key: 
            suggestion = suggestion_list[0] #TODO: Rank suggestions
            print('suggestion', suggestion)
            #Save suggested chars
            self.suggestion_text = suggestion[len(partial_key):]
            if self.suggestion_text:
                self.suggestion_list = suggestion_list
            else:
                self.suggestion_list = []
            self.update_display()
        self.debug('get_suggestion', out=True)

    def debug(self, name, out=False):
        if not config.config_dict['debug']:
            return
        super().debug(name, out=out)
