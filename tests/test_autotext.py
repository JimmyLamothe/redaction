""" Tests for AutoText class

Tests not written for all methods. Add more as bugs arise.
"""
import pytest
import mock
import config
from AutoText import AutoText
import tkinter as tk

@pytest.fixture
def widget():
    return AutoText(tk.Tk())

def generate_suggestion_widget():
    widget = AutoText(tk.Tk())
    widget.set_contents('TextSuggestion')
    widget.current_text = 'Text'
    widget.suggestion_list = ['TextSuggestion']
    widget.suggestion_text = 'Suggestion'
    widget.current_cursor = '1.4'
    return widget

@pytest.fixture
def suggestion_widget():
    return generate_suggestion_widget()

def test_set_get_clear_contents(widget):
    assert widget.get_contents() == ''
    widget.set_contents('test')
    assert widget.get_contents() == 'test'
    widget.clear()
    assert widget.get_contents() == ''

def test_get_selection(widget):
    widget.set_contents('Select THIS not THAT')
    assert widget.get_selection() is None
    widget.tag_add('sel', '1.7', '1.11')
    assert widget.get_selection() == 'THIS'
    
def test_cursor_methods(widget):
    """ Tests get_cursor, set_cursor and cursor_moved """
    widget.set_contents('Cursor tests')
    assert widget.get_cursor() == '1.12'
    assert widget.cursor_at_end()
    widget.set_cursor('1.0')
    assert widget.get_cursor() == '1.0'
    widget.set_cursor('1.15')
    assert widget.get_cursor() == '1.12'
    assert widget.cursor_at_end()
    widget.set_cursor('4.24')
    assert widget.get_cursor() == '1.12'
    assert widget.cursor_at_end()
    widget.current_cursor = '1.12'
    assert widget.cursor_moved() == False
    widget.set_cursor('1.06')
    assert widget.cursor_moved() == 'LEFT'
    widget.current_cursor = '1.06'
    widget.set_cursor('1.07')
    assert widget.cursor_moved() == 'RIGHT'

def test_clear_and_full_clear(widget):
    assert widget.get_contents() == ''
    widget.set_contents('adfg')
    widget.current_cursor = widget.get_cursor()
    widget.current_text = widget.get_contents()
    assert widget.get_contents() == 'adfg'
    assert widget.get_cursor() == '1.4'
    assert widget.current_text == 'adfg'
    assert widget.current_cursor == '1.4'
    widget.clear()
    assert widget.get_contents() == ''
    assert widget.get_cursor() == '1.0'
    assert widget.current_text == 'adfg'
    assert widget.current_cursor == '1.4'
    widget.full_clear()
    assert widget.get_contents() == ''
    assert widget.get_cursor() == '1.0'
    assert widget.current_text == ''
    assert widget.current_cursor == None
    

def test_update_display(widget):
    widget.set_contents('Start')
    widget.current_text = widget.get_contents()
    widget.current_cursor = widget.get_cursor()
    widget.suggestion_text = 'Suggestion'
    widget.update_display()
    assert widget.get_contents() == 'StartSuggestion'
    assert widget.get_cursor() == '1.5'
    assert widget.current_cursor == '1.5'
    assert widget.tag_names('1.5') == ('grey',)
    assert widget.tag_names('1.14') == ('grey',)

def test_search_forwards(widget):
    widget.set_contents('Search string')
    assert widget.search_forwards('', index='1.0') == None
    assert widget.search_forwards('Not in string', index='1.0') == None
    assert widget.search_forwards('S', index='1.0') == '1.0'
    assert widget.search_forwards('S', index='1.1') == None
    assert widget.search_forwards('s', index='1.0') == '1.7'
    assert widget.search_forwards('tri', index='1.0') == '1.8'
    
