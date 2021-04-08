""" Main configuration module for Key/Phrase

Implements logic and stores constants.

Stores and manages variables related to user configuration.

Constants:
    DEFAULT_CONFIG
    FRENCH_DICT
    ENGLISH_DICT
    LANGUAGE_DICT

Variables:
    active_objects
    config_dict

Functions:
    load_config()
    save_config()
    reset_config()
    backup()
    restore()
    set_language(str)
    get_language_dict()
    show_buttons()
    hide_buttons()
    get_config()
    get_languages()
"""

import atexit
import shutil
import pathlib
import json
from json.decoder import JSONDecodeError
from utilities import get_default_dir

#Default configuration on first execution or config reset
DEFAULT_CONFIG = {
    'initial_geometry':'', #Initial size and position of app window
    'current_geometry':'', #Current size and position of app window
    'default_size':'600x250', #Default size of app window
    'show_buttons':True, #Show or hide app buttons
    'language':'Français', #Current app interface language
    'mode':'put', #'get' entry from db or 'put' entry in db
    'db':'def', #Database implementation to use - only for testing
    'db_path':None, #Database save path
    'debug':False #Print debug information - only for testing
}

#Word equivalents in each supported language
FRENCH_DICT = {
    'key':'Clé',
    'phrase':'Phrase',
    'copy':'Copier',
    'save':'Enregistrer',
    'new':'Nouveau',
    'cancel':'Annuler',
    'language':'Langue',
    'show_buttons':'Montrer les boutons',
    'hide_buttons':'Cacher les boutons',
    'options':'Options',
    'display':'Affichage',
    'title':'Phrase/Clé'
}
ENGLISH_DICT = {
    'key':'Key',
    'phrase':'Phrase',
    'copy':'Copy',
    'save':'Save',
    'new':'New',
    'cancel':'Cancel',
    'language':'Language',
    'show_buttons':'Show buttons',
    'hide_buttons':'Hide buttons',
    'options':'Options',
    'display':'Display',
    'title':'Key/Phrase'
}
#Supported languages
LANGUAGE_DICT = {
    'Français':FRENCH_DICT,
    'English':ENGLISH_DICT
}

#Holds references to GUI objects while app is active
active_objects = { 
    'root':None,
}

def load_config():
    """ Loads config from disk or return default setting | None -> dict """
    try:
        with open('config/config.json', 'r') as config_file:
            config_dict = json.load(config_file)
            print('Loading saved configuration:', config_dict)
    except (FileNotFoundError, ValueError):
        print('Loading default configuration:', DEFAULT_CONFIG)
        config_dict = DEFAULT_CONFIG
    return config_dict

@atexit.register
def save_config():
    """ Saves current config to disk | None -> None """
    with open('config/config.json', 'w') as config_file:
        config_dict['initial_geometry'] = config_dict['current_geometry']
        print('Saving configuration:', config_dict)
        json.dump(config_dict, config_file)

def reset_config():
    """ Resets config to default and deletes saved config | None -> None """
    global config_dict
    config_dict = DEFAULT_CONFIG
    save_config()

def backup():
    """ Creates backup copy of config file | None -> None """
    shutil.copy2('config/config.json', 'config/config_bkup.json')

def restore():
    """ Restores backup of config file | None -> None """
    shutil.copy2('config/config_bkup.json', 'config/config.json')

def redraw():
    """ Redraw app window after config changes | None -> None """
    active_objects['root'].destroy()
    active_objects['root'].redraw()

def get_show_buttons():
    """ Get show_buttons bool from config_dict | None -> bool """
    return config_dict['show_buttons']
    
def get_mode():
    """ Get current mode from config_dict | None -> str """
    return config_dict['mode']

def set_mode(mode):
    """ Set current mode | str -> None """
    config_dict['mode'] = mode

def change_mode():
    """ Change database mode | None -> None

    'get' mode: retrieve entry from database
    'put' mode: add, modify or delete database entry
    """
    if config_dict['mode'] == 'get':
        print('Switching to put mode')
        active_objects['root'].main_frame.activate_put_mode()
        
    else:
        print('Switching to get mode')
        active_objects['root'].main_frame.activate_get_mode()
    
def set_language(language):
    """ Sets config to specific language and reloads interface | None -> None """
    print(language)
    config_dict['language'] = language
    print(config_dict)
    language_dict = get_language_dict()
    active_objects['root'].set_text()

def get_language_dict():
    """ Get language dict for active language | None -> dict """
    return LANGUAGE_DICT[config_dict['language']]

def show_buttons():
    """ Show buttons in GUI | None -> None """
    config_dict['show_buttons'] = True
    active_objects['root'].destroy()
    active_objects['root'].redraw()
    
def hide_buttons():
    """ Hide buttons in GUI | None -> None """
    config_dict['show_buttons'] = False
    active_objects['root'].destroy()
    active_objects['root'].redraw()

#Current user application settings
config_dict = load_config()

def get_config():
    """ Access config dict from outside module | None -> dict """
    return config_dict


def get_languages():
    """ Alphabetical list of supported languages | None -> list(str) """
    return sorted([key for key in LANGUAGE_DICT])

def set_db_path(db_path=None):
        """ Set db save folder, ask user if necessary | Optional(str) -> None """
        if not db_path:
            db_path = get_default_dir()
        config_dict['db_path'] = db_path

def get_db_path():
    """ Get database save path | None -> pathlib.Path """
    if config_dict['db_path']:
        return pathlib.Path(config_dict['db_path'])
    return None

def get_debug():
    """ Get debug bool from config_dict | None -> bool """
    return config_dict['debug']

def debug_mode():
    """ Switch debug mode on or off | None -> None """
    print(f'Before: {config_dict["debug"]}')
    config_dict['debug'] = not config_dict['debug']
    print(f'After: {config_dict["debug"]}')
