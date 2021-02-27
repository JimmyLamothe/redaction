import tkinter as tk
import config
if config.config_dict['db'] == 'def':
    import database as db
else:
    import database_alt as db

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
        return self.get('1.0', tk.END)[:-1] #Remove carriage return

    def create_list(self, key_list):
        if key_list and not key_list == ['']:
            #print('key list', key_list)
            phrase_list = db.get_phrase_list(key_list)
            if phrase_list:
                self.active_list = phrase_list
                self.current_index = 0
                return 'VALID KEY'
        return 'INVALID KEY'

    def clear(self):
        self.delete('1.0', tk.END)

    def get_cursor(self):
        return self.index(tk.INSERT)
        
    def set_cursor(self, line, column):
        self.mark_set(tk.INSERT, f'{line}.{column}')
        
    def search_forwards(self, pattern):
        return self.search(pattern, tk.INSERT, forwards=True, stopindex=tk.END)

    def search_backwards(self, pattern):
        index = self.search(pattern, tk.INSERT, backwards=True, stopindex='1.0')
        line = self.get_cursor()[0]
        if (not index) or (index[0] != line[0]):
            index = f'{line}.0'
        return index

    def delete_word(self):
        start = self.search_backwards(' ')
        end = tk.INSERT
        if start == self.index(tk.INSERT):
            line = int(self.get_cursor()[0])
            if not line == 0:
                start = f'{line-1}.end'
        self.delete(start, end)
    
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
            
    def display_phrase(self, key_list):
        if self.create_list(key_list) == 'VALID KEY':
            #print('Active phrase list:', self.phrase.active_list) #Testing code
            self.clear()
            self.display_current()
            return True