def test_search_backwards(widget):
    widget.set_contents('Search string')
    assert widget.search_backwards('', index='end') == None
    assert widget.search_backwards('Not in string', index='end') == None
    assert widget.search_backwards('S', index='1.0') == None
    assert widget.search_backwards('g', index='end') == '1.12'
    assert widget.search_backwards('g', index='end-1c') == '1.12'
    assert widget.search_backwards('g', index='end-2c') == None
    assert widget.search_backwards('s', index='end') == '1.7'
    assert widget.search_backwards('tri', index='end') == '1.8'
    
def test_delete_word(widget):
    assert widget.get_contents() == ''
    widget.delete_word()
    assert widget.get_contents() == ''
    widget.set_contents('word')
    widget.delete_word()
    assert widget.get_contents() == ''
    widget.set_contents('Multiple words, even a phrase')
    widget.delete_word()
    assert widget.get_contents() == 'Multiple words, even a'
    widget.delete_word()
    assert widget.get_contents() == 'Multiple words, even'
    widget.set_cursor('insert-1c')
    widget.delete_word()
    assert widget.get_contents() == 'Multiple words,n'
    widget.set_cursor('end-1c')
    widget.delete_word()
    assert widget.get_contents() == 'Multiple'
    
def test_update_current(widget):
    widget.set_contents('New stuff')
    assert widget.current_text == ''
    assert widget.current_cursor == None
    widget.update_current()
    assert widget.current_text == 'New stuff'
    assert widget.current_cursor == '1.9'
    widget.set_contents('New stuff' + 'New suggestion')
    widget.set_cursor(widget.current_cursor)
    widget.suggestion_text = 'New suggestion'
    widget.update_current()
    assert widget.current_text == 'New stuff'
    assert widget.current_cursor == '1.9'
    
def test_text_changed(suggestion_widget):
    widget = suggestion_widget
    assert widget.text_changed() == False
    widget.set_contents('TextASuggestion')
    assert widget.text_changed() == True
    widget.suggestion_text = ''
    widget.set_contents('Text')
    assert widget.text_changed() == False
    widget.set_contents('TextA')
    assert widget.text_changed() == True
    widget.set_contents('AText')
    assert widget.text_changed() == True
    
def test_get_difference(widget, suggestion_widget):
    widget.set_contents('Text')
    widget.current_text = 'Text'
    widget.current_cursor = '1.4'
    widget.suggestion_text = ''
    assert widget.get_difference() == ''
    widget.set_contents('Texta')
    assert widget.get_difference() == 'a'
    widget.set_contents('TextLotOfText')
    assert widget.get_difference() == 'LotOfText'
    widget = suggestion_widget
    assert widget.get_difference() == ''
    widget.set_contents('TextaSuggestion')
    assert widget.get_difference() == 'a'
    widget.set_contents('TextLotOfTextSuggestion')
    assert widget.get_difference() == 'LotOfText'
    
def test_get_suggestion(widget):
    with pytest.raises(NotImplementedError) as excinfo:
        widget.get_suggestion()
    assert str(excinfo.value) == 'get_suggestion must be overridden by subclass'
    
def test_update_suggestions(widget):
    original_list = ['pou', 'poule', 'poulet', 'poulet frit','poulet au miel']
    widget.suggestion_list = original_list
    widget.current_text = ''
    widget.update_suggestions()
    assert widget.suggestion_list == original_list
    widget.current_text = 'c'
    widget.update_suggestions()
    assert widget.suggestion_list == []
    widget.suggestion_list = original_list
    widget.current_text = 'p'
    widget.update_suggestions()
    assert widget.suggestion_list == original_list
    widget.current_text = 'pou'
    widget.update_suggestions()
    current_list = [item for item in original_list]
    current_list.remove('pou')
    assert widget.suggestion_list == current_list
    widget.current_text = 'poul'
    widget.update_suggestions()
    assert widget.suggestion_list == current_list
    widget.current_text = 'poule'
    widget.update_suggestions()
    current_list.remove('poule')
    assert widget.suggestion_list == current_list
    widget.current_text = 'poulet'
    widget.update_suggestions()
    current_list.remove('poulet')
    assert widget.suggestion_list == current_list
    widget.current_text = 'poulet '
    widget.update_suggestions()
    assert widget.suggestion_list == current_list
    widget.current_text = 'poulet f'
    widget.update_suggestions()
    current_list.remove('poulet au miel')
    assert widget.suggestion_list == ['poulet frit']
    widget.current_text = 'poulet frit'
    widget.update_suggestions()
    assert widget.suggestion_list == []

