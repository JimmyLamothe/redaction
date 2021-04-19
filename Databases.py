""" Database classes for Key/Phrase

Implements all the logic related to database queries and storage.

Presently, databases are implemented as Pandas dataframes. It might eventually
be better to convert it to a form of SQL.

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
import shutil
import pandas as pd
import numpy as np
import config

class StandardDatabase():
    """
    This is the base class for the Key/Phrase database.
    """

    def __init__(self):
        self.db = self.load_database()
        self.undo_db_list = [] #Cleared after each session
        self.redo_db_list = [] #Cleared after each session

    def load_database(self):
        """ Loads database from disk if it exists | None -> pd.DataFrame or None """
        try:
            db = pd.read_pickle(config.get_full_db_path())
            print('Loading saved key dataframe')
            print(db)
        except FileNotFoundError:
            print('No saved key dataframe')
            db = pd.DataFrame() #Initialize empty db
            db.to_pickle(config.get_full_db_path()) 
        return db

    def reload_database(self):
        """ Reload db from disk - used for undo and redo """
        self.db = load_database()

    def get_phrase_series(self):
        """ Gets phrase Series from key DataFrame | None -> pd.Series """
        return self.db.index

    def save(self):
        """ Save contents of database to disk | db.DataFrame -> None """
        self.db.to_pickle(config.get_full_db_path())
    
    def add_column_if_missing(self, name):
        """ Initializes column if it doesn't exist | str, pd.DataFrame -> None """
        if not name in self.db.columns:
            self.db[name] = False

    def initialize_db(self, key_list, phrase):
        """ Create new database on first startup | list(str), str -> pd.DataFrame """
        print('Initializing database')
        row_data = []
        for i in range(len(key_list)):
            row_data.append(True)
        self.db = pd.DataFrame.from_dict({phrase:row_data},
                                         orient='index',
                                         columns=key_list)
        self.db.to_pickle(config.get_full_db_path())

    def save_entry(self, key_list, phrase):
        """ Save new key/phrase combination to database | list(str), str -> None """
        if not phrase: #To prevent accidental empty phrase entry
            return
        if self.db.empty: #If first entry, initialize new database
            self.initialize_db(key_list, phrase)
            self.save_entry(key_list, phrase)
        else:
            print('Found DataFrame')
            if not key_list: #If no keys given
                try:
                    self.db = db.drop(phrase) #Used to delete phrase from database
                except KeyError:
                    return
            self.db.loc[phrase] = False #Initialize row with all False 
            for key in key_list:
                self.add_column_if_missing(key) #Add missing new keys 
            self.db.loc[phrase, key_list] = True #Set keys in key_list to True
            self.save()

    def get_phrase_list(self, key_list):
        """ Get list of valid phrases for a list of keys | list(str) -> list(str) """
        try:
            index = self.db.loc[self.db[key_list].all(axis=1), :].index
            return list(index.values)
        except KeyError:
            return None

    def valid_keys(self, partial_key):
        """ Get list of db keys starting with specific string | str -> list(str) """
        if partial_key:
            mask = self.db.columns.str.lower().str.startswith(partial_key.lower())
            return list(self.db.columns[mask])
        return []

    def valid_phrases(self, partial_phrase):
        """ Get list of db phrases starting with specific string | str -> list(str) """
        if partial_phrase:
            return list(self.db.index[self.db.index.str.startswith(partial_phrase)])
        return []

    def saved_keys(self, phrase):
        """ Get list of db keys for specific phrase | None -> list(str) """
        try:
            row = self.db.loc[phrase, :]
            return list(row[row==True].index)
        except KeyError:
            return []

    @staticmethod
    def get_words(word_list, minimum, maximum):
        """ Get random words from word list | list(str), int, int -> list(str) """
        total = random.randint(minimum, maximum) #Total words to return
        result = []
        for i in range(total):
            result.append(random.choice(word_list))
        return result

    @staticmethod
    def generate_key_list(word_list):
        """ Get random words for sample key list | list(str) -> list(str) """
        return Database.get_words(word_list, 1, 3)

    @staticmethod
    def generate_phrase(word_list):
        """ Get random words for sample phrase string | list(str) -> str """
        return ' '.join(Database.get_words(word_list, 8, 30))

    def generate_test_db(self, language='fr', size=500):
        """ Adds random key/phrase entries to a test db | None -> None """
        if language == 'fr':
            with open('language/mots.txt', 'r') as f:
                word_list = f.read().splitlines()
        elif language == 'en':
            with open('/usr/share/dict/words', 'r') as f:
                word_list = f.read().splitlines()
        for i in range(size):
            print(f'Generating entry {i+1} of {size}')
            self.save_entry(Database.generate_key_list(word_list),
                            Database.generate_phrase(word_list))
        print(self.db)

    def generate_undo_filepath(self):
        """ Generate filepath for undo file | None -> Path """
        session_path = config.get_session_path()
        name = 'undo_' + str(len(self.undo_db_list)) + '.pickle'
        filepath = session_path / name
        return filepath

    def prepare_undo(self):
        """ Saves current db state to undo file and saves path | None -> None """
        db_filepath = config.get_full_db_path()
        filepath = self.generate_undo_filepath()
        shutil.copy(db_filepath, filepath)
        self.undo_db_list.append(filepath)

    def generate_redo_filepath(self):
        """ Generate filepath for redo file | None -> Path """
        session_path = config.get_session_path()
        name = 'redo_' + str(len(self.redo_db_list)) + '.pickle'
        filepath = session_path / name 
        return filepath

    def prepare_redo(self):
        """ Saves current db state to redo file and saves path | None -> None """
        db_filepath = config.get_full_db_path()
        filepath = generate_redo_filepath()
        shutil.copy(db_filepath, filepath)
        self.redo_db_list.append(filepath)
    
    def undo(self):
        """ Reverts previous database save command | None -> None """
        if not self.undo_db_list: #If no previous saved state
            return
        #Part 1: Save current state to temp backup
        self.prepare_redo()
        #Part 2: Revert previous save command
        db_filepath = config.get_full_db_path()
        revert_filepath = undo_db_list[-1]
        shutil.copy(revert_filepath, db_filepath)
        self.undo_db_list.pop().unlink()
        self.reload_database()
    
    def redo(self):
        """ Reverts previous undo call | None -> None """
        if not self.redo_db_list: # If no undo in memory
            return
        #Part 1: Save current state to temp backup
        self.prepare_undo()
        #Part 2: Revert previous undo command
        db_filepath = config.get_full_db_path()
        revert_filepath = redo_db_list[-1]
        shutil.copy(revert_filepath, db_filepath)
        self.redo_db_list.pop().unlink()
        self.reload_database()

    def __repr__(self):
        return self.db.__repr__()

    def __str__(self):
        return self.db.__str__()
