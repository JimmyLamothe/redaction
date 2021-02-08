import atexit
import json

active_objects = { #Holds references to import GUI objects while app is active
    'root':None
}

def load_config():
    try:
        with open('config/config.json', 'r') as config_file:
            config_dict = json.load(config_file)
            print('Loading saved configuration:', config_dict)
    except FileNotFoundError:
        print('Loading default configuration:', config_dict)
        config_dict = DEFAULT_CONFIG
    return config_dict

@atexit.register
def save_config():
    with open('config/config.json', 'w') as config_file:
        config_dict['initial_geometry'] = config_dict['current_geometry']
        print('Saving configuration:', config_dict)
        json.dump(config_dict, config_file)

def reset_config():
    global config_dict
    config_dict = DEFAULT_CONFIG
    save_config()

def set_language(language):
    print(language)
    config_dict['language'] = language
    print(config_dict)
    active_objects['root'].destroy()
    active_objects['root'].redraw()

def get_language_dict():
    return LANGUAGE_DICT[config_dict['language']]

def show_buttons():
    config_dict['show_buttons'] = True
    active_objects['root'].destroy()
    active_objects['root'].redraw()

def hide_buttons():
    config_dict['show_buttons'] = False
    active_objects['root'].destroy()
    active_objects['root'].redraw()

#Configurable settings - Only default size and language is set on first execution
config_dict = load_config()

def get_config():
    return config_dict

DEFAULT_CONFIG = {
    'initial_geometry':'',
    'current_geometry':'',
    'default_size':'600x250',
    'show_buttons':True,
    'language':'Français',
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

def get_languages():
    return sorted([key for key in LANGUAGE_DICT])
