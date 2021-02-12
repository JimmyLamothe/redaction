import tkinter as tk
import database as db

class Key(tk.Entry):
    def __init__(self, master):
        self.display_text = tk.StringVar() #Text displayed in entry
        tk.Entry.__init__(
            self,
            master=master,
            textvariable=self.display_text,
            relief=tk.RIDGE,
            borderwidth=2,
            highlightbackground='#EEEEEE',
            highlightcolor='#EEEEEE',
        )
        self.user_text='' #Text user has actually input
        self.user_cursor=0

    def get_cursor(self):
        return self.index(tk.INSERT)
        
    def set_cursor(self, index):
        self.icursor(index)
    
    def clear(self, index):
        self.delete(0, len(self.get()))

    @staticmethod
    def get_key_list(text):
        key_list = text.split(' ')
        key_list = [key for key in key_list if not key == '']
        return key_list

    def get_user_key_list(self):
        return self.get_key_list(self.user_text)

    def get_display_key_list(self):
        return self.get_key_list(self.get())
    
    def insert_char(self, char):
        self.print_attributes('insert_char')
        print('before insert', self.user_text)
        cursor = self.get_cursor()
        start = self.user_text[:cursor]
        end = self.user_text[cursor:]
        self.user_text = start + char + end
        print('after insert', self.user_text)
        self.print_attributes

    def get_key_start(self, cursor):
        start = max(self.user_text[:self.get_cursor()].rfind(' '), 0)
        return start

    def get_key_end(self, cursor):
        next_space = self.user_text[self.get_cursor():].find(' ')
        if next_space == -1:
            end = len(self.user_text)
        else:
            end = next_space
        return end
        
    def autocomplete(self):
        self.print_attributes('autocomplete')
        try:
            partial_key = [item for item in self.get_user_key_list()
                           if item not in self.get_display_key_list()][0]
        except IndexError:
            return
        suggestion_list = db.valid_keys(partial_key)
        print('suggestion_list', suggestion_list)
        if suggestion_list:
            suggestion = suggestion_list[0] #TODO: Rank suggestions
            print('suggestion', suggestion)
            cursor = self.get_cursor()
            start = self.key_start(cursor)
            end = self.key_end(cursor)
            self.delete(start, end)
            self.insert(start, suggestion)
            self.current_display = self.get()
            self.set_cursor(cursor)
        self.print_attributes
            
    def confirm_suggestion(self):
        self.print_attributes('confirm_suggestion')
        display_text = self.get()
        cursor_diff = len(display_text) - len(self.user_text)
        self.user_text = display_text
        set_cursor(get_cursor() + cursor_diff)
        self.print_attributes
                   
    def print_attributes(self, func_string=None):
        if func_string:
            print('Inside:', func_string)
        print('user_text', self.user_text)
        print('user_cursor', self.user_cursor)
        print('display text', self.get())
        print('display cursor', self.get_cursor())
        if not func_string:
            print('Leaving function')