def test_reset_suggestions(widget):
    widget.suggestion_list = ['sugg1', 'sugg2']
    widget.suggestion_text = 'sugg1'
    widget.reset_suggestions()
    assert widget.suggestion_list == []
    assert widget.suggestion_text == ''

def test_ignore_suggestion(suggestion_widget):
    widget = suggestion_widget
    widget.ignore_suggestion()
    assert widget.current_text == 'Text'
    assert widget.get_contents() == 'Text'
    assert widget.current_cursor == '1.4'
    assert widget.get_cursor() == '1.4'
    assert widget.suggestion_list == []
    assert widget.suggestion_text == ''

def test_confirm_suggestion(widget, suggestion_widget):
    assert widget.confirm_suggestion() is False
    widget = suggestion_widget
    widget.confirm_suggestion()
    assert widget.get_contents() == 'TextSuggestion' == widget.current_text
    assert widget.get_cursor() == '1.14' == widget.current_cursor
    assert widget.suggestion_list == ['TextSuggestion']
    assert widget.suggestion_text == ''
    widget = generate_suggestion_widget()
    widget.confirm_suggestion(cursor='1.11')
    assert widget.get_contents() == 'TextSuggestion'
    assert widget.current_text == 'TextSuggest'
    assert widget.get_cursor() == '1.11' == widget.current_cursor
    assert widget.suggestion_list == ['TextSuggestion']
    assert widget.suggestion_text == 'ion'

def test_type_text(widget):
    assert widget.get_contents() == ''
    widget.type_text('a')
    assert widget.get_contents() == 'a'
    widget.type_text('b')
    assert widget.get_contents() == 'ab'
    widget.type_text('c', 1)
    assert widget.get_contents() == 'acb'
    assert widget.get_cursor() == '1.2'
    widget.type_text('d', 0)
    assert widget.get_contents() == 'dacb'
    assert widget.get_cursor() == '1.1'

def test_backspace(widget):
    widget.type_text('abcdefg')
    assert widget.get_contents() == 'abcdefg'
    widget.backspace_text()
    assert widget.get_contents() == 'abcdef'
    widget.backspace_text(0)
    assert widget.get_contents() == 'abcdef'
    widget.backspace_text(1)
    assert widget.get_contents() == 'bcdef'

def test_delete(widget):
    widget.type_text('abcdefg')
    assert widget.get_contents() == 'abcdefg'
    widget.delete_text()
    assert widget.get_contents() == 'abcdefg'
    widget.delete_text(6)
    assert widget.get_contents() == 'abcdef'
    widget.delete_text(0)
    assert widget.get_contents() == 'bcdef'
        
class DummyEvent():
    def __init__(self, key):
        if type(key) == int: 
            self.keycode = key
            self.keysym = None
        else:
            self.keycode = None
            self.keysym = key

