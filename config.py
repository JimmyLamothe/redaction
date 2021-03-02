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
import json
from json.decoder import JSONDecodeError

#Default configuration on first execution or config reset
DEFAULT_CONFIG = {
    'initial_geometry':'',
    'current_geometry':'',
    'default_size':'600x250',
    'show_buttons':True,
    'language':'Français',
    'db':'def'
}

#Word equivalents in each supported language
FRENCH_DICT = {
    'key':'Clé',
    'phrase':'Phrase',
    'copy':'Copier',
    'save':'Ajouter',
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
    'root':None
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
    
def set_language(language):
    """ Sets config to specific language and reloads interface | None -> None """
    print(language)
    config_dict['language'] = language
    print(config_dict)
    active_objects['root'].destroy()
    active_objects['root'].redraw()

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
