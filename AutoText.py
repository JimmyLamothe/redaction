import tkinter as tk

class AutoText(tk.Text):
    def __init__(self, master, **kwargs):
        tk.Text.__init__(
            self,
            master=master, #MainFrame object
            **kwargs
        )

        self.current_text = '' #Actual text input by user
        self.current_cursor = None #Current tracked cursor position
        self.suggestion_text = '' #Current autocomplete string
        self.suggestion_list = [] #Current possible autocompletions
        self.tag_configure('grey', foreground='#666666')
        
    def get_contents(self):
        """ Return text contents of widget | None -> str """
        return self.get('1.0', tk.END)[:-1] #Remove carriage return
        
    def get_cursor(self):
        """ Get index value of current cursor position | None -> int """
        #print(f'\nGetting cursor at: {self.index(tk.INSERT)}')
        return self.index(tk.INSERT)
        cursor = self.index(tk.INSERT)
        start = cursor.find('.') + 1
        return int(cursor[start:])

    def cursor_at_end(self, cursor=None):
        """ Check if cursor at end | None -> bool """
        if not cursor:
            cursor = self.get_cursor()
        if cursor == self.index('end-1c'):
            return True
        print(self.index('end-1c'))
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
        """ Set cursor at specific index | str -> None """
        self.mark_set(tk.INSERT, index)

    def increment_cursor(self, integer):
        """ Increment cursor by i | int -> None """
        self.debug('increment_cursor')
        dot_index = self.current_cursor.find('.')
        start_index = self.current_cursor[:dot_index + 1]
        end_index = int(self.current_cursor[dot_index + 1:])
        end_index += integer
        self.current_cursor = start_index + str(end_index)
        self.debug('increment_cursor', out=True)
        
    def clear(self):
        """ Delete all text from Key widget | None -> None """
        self.delete('1.0', tk.END)

    def update_display(self):
        self.debug('update_display')
        suggestion_start = f'1.{len(self.current_text)}'
        suggestion_end = f'1.{len(self.current_text) + len(self.suggestion_text)}'
        self.clear()
        self.insert('1.0', self.current_text + self.suggestion_text)
        self.tag_add('grey', suggestion_start, suggestion_end)
        self.set_cursor(self.current_cursor)
        self.debug('update_display', out=True)

    def delete_word(self):
        """ Delete prior characters until previous space or start | None -> None """
        start = self.search(' ', 'insert', backwards=True)
        if not start:
            start = '1.0'
        end = self.index(tk.INSERT)
        self.delete(start, end)

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
        print('get_suggestion must be overridden by subclass')
        raise NotImplementedError

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
        
    def ignore_suggestion(self):
        """ Delete autocompleted char suggestion from display | None -> None """
        self.debug('ignore_suggestion')
        self.reset_suggestions()
        self.current_cursor = self.get_cursor()
        self.update_display()
        self.update_current()
        self.debug('ignore_suggestion', out=True)
        
    def confirm_suggestion(self, cursor=None):
        """ Keep autocompleted text and set cursor | None -> None """
        self.debug('confirm_suggestion')
        if not self.suggestion_text:
            print('no suggestion text')
            return False #For tab autocomplete
        if not cursor:
            cursor = self.index('end')
        start = self.current_cursor
        print(f'start: {start}')
        print(f'cursor: {cursor}')
        chars = len(self.get(start, cursor))
        print(f'chars: {chars}')
        self.current_text += self.suggestion_text[:chars]
        self.suggestion_text = self.suggestion_text[chars:]
        self.current_cursor = cursor
        self.update_display()
        self.debug('confirm_suggestion', out=True)
        return True #For tab autocomplete
