""" Main database logic for Key/Phrase

Implements all the logic related to database queries and storage.

Presently, the database is implemented as a Pandas dataframe. Alternative
database implementations can be tested as 'database_alt.py' with the
'speedtest.py' script.

Database variable:
    key_df

Functions:
    load_key_dataframe() -> pd.DataFrame
    get_phrase_series() -> pd.Series
    save(pd.DataFrame)
    add_column_if_missing(string, pd.DataFrame)
    initialize_key_df(list, string) -> pd.DataFrame
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

def load_key_dataframe():
    """ Loads key DataFrame from disk if it exists | None -> pd.DataFrame or None """
    try:
        key_df = pd.read_pickle('database/key.pickle')
        print('Loading saved key dataframe')
    except FileNotFoundError:
        print('No saved key dataframe')
        key_df = None
    return key_df

def get_phrase_series():
    """ Gets phrase Series from key DataFrame | None -> pd.Series """
    return key_df.index

key_df = load_key_dataframe() #The application database (Pandas DataFrame)

def save(key_df):
    """ Save contents of database to disk | df.DataFrame -> None """
    key_df.to_pickle('database/key.pickle')
    
def add_column_if_missing(name, df):
    """ Initializes column if it doesn't exist | str, pd.DataFrame -> None """
    if not name in df.columns:
        df[name] = False

def initialize_key_df(key_list, phrase):
    """ Create new database on first saved entry | list(str), str -> pd.DataFrame """
    print('Initializing DataFrame')
    row_data = []
    for i in range(len(key_list)):
        row_data.append(True)
    global key_df
    key_df = pd.DataFrame.from_dict({phrase:row_data},
                                    orient='index',
                                    columns=key_list)
    return key_df

def save_entry(key_list, phrase, key_df=key_df):
    """ Save new key/phrase combination to database | list(str), str -> None """
    if key_df is None: #If first entry, initialize new database
        key_df = initialize_key_df(key_list, phrase)
        save_entry(key_list, phrase, key_df=key_df)
    else:
        print('Found DataFrame')
        key_df.loc[phrase] = False #Initialize row with all False 
        for key in key_list:
            add_column_if_missing(key, key_df) #Add missing new keys 
        key_df.loc[phrase, key_list] = True #Set keys in key_list to True
        save(key_df)
    
def get_phrase_list(key_list):
    """ Get list of valid phrases for a list of keys | list(str) -> list(str) """
    try:
        index = key_df.loc[key_df[key_list].all(axis=1), :].index
        return list(index.values)
    except KeyError:
        return None

def valid_keys(partial_key):
    """ Get list of db keys starting with specific string | str -> list(str) """
    if partial_key:
        mask = key_df.columns.str.lower().str.startswith(partial_key.lower())
        return list(key_df.columns[mask])
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
                   key_df=key_df)
    print(key_df)
