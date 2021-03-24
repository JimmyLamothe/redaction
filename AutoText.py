import tkinter as tk

class AutoText(tk.Text):
    def __init__(self, master, **kwargs):
        tk.Text.__init__(
            self,
            master=master, #MainFrame object
            **kwargs
        )
        self.DELETE_KEYSYMS = ['Delete','KP_Delete','BackSpace']
        self.DELETE_KEYCODES = [458872, 458776]
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

    def search_forwards(self, pattern, stopindex=tk.END):
        """ Get next start position of string pattern | str -> None """
        return self.search(pattern, 'insert', forwards=True, stopindex=stopindex)

    def search_backwards(self, pattern, stopindex='1.0'):
        """ Get previous start position of string pattern | str -> None """
        return self.search(pattern, 'insert', backwards=True, stopindex=stopindex)
    
    def delete_word(self):
        """ Delete prior characters until previous space or start | None -> None """
        start = self.search_backwards(' ')
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
        error_message = 'get_suggestion must be overridden by subclass'
        raise NotImplementedError(error_message)

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
            cursor = self.index('end-1c')
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

    def autocomplete(self, event):
        """ Autocomplete logic | tk.Event -> None """
        if event.keysym == 'Tab':
            self.debug(0)
            return 'break'
        #If input was a delete command:
        if (event.keysym in self.DELETE_KEYSYMS) or (event.keycode in
                                                     self.DELETE_KEYCODES):
            self.debug(1)
            self.update_current() #Update current user text
            if self.suggestion_text:
                self.ignore_suggestion() #Delete suggestions and update display
            else:
                self.reset_suggestions() #Delete suggestions
            self.debug(1.0)
        elif not self.suggestion_text: #If no suggestion displayed
            self.debug(2)
            if self.text_changed(): #If input received
                self.debug(2.1)
                self.update_current()
                if self.cursor_at_end(): #If cursor at end
                    self.debug(2.11)
                    self.get_suggestion() #Get suggestion
            self.debug(2.0)
        elif not self.text_changed(): #If no new input char
            self.debug(3)
            if self.cursor_moved() == 'LEFT': #If cursor moved left
                self.debug(3.1)
                self.ignore_suggestion() #Delete suggestion text
            elif self.cursor_moved() == 'RIGHT': #If cursor moved right
                self.debug(3.2)
                #Confirm suggestion up to cursor position
                self.confirm_suggestion(cursor=self.get_cursor())
                self.update_suggestions()
                self.get_suggestion() #Get next top suggestion from list
            self.update_current()
            self.debug(3.0)
        else: #If suggestion active and text changed
            self.debug(4)
            current_input = self.get_difference() #Get new user input
            self.update_current()
            print(f'current_input = {current_input}')
            print(f'len(current_input) = {len(current_input)}')
            if not len(current_input) == 1: #If user input more than one char
                self.debug(4.1)
                self.ignore_suggestion() #Delete suggestion text
            #If input char was next char in suggestion
            elif current_input == self.suggestion_text[0]:
                self.debug(4.2)
                #Confirm suggestion up to cursor
                self.suggestion_text = self.suggestion_text[1:]
                self.update_display()
                self.confirm_suggestion(self.get_cursor()) 
                self.update_suggestions()
                self.get_suggestion() #Get next top suggestion from list
            else:
                self.debug(4.3)
                self.ignore_suggestion() #Delete suggestion text
                self.get_suggestion() #Get new suggestions
            self.debug(4.0)

    def handle_button_release(self, event):
        """ Autocompletion on mouse button release | tk.Event -> None """
        if self.suggestion_text: #If suggestion displayed
            try: #If text was selected
                start = self.index(tk.SEL_FIRST)
                end = self.index(tk.SEL_LAST)
                self.confirm_suggestion(cursor=end) #Confirm selected text if any
                self.tag_remove('sel', '1.0', tk.END)
                self.tag_add('sel', start, end)
            except tk.TclError: #If no text was selected
                pass
            if self.cursor_moved() == 'LEFT': #If cursor moved left
                self.ignore_suggestion() #Delete suggestion text
            elif self.cursor_moved() == 'RIGHT': #If cursor moved right
                #Confirm suggestion up to cursor position
                self.confirm_suggestion(cursor=self.get_cursor())

    def handle_backspace(self, event):
        """ Backspace + modifier deletes previous word | tk.Event -> str """
        if event.state in [1,4,8,16]: #If any key modifier + backspace
            self.delete_word() #Delete previous word in Key widget
            return 'break' #Interrupt standard tkinter event processing

    def handle_tab(self, event, return_value='break'):
        """ Tab confirms current suggestion | tk.Event -> str 

        return_value can be used to return True if suggestion was confirmed
        or False if it wasn't. This lets you handle the tab key differently
        in each circumstance. By default, it returns 'break' to stop the standard
        tkinter processing for the tab key.
        """
        if return_value not in ['break', 'bool']:
            error_message = 'return_value must be the string "break"'
            error_message += 'or the string "bool"'
            raise ValueError(error_message) 
        if self.confirm_suggestion():
            self.update_suggestions()
            self.get_suggestion() #Get next top suggestion from list
            self.update_current()
            if return_value == 'break':
                return 'break'
            return True
        if return_value == 'break':
            return 'break'
        return False

    def debug(self, name, out=False):
        """ Test function to debug autocomplete logic | optional:str -> None """
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
