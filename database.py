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

def load_database():
    """ Loads database from disk if it exists | None -> pd.DataFrame or None """
    try:
        db = pd.read_pickle('database/key.pickle')
        print('Loading saved key dataframe')
        print(db.head())
    except FileNotFoundError:
        print('No saved key dataframe')
        db = None
    return db

def get_phrase_series():
    """ Gets phrase Series from key DataFrame | None -> pd.Series """
    return db.index

db = load_database() #The application database (Pandas DataFrame)

def save(db):
    """ Save contents of database to disk | db.DataFrame -> None """
    db.to_pickle('database/key.pickle')
    
def add_column_if_missing(name, db):
    """ Initializes column if it doesn't exist | str, pd.DataFrame -> None """
    if not name in db.columns:
        db[name] = False

def initialize_db(key_list, phrase):
    """ Create new database on first saved entry | list(str), str -> pd.DataFrame """
    print('Initializing DataFrame')
    row_data = []
    for i in range(len(key_list)):
        row_data.append(True)
    global db
    db = pd.DataFrame.from_dict({phrase:row_data},
                                    orient='index',
                                    columns=key_list)
    return db

def save_entry(key_list, phrase, db=db):
    """ Save new key/phrase combination to database | list(str), str -> None """
    if not phrase: #To prevent accidental empty phrase entry
        return
    if db is None: #If first entry, initialize new database
        db = initialize_db(key_list, phrase)
        save_entry(key_list, phrase, db=db)
        
    else:
        print('Found DataFrame')
        if not key_list: #If no keys given
            db = db.drop(phrase) #Used to delete phrase from database
        db.loc[phrase] = False #Initialize row with all False 
        for key in key_list:
            add_column_if_missing(key, db) #Add missing new keys 
        db.loc[phrase, key_list] = True #Set keys in key_list to True
        save(db)
    
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
                   generate_phrase(word_list),
                   db=db)
    print(db)
