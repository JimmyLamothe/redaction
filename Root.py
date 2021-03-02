""" Implements the root tkinter window


Classes: Root
"""

import tkinter as tk
import config
from MainFrame import MainFrame
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
        self.option_add('*Font', 'TkDefaultFont') #All widgets use default font
        config.active_objects['root'] = self #Allows access outside creation module
        self.main_frame = MainFrame(self)
        self.menu_bar = MenuBar(self)
        self['menu'] = self.menu_bar
        self.title(config.get_language_dict()['title']) #Application name
        self.set_geometry()
        self.bind_events()
        
    def redraw(self):
        """ Redraws the application window using current config settings """
        config.save_config()
        self.__init__()

    def set_geometry(self):
        """ Sets the window geometry according to default or current settings """
        config_dict = config.get_config()
        if config_dict['initial_geometry']:
            self.geometry(config_dict['initial_geometry'])
        else:
            self.geometry(config_dict['default_size'])
        self.minsize(300, 180)

    def save_geometry(self, event):
        """ Saves the current window geometry """
        config.get_config()['current_geometry'] = self.geometry()

    def test_keystrokes(self):
        """ Display keystroke event information """
        #self.bind('<Command-c>', lambda x:print('Command-c'))
        #Use above as reference
        pass
    
    def bind_events(self):
        """ Binds all application window events """
        self.bind('<Configure>', self.save_geometry)
        #print_tracked_events(self) #Uncomment for testing
        #self.test_keystrokes() #Uncomment for testing

