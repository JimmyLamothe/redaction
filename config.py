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
from tkinter import filedialog
from utilities import get_default_dir, get_default_backup, get_default_session

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
    'backup_path':None, #Database backup path
    'session_path':None, #Session save path
    'db_type':'standard', #Database type ('standard' or 'translation')
    'language_pair': None, #Active language pair tuple if translation db active
    'show_tutorial':True, #Show tutorial on startup
    'tutorials_remaining':3, #Number of times to show tutorial on startup
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
    'title':'Phrase/Clé',
    'tutorial':'language/tutorial_FR.txt'
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
    'title':'Key/Phrase',
    'tutorial':'language/tutorial_EN.txt'
}
#Supported languages
LANGUAGE_DICT = {
    'Français':FRENCH_DICT,
    'English':ENGLISH_DICT
}

#Holds references to common-use objects while app is active
active_objects = { 
    'root':None,
    'db':None
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

#Current user application settings
config_dict = load_config()

def get_config():
    """ Access config dict from outside module | None -> dict """
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

def get_db_type():
    """ Get db type from config_dict | None -> bool """
    return config_dict['db_type']

def set_db_type(setting):
    """ Set db type ('standard' or 'translation') | str -> None """
    config_dict['db_type'] = setting
    
def get_lang1():
    """ Get language 1 from active language pair | None -> bool """
    return config_dict['language_pair'][0]

def get_lang2():
    """ Get language2 from active language pair | None -> bool """
    return config_dict['language_pair'][1]

def set_language_pair(language_pair):
    """ Sets db to language pair | list -> None """
    config_dict['language_pair'] = language_pair

def get_show_buttons():
    """ Get show_buttons bool from config_dict | None -> bool """
    return config_dict['show_buttons']

def get_show_tutorial():
    """ Get show_tutorial bool from config_dict | None -> bool """
    return config_dict['show_tutorial']

def decrement_tutorial():
    """ Decrement number of times to show tutorial | None -> None """
    config_dict['tutorials_remaining'] -= 1
    if config_dict['tutorials_remaining'] < 1:
        config_dict['show_tutorial'] = False
        config_dict['show_tutorial'] = 0

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

def get_languages():
    """ Alphabetical list of supported languages | None -> list(str) """
    return sorted([key for key in LANGUAGE_DICT])

def set_db_path(db_path=None):
    """ Set db save folder, creating if necessary | optional:Path -> None """
    if not db_path:
        db_path = get_default_dir()
    config_dict['db_path'] = str(db_path)

def get_db_path():
    """ Get database save path | None -> pathlib.Path """
    if config_dict['db_path']:
        return pathlib.Path(config_dict['db_path'])
    return None #NOTE: On startup set_db_path will be called if this is returned

def get_full_db_path():
    """ Returns full path to db including filename | None -> str """
    folder = get_db_path()
    file_name = 'key.pickle'
    return folder / file_name

def set_backup_path(backup_path=None):
    """ Sets backup directory, creating if necessary | optional:Path -> None """
    if not backup_path:
        backup_path = get_default_backup()
    elif backup_path == 'ask':
        backup_path = filedialog.askdirectory()
    config_dict['backup_path'] = str(backup_path)

def get_backup_path():
    """ Get database backup path | None -> Path """
    if config_dict['backup_path']:
        return pathlib.Path(config_dict['backup_path'])
    return None #NOTE: On startup set_backup_path will be called if this is returned

def set_session_path(session_path=None):
    """ Sets session directory, creating if necessary | optional:Path -> None """
    if not session_path:
        session_path = get_default_session()
    config_dict['session_path'] = str(session_path)
    
def get_session_path():
    """ Get path to session database save states | None -> Path """
    if config_dict['session_path']:
        return pathlib.Path(config_dict['session_path'])
    return None #NOTE: On startup set_session_path will be called if this is returned

def get_debug():
    """ Get debug bool from config_dict | None -> bool """
    return config_dict['debug']

def debug_mode():
    """ Switch debug mode on or off | None -> None """
    print(f'Before: {config_dict["debug"]}')
    config_dict['debug'] = not config_dict['debug']
    print(f'After: {config_dict["debug"]}')

@atexit.register
def clear_session():
    session_path = get_session_path()
    for f in session_path.iterdir():
        f.unlink()
