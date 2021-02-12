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
        self.previous_display = ''
        self.auto_text=''
        self.auto_cursor=None

    def get_cursor(self):
        return self.index(tk.INSERT)
        
    def set_cursor(self, index):
        self.icursor(index)
    
    def clear(self):
        self.delete(0, len(self.get()))

    def delete_word(self):
        print('deleting')
        end = self.get_cursor()
        display = self.get()
        start = max(display.rfind(' '), 0)
        self.delete(start, end)
        
    @staticmethod
    def get_key_list(text):
        key_list = text.split(' ')
        key_list = [key for key in key_list if not key == '']
        return key_list

    def get_display_key_list(self):
        return self.get_key_list(self.get())
    
    def get_key_start(self, cursor):
        start = max(self.get()[:self.get_cursor()].rfind(' '), 0)
        return start

    def get_key_end(self, cursor):
        display_text = self.get()
        next_space = display_text[self.get_cursor():].find(' ')
        if next_space == -1:
            end = len(display_text)
        else:
            end = next_space
        return end

    def compare_states(self):
        self.print_attributes('compare_states')
        if self.auto_text == '':
            return False
        previous_cursor = self.get_cursor() - 1
        current = self.get()
        comparison = current[:previous_cursor] + current[previous_cursor+1:]
        print('comparison', comparison)
        print('previous_display', self.previous_display)
        self.print_attributes()
        return comparison == self.previous_display

        
    def autocomplete(self):
        self.print_attributes('autocomplete')
        cursor = self.get_cursor()
        start = self.get_key_start(cursor)
        end = self.get_key_end(cursor)
        partial_key = self.get()[start:end]    
        suggestion_list = db.valid_keys(partial_key)
        print('suggestion_list', suggestion_list)
        if suggestion_list:
            suggestion = suggestion_list[0] #TODO: Rank suggestions
            print('suggestion', suggestion)
            self.delete(start, end)
            self.insert(start, suggestion)
            self.previous_display = self.get()
            self.set_cursor(cursor)
            self.auto_cursor = cursor
            self.auto_text = suggestion[len(partial_key):]
        self.print_attributes()

    def reset_auto_vars(self):
        self.auto_text = ''
        self.auto_cursor = None
        
    def ignore_suggestion(self):
        self.print_attributes('ignore_suggestion')
        cursor = self.get_cursor()
        self.delete(cursor, cursor + len(self.auto_text))
        self.reset_auto_vars()
        self.print_attributes()
        
    def confirm_suggestion(self):
        if not self.auto_text:
            return False
        self.print_attributes('confirm_suggestion')
        self.set_cursor(self.get_cursor() + len(self.auto_text))
        self.insert(self.get_cursor(), ' ') 
        self.reset_auto_vars()
        self.print_attributes()
        return True
                   
    def print_attributes(self, func_string=None):
        if func_string:
            print('Inside:', func_string)
        print('auto_text', self.auto_text)
        print('auto_cursor', self.auto_cursor)
        print('display text', self.get())
        print('display cursor', self.get_cursor())
        if not func_string:
            print('Leaving function')
