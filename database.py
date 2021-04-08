""" Main database logic for Key/Phrase

Implements all the logic related to database queries and storage.

Presently, the database is implemented as a Pandas dataframe. Alternative
database implementations can be tested as 'database_alt.py' with the
'speedtest.py' script.

Database variable:
    db

Functions:
    load_database() -> pd.DataFrame
    get_phrase_series() -> pd.Series
    save(pd.DataFrame)
    add_column_if_missing(string, pd.DataFrame)
    initialize_db(list, string) -> pd.DataFrame
    save_entry(list, string)
    get_phrase_list(list) -> list
    valid_keys(string) -> list
    get_words(list, int, int) -> list
    generate_key_list(list) -> list
    generate_phrase(list) -> string
    generate_test_db(kwargs: str, int)
"""

import random
import pandas as pd
import numpy as np
import config
from utilities import get_default_dir

def get_full_db_path():
    """ Returns full path to db including filename | None -> str """
    folder = config.get_db_path()
    file_name = 'key.pickle'
    return folder / file_name

def load_database():
    """ Loads database from disk if it exists | None -> pd.DataFrame or None """
    try:
        db = pd.read_pickle(get_full_db_path())
        print('Loading saved key dataframe')
        print(db)
    except FileNotFoundError:
        print('No saved key dataframe')
        db = None
    return db

db = load_database() #The application database (Pandas DataFrame)

def get_phrase_series():
    """ Gets phrase Series from key DataFrame | None -> pd.Series """
    return db.index

def save():
    """ Save contents of database to disk | db.DataFrame -> None """
    global db
    db.to_pickle(get_full_db_path())
    
def add_column_if_missing(name):
    """ Initializes column if it doesn't exist | str, pd.DataFrame -> None """
    global db
    if not name in db.columns:
        db[name] = False

def initialize_db(key_list, phrase):
    """ Create new database on first saved entry | list(str), str -> pd.DataFrame """
    print('Initializing DataFrame')
    global db
    row_data = []
    for i in range(len(key_list)):
        row_data.append(True)
    db = pd.DataFrame.from_dict({phrase:row_data},
                                    orient='index',
                                    columns=key_list)
    #get_full_db_path().touch(exists_ok=True) #Create file if necessary
    save()

def save_entry(key_list, phrase):
    """ Save new key/phrase combination to database | list(str), str -> None """
    global db
    if not phrase: #To prevent accidental empty phrase entry
        return
    if db is None: #If first entry, initialize new database
        initialize_db(key_list, phrase)
        save_entry(key_list, phrase)
    else:
        print('Found DataFrame')
        if not key_list: #If no keys given
            db = db.drop(phrase) #Used to delete phrase from database
        db.loc[phrase] = False #Initialize row with all False 
        for key in key_list:
            add_column_if_missing(key) #Add missing new keys 
        db.loc[phrase, key_list] = True #Set keys in key_list to True
        save()

def get_phrase_list(key_list):
    """ Get list of valid phrases for a list of keys | list(str) -> list(str) """
    try:
        index = db.loc[db[key_list].all(axis=1), :].index
        return list(index.values)
    except KeyError:
        return None

def valid_keys(partial_key):
    """ Get list of db keys starting with specific string | str -> list(str) """
    if partial_key:
        mask = db.columns.str.lower().str.startswith(partial_key.lower())
        return list(db.columns[mask])
    return []

def valid_phrases(partial_phrase):
    """ Get list of db phrases starting with specific string | str -> list(str) """
    if partial_phrase:
        return list(db.index[db.index.str.startswith(partial_phrase)])
    return []

def saved_keys(phrase):
    """ Get list of db keys for specific phrase | None -> list(str) """
    try:
        row = db.loc[phrase, :]
        return list(row[row==True].index)
    except KeyError:
        return []

def get_words(word_list, minimum, maximum):
    """ Get random words from word list | list(str), int, int -> list(str) """
    total = random.randint(minimum, maximum) #Total words to return
    result = []
    for i in range(total):
        result.append(random.choice(word_list))
    return result

def generate_key_list(word_list):
    """ Get random words for sample key list | list(str) -> list(str) """
    return get_words(word_list, 1, 3)

def generate_phrase(word_list):
    """ Get random words for sample phrase string | list(str) -> str """
    return ' '.join(get_words(word_list, 8, 30))

def generate_test_db(language='fr', size=500):
    """ Adds random key/phrase entries to a test db | None -> None """
    if language == 'fr':
        with open('language/mots.txt', 'r') as f:
            word_list = f.read().splitlines()
    elif language == 'en':
        with open('/usr/share/dict/words', 'r') as f:
            word_list = f.read().splitlines()
    for i in range(size):
        print(f'Generating entry {i+1} of {size}')
        save_entry(generate_key_list(word_list),
                   generate_phrase(word_list))
    print(db)
