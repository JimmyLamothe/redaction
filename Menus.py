import tkinter as tk
from functools import partial
import config

class MenuBar(tk.Menu):
    def __init__(self, master):
        master.option_add('tearOff', tk.FALSE)
        tk.Menu.__init__(self, master)
        self.option_menu = OptionMenu(self)
        self.add_menus()
        
    def add_menus(self):
        self.add_cascade(
            menu=self.option_menu,
            label='Options'
        )
        
class OptionMenu(tk.Menu):
    def __init__(self, master):
        tk.Menu.__init__(self, master)
        self.language_menu = LanguageMenu(self)
        self.add_commands()
        self.add_menus()
        
    def temp(self):
        pass

    def add_menus(self):
        language_dict = config.get_language_dict()
        self.add_cascade(
            menu=self.language_menu,
            label=language_dict['language']
        )
    
    def add_commands(self):
        self.add_command(
            label='Temp 2',
            command=self.temp
        )
        self.add_command(
            label='Temp 3',
            command=self.temp
        )
        self.add_command(
            label='Temp 4',
            command=self.temp
        )
    
class LanguageMenu(tk.Menu):
    def __init__(self, master):
        tk.Menu.__init__(self, master)
        self.add_commands()

    def add_commands(self):
        for language in config.get_languages():
            print('adding language:', language)
            self.add_command(
                label=language,
                command=partial(config.set_language, language)
            )
