""" Implements all the menu classes

MenuBar is the main menu.

At the moment, it includes an OptionMenu and a DisplayMenu, though more
will be added.

The OptionMenu includes a LanguageMenu object and temporary menu options.

The LanguageMenu presently implements French and English modes.

Classes:
    MenuBar
    OptionMenu
    DisplayMenu
    LanguageMenu
"""

import tkinter as tk
from functools import partial
import config

class MenuBar(tk.Menu):
    """ Implements the main menu bar

    Args:
        master(tk.Tk): Root object inheriting from tk.Tk

    Methods:
        add_menus
    """
    def __init__(self, master):
        master.option_add('tearOff', tk.FALSE)
        tk.Menu.__init__(self, master)
        self.option_menu = OptionMenu(self)
        self.display_menu = DisplayMenu(self)
        self.add_menus()
        
    def add_menus(self):
        """ Adds submenus to main menu bar | None -> None """
        language_dict = config.get_language_dict()
        self.add_cascade(
            menu=self.option_menu,
            label=language_dict['options']
        )
        self.add_cascade(
            menu=self.display_menu,
            label=language_dict['display']
        )

        
class OptionMenu(tk.Menu):
    """ Implements the option menu

    Args:
        master(tk.Menu): MainMenu object inheriting from tk.Menu

    Methods:
        temp - TEST FUNCTION, WILL BE DELETED
        add_menus
        add_commands
    """

    def __init__(self, master):
        tk.Menu.__init__(self, master)
        self.language_menu = LanguageMenu(self)
        self.add_commands()
        self.add_menus()
        
    def temp(self):
        """ Test function - to be deleted | None -> None """
        pass

    def add_menus(self):
        """ Add sub menus to option menu | None -> None """
        language_dict = config.get_language_dict()
        self.add_cascade(
            menu=self.language_menu,
            label=language_dict['language']
        )
    
    def add_commands(self):
        """ Add items to option menu | None -> None """
        self.add_command(
            label='Debug Mode',
            command=config.debug_mode
        )
        self.add_command(
            label='Temp 3',
            command=self.temp
        )
        self.add_command(
            label='Temp 4',
            command=self.temp
        )

class DisplayMenu(tk.Menu):
    """ Implements the display menu

    Args:
        master(tk.Menu): MainMenu object inheriting from tk.Menu

    Methods:
        add_commands
    """

    def __init__(self, master):
        tk.Menu.__init__(self, master)
        self.add_commands()

    def add_commands(self):
        """ Add items to display menu | None -> None """
        language_dict = config.get_language_dict()
        self.add_command(
            label=language_dict['show_buttons'],
            command=config.show_buttons
        )
        self.add_command(
            label=language_dict['hide_buttons'],
            command = config.hide_buttons
        )
    
class LanguageMenu(tk.Menu):
    """ Implements the language menu

    Args:
        master(tk.Menu): MainMenu object inheriting from tk.Menu

    Methods:
        add_commands
    """
        
    def __init__(self, master):
        tk.Menu.__init__(self, master)
        self.add_commands()

    def add_commands(self):
        """ Add items to language menu | None -> None """
        for language in config.get_languages():
            self.add_command(
                label=language,
                command=partial(config.set_language, language)
            )
