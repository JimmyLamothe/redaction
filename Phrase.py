import tkinter as tk
import database as db

class Phrase(tk.Text):
    def __init__(self, master):
        tk.Text.__init__(
            self,
            master=master,
            relief=tk.RIDGE,
            borderwidth=2,
            highlightbackground='#EEEEEE',
            highlightcolor='#EEEEEE', #No border on focus
            active_list=None,
            current_index=None
        )   
        
    def get_contents(self):
        return self.get('1.0', tk.END)[:-1] #Remove end line

    def create_list(self, key_list):
        if key_list and not key_list == ['']:
            print('key list', key_list)
            phrase_list = db.get_phrase_list(key_list)
            if phrase_list:
                self.active_list = phrase_list
                self.current_index = 0
                return 'VALID KEY'
        return 'INVALID KEY'

    def clear(self):
        self.delete('1.0', tk.END)
    
    def display_current(self):
        self.insert('1.0', self.active_list[self.current_index])

    def not_last_index(self):
        if self.active_list and (self.current_index < (len(self.active_list) - 1)):
              return True
        return False

    def next(self):
        if self.not_last_index():
            self.current_index += 1
            self.clear()
            self.display_current()
            
    def not_first_index(self):
        if self.active_list and (self.current_index >= 1):
            return True
        return False
            
    def previous(self):
        if self.not_first_index():
            self.current_index -= 1
            self.clear()
            self.display_current()
            
    