def test_autocomplete_delete(suggestion_widget):
    """ Section 1 of autocomplete function """
    suggestion_widget.delete_text()
    suggestion_widget.autocomplete(DummyEvent('Delete'))
    assert suggestion_widget.get_contents() == 'Text'
    assert suggestion_widget.suggestion_text == ''
    assert suggestion_widget.current_text == 'Text'
    assert suggestion_widget.suggestion_list == []
    suggestion_widget = generate_suggestion_widget()
    suggestion_widget.delete_text()
    suggestion_widget.autocomplete(DummyEvent('KP_Delete'))
    assert suggestion_widget.get_contents() == 'Text'
    assert suggestion_widget.suggestion_text == ''
    assert suggestion_widget.current_text == 'Text'
    assert suggestion_widget.suggestion_list == []
    suggestion_widget = generate_suggestion_widget()
    suggestion_widget.backspace_text()
    suggestion_widget.autocomplete(DummyEvent('BackSpace'))
    assert suggestion_widget.get_contents() == 'Tex'
    assert suggestion_widget.suggestion_text == ''
    assert suggestion_widget.current_text == 'Tex'
    assert suggestion_widget.suggestion_list == []
    suggestion_widget = generate_suggestion_widget()
    suggestion_widget.delete_text()
    suggestion_widget.autocomplete(DummyEvent(458872))
    assert suggestion_widget.get_contents() == 'Text'
    assert suggestion_widget.suggestion_text == ''
    assert suggestion_widget.current_text == 'Text'
    assert suggestion_widget.suggestion_list == []
    suggestion_widget = generate_suggestion_widget()
    suggestion_widget.backspace_text()
    suggestion_widget.autocomplete(DummyEvent(458776))
    assert suggestion_widget.get_contents() == 'Tex'
    assert suggestion_widget.suggestion_text == ''
    assert suggestion_widget.current_text == 'Tex'
    assert suggestion_widget.suggestion_list == []
    
def get_suggestion_no_list(self): #will replace AutoText method
    if self.suggestion_list:
        suggestion = self.suggestion_list[0]
        self.suggestion_text = suggestion[len(self.current_text):]
    self.update_display()

@pytest.fixture
def mock_get_suggestion_no_list(monkeypatch):
    """ Patch get_suggestion as if db had no match | None -> None """
    monkeypatch.setattr(AutoText, 'get_suggestion', get_suggestion_no_list)
    
def get_suggestion_dummy_list(self): #Will replace AutoText method
    if not self.suggestion_list:
        self.suggestion_list = [
            self.current_text + 'Suggestion1',
            self.current_text + 'Suggestion2'
        ]
    suggestion = self.suggestion_list[0]
    self.suggestion_text = suggestion[len(self.current_text):]
    self.update_display()

@pytest.fixture
def mock_get_suggestion_dummy_list(monkeypatch):
    """ Patch get_suggestion as if db had two matches | None -> None """
    monkeypatch.setattr(AutoText, 'get_suggestion', get_suggestion_dummy_list)

def test_autocomplete_no_suggestion(widget, mock_get_suggestion_no_list):
    """ Section 2 of autocomplete with no db matches """
    widget.type_text('a')
    widget.autocomplete(DummyEvent('a'))
    assert widget.current_text == 'a'
    assert widget.suggestion_text == ''
    assert widget.suggestion_list == []
    assert widget.current_cursor == '1.1'

def test_autocomplete_dummy_suggestion(widget, mock_get_suggestion_dummy_list):
    """ Section 2 of autocomplete with db matches """
    widget.type_text('a')
    widget.autocomplete(DummyEvent('a'))
    assert widget.current_text == 'a'
    assert widget.suggestion_text == 'Suggestion1'
    assert widget.suggestion_list == ['aSuggestion1', 'aSuggestion2']
    assert widget.current_cursor == '1.1'
    assert widget.get_contents() == 'aSuggestion1'

def test_autocomplete_cursor_moved_left(suggestion_widget):
    """ Section 3 of autocomplete with cursor moving left """
    suggestion_widget.set_cursor('1.3')
    suggestion_widget.autocomplete(DummyEvent(''))
    assert suggestion_widget.current_text == 'Text'
    assert suggestion_widget.get_contents() == 'Text'
    assert suggestion_widget.current_cursor == '1.3'
    assert suggestion_widget.get_cursor() == '1.3'
    assert suggestion_widget.suggestion_text == ''
    assert suggestion_widget.suggestion_list == []

