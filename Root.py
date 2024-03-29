""" Implements the root tkinter window


Classes: Root
"""

import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image
import config
import backup
import Databases
from NewMainFrame import StandardMainFrame
#from MainFrame import MainFrame
from NewMainFrame import TranslationMainFrame
#from TranslationMainFrame import TranslationMainFrame
from Menus import MenuBar
from commands import print_tracked_events


class Root(tk.Tk):
    """ Main tkinter window

    The root window holds the MainFrame object and the MenuBar object.
    It manages the window geography and saves it after user changes.

    Methods:
        redraw()
        set_geometry()
        save_geometry(tkinter.Event)
        test_keystrokes()
        bind_events()
    """
    def __init__(self):
        tk.Tk.__init__(self)
        if not config.get_db_path():
            config.set_db_path()
        if not config.get_backup_path():
            config.set_backup_path()
        if not config.get_session_path():
            config.set_session_path()
        db_type = config.get_db_type()
        if db_type == 'standard':
            db = Databases.StandardDatabase()
        else:
            db = Databases.TranslationDatabase(
                config.get_lang1(),
                config.get_lang2()
            )
        config.active_objects['db'] = db
        config.active_objects['root'] = self #Allows access outside creation module
        backup.backup()
        self.option_add('*Font', 'TkDefaultFont') #All widgets use default font
        if db_type == 'standard':
            self.main_frame = StandardMainFrame(self)
        else:
            self.main_frame = TranslationMainFrame(self)
        self.menu_bar = MenuBar(self)
        self['menu'] = self.menu_bar
        self.title(config.get_language_dict()['title']) #Application name
        icon = Image.open('icons/30101621.png')
        icon = ImageTk.PhotoImage(icon)
        self.iconphoto(True, icon)
        self.set_geometry()
        self.bind_events()
        
    def redraw(self):
        """ Redraws the application window using current config settings """
        config.save_config()
        self.__init__()

    def set_text(self):
        """ Sets text of all widgets to config settings | None -> None """
        language_dict = config.get_language_dict()
        self.title(language_dict['title'])
        self.menu_bar = MenuBar(self)
        self.config(menu = self.menu_bar)
        self.main_frame.set_text(language_dict)

    def set_geometry(self):
        """ Sets the window geometry according to default or current settings """
        config_dict = config.get_config()
        if config_dict['initial_geometry']:
            self.geometry(config_dict['initial_geometry'])
        else:
            self.geometry(config_dict['default_size'])
        self.minsize(400, 160)

    def translation_mode(self, language_pair):
        """ Activate translation mode | None -> None """
        config.set_db_type('translation')
        config.set_language_pair(language_pair)
        
    def save_geometry(self, event):
        """ Saves the current window geometry """
        config.get_config()['current_geometry'] = self.geometry()

    def test_keystrokes(self):
        """ Display keystroke event information """
        #self.bind('<Command-c>', lambda x:print('Command-c'))
        #Use above as reference
        pass
    
    def test_command(self, event):
        print(event)
    
    def bind_events(self, test=False):
        """ Binds all application window events """
        self.bind('<Configure>', self.save_geometry)
        if test:
            print_tracked_events(self)
            #self.bind('<<MenuSelect>>', self.test_command)
            #self.menu_bar.bind('<<MenuSelect>>', self.test_command)
            #self.menu_bar.option_menu.bind('<<MenuSelect>>', self.test_command)
            #self.menu_bar.option_menu.bind('<<MenuSelect>>', self.test_command)
