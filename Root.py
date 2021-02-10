import tkinter as tk
import config
from MainFrame import MainFrame
from Menus import MenuBar
from commands import print_tracked_events

class Root(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        config.active_objects['root'] = self
        self.main_frame = MainFrame(self)
        self.menu_bar = MenuBar(self)
        self['menu'] = self.menu_bar
        self.title(config.get_language_dict()['title'])
        self.set_geometry()
        self.bind_events()
        
    def redraw(self):
        config.save_config()
        self.__init__()

    def set_geometry(self):
        config_dict = config.get_config()
        if config_dict['initial_geometry']:
            self.geometry(config_dict['initial_geometry'])
        else:
            self.geometry(config_dict['default_size'])
        self.minsize(300, 180)

    def save_geometry(self, event):
        config.get_config()['current_geometry'] = self.geometry()

    def test_keystrokes(self):
        #self.bind('<Command-c>', lambda x:print('Command-c'))
        #Use above as reference
        pass
    
    def bind_events(self):
        self.bind('<Configure>', self.save_geometry)
        #print_tracked_events(self) #Uncomment for testing
        #self.test_keystrokes() #Uncomment for testing