def get_suggestion_single_list(self): #Will replace AutoText method
    if not self.suggestion_list:
        self.suggestion_list = ['TextSuggestion']
    suggestion = self.suggestion_list[0]
    self.suggestion_text = suggestion[len(self.current_text):]
    if not self.suggestion_text:
        self.suggestion_list = []
    self.update_display()

@pytest.fixture
def mock_get_suggestion_single_list(monkeypatch):
    """ Patch get_suggestion as if db had one match | None -> None """
    monkeypatch.setattr(AutoText, 'get_suggestion', get_suggestion_single_list)
    
def test_autocomplete_cursor_moved_right(suggestion_widget,
                                         mock_get_suggestion_single_list):
    """ Section 3 of autocomplete with cursor moving right """
    suggestion_widget.set_cursor('1.5')
    suggestion_widget.autocomplete(DummyEvent(''))
    assert suggestion_widget.current_text == 'TextS'
    assert suggestion_widget.get_contents() == 'TextSuggestion'
    assert suggestion_widget.current_cursor == '1.5'
    assert suggestion_widget.get_cursor() == '1.5'
    assert suggestion_widget.suggestion_text == 'uggestion'
    assert suggestion_widget.suggestion_list == ['TextSuggestion']
    suggestion_widget.set_cursor('1.13')
    suggestion_widget.autocomplete(DummyEvent(''))
    assert suggestion_widget.current_text == 'TextSuggestio'
    assert suggestion_widget.get_contents() == 'TextSuggestion'
    assert suggestion_widget.current_cursor == '1.13'
    assert suggestion_widget.get_cursor() == '1.13'
    assert suggestion_widget.suggestion_text == 'n'
    assert suggestion_widget.suggestion_list == ['TextSuggestion']
    suggestion_widget.set_cursor('1.14')
    suggestion_widget.autocomplete(DummyEvent(''))
    assert suggestion_widget.current_text == 'TextSuggestion'
    assert suggestion_widget.get_contents() == 'TextSuggestion'
    assert suggestion_widget.current_cursor == '1.14'
    assert suggestion_widget.get_cursor() == '1.14'
    assert suggestion_widget.suggestion_text == ''
    assert suggestion_widget.suggestion_list == []
    
def test_autocomplete_text_changed_sugg_active(suggestion_widget,
                                               mock_get_suggestion_single_list):
    """ Section 4.1 of autocomplete """
    suggestion_widget.type_text('ab') #BUGGED - FIX
    suggestion_widget.autocomplete(DummyEvent('ab'))
    assert suggestion_widget.current_text == 'Textab'
    assert suggestion_widget.get_contents() == 'Textab'
    assert suggestion_widget.current_cursor == '1.6'
    assert suggestion_widget.get_cursor() == '1.6'
    assert suggestion_widget.suggestion_text == ''
    assert suggestion_widget.suggestion_list == []
    
def _test_autocomplete(self, event):
    """ Autocomplete logic | tk.Event -> None """
    #If input was a delete command:
    if (event.keysym in self.DELETE_KEYSYMS) or (event.keycode in
                                                 self.DELETE_KEYCODES):
        self.debug(1)
        self.update_current() #Update current user text
        self.debug(1.05)
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

def _test_handle_button_release(self, event):
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

def _test_handle_backspace(self, event):
    """ Backspace + modifier deletes previous word | tk.Event -> str """
    if event.state in [1,4,8,16]: #If any key modifier + backspace
        self.delete_word() #Delete previous word in Key widget
        return 'break' #Interrupt standard tkinter event processing

def _test_handle_tab(self, event):
    """ Tab confirms current suggestion | tk.Event -> str """
    if self.confirm_suggestion():
        self.update_suggestions()
        self.get_suggestion() #Get next top suggestion from list
        self.update_current()

def _test_debug(self, name, out=False):
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
