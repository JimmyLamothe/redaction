""" Tests for Database class

Tests not written for all methods. Add more as bugs arise.
"""

import random
import shutil
import pandas as pd
import numpy as np
import config

class Database():
    """ Abstract class """

    def __init__(self, name=None):
        self.name = name #Defined by subclasses
        self.undo_db_list = [] #Cleared after each session
        self.redo_db_list = [] #Cleared after each session
        self.db = self.load_database()
        
    def get_filepath(self):
        """ Get full filepath of database file | None -> Path """
        folder = config.get_db_path()
        extension = '.pickle'
        filename = self.name + extension
        filepath = folder / filename
        return filepath
        
    def load_database(self):
        """ Loads database from disk if it exists | None -> pd.DataFrame or None """
        try:
            db = pd.read_pickle(self.get_filepath())
            print('Loading saved key dataframe')
            print(db)
        except FileNotFoundError or AttributeError:
            print('No saved key dataframe')
            db = pd.DataFrame() #Initialize empty db
            db.to_pickle(self.get_filepath()) 
        return db

    def reload_database(self):
        """ Reload db from disk - used for undo and redo """
        self.db = self.load_database()

    def save(self):
        """ Save contents of database to disk | db.DataFrame -> None """
        self.db.to_pickle(self.get_filepath())

    def initialize_db(self, entry_1, entry_2):
        """ Create new database on first startup | -> pd.DataFrame """
        error_message = 'initialize_db must be overridden by subclass'
        raise NotImplementedError(error_message)

    def add_column_if_missing(self, name):
        """ Initializes column if it doesn't exist | str -> None """
        error_message = 'add_column_if_missing must be overridden by subclass'
        raise NotImplementedError(error_message)

    def save_entry(self, entry_1, entry_2):
        """ Save new combination to database | str, str -> None """
        error_message = 'save_entry must be overridden by subclass'
        raise NotImplementedError(error_message)
    
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
        db_filepath = self.get_filepath()
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
        db_filepath = self.get_filepath()
        filepath = self.generate_redo_filepath()
        shutil.copy(db_filepath, filepath)
        self.redo_db_list.append(filepath)
    
    def undo(self):
        """ Reverts previous database save command | None -> None """
        if not self.undo_db_list: #If no previous saved state
            return
        #Part 1: Save current state to temp backup
        self.prepare_redo()
        #Part 2: Revert previous save command
        db_filepath = self.get_filepath()
        revert_filepath = self.undo_db_list[-1]
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
        db_filepath = self.get_filepath()
        revert_filepath = self.redo_db_list[-1]
        shutil.copy(revert_filepath, db_filepath)
        self.redo_db_list.pop().unlink()
        self.reload_database()

    def __repr__(self):
        return self.db.__repr__()

    def __str__(self):
        return self.db.__str__()

class StandardDatabase(Database):
    """
    Database class for Key/Phrase combinations

    Keys form the column names.
    Phrases form the index.

    Values are booleans. True indicates a valid key / phrase match.
    """

    def __init__(self):
        Database.__init__(self, name='standard')

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
        self.db.to_pickle(self.get_filepath())

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
                    self.db.drop(phrase, inplace=True) #To delete phrase from database
                except KeyError:
                    return
            self.db.loc[phrase] = False #Initialize row with all False 
            for key in key_list:
                self.add_column_if_missing(key) #Add missing new keys 
            self.db.loc[phrase, key_list] = True #Set keys in key_list to True
            self.save()

    def delete_phrase(self, phrase):
        """ Delete phrase from database and unused keys | str, str -> None """
        self.db.drop(phrase, inplace=True)
        self.db = self.db.loc[:, self.db.any()]
        self.save()
            
    def get_phrase_series(self):
        """ Gets phrase Series from key DataFrame | None -> pd.Series """
        return self.db.index
            
    def get_phrase_list(self, key_list):
        """ Get list of valid phrases for a list of keys | list(str) -> list(str) """
        try:
            index = self.db.loc[self.db[key_list].all(axis=1), :].index
            return list(index.values)
        except KeyError:
            return None

    def get_matching_keys(self, phrase):
        """ Get matching keys for phrase if any | str -> list(str) """
        try:
            return list(self.db.loc[phrase,self.db.loc[phrase,:]].index)
        except KeyError:
            return []
        
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

class TranslationDatabase(StandardDatabase):
    """
    Database class for language pair databases.

    Language 1 keys form the column names.
    Language 2 keys from the index.

    Values are booleans. True indicates a valid translation.
    """

    def __init__(self, lang1, lang2):
        """ Initialize translation database | str, str -> None

        NOTE: On initial creation, check if file exists. If so,
        confirm user really wants to replace the existing database
        """
        name = lang1 + '_' + lang2
        Database.__init__(self, name)

    def add_column_if_missing(self, key_lang1):
        """ Initializes column if it doesn't exist | str, pd.DataFrame -> None """
        if not key_lang1 in self.db.columns:
            self.db[key_lang1] = False

    def initialize_db(self, key_lang1, key_lang2):
        """ Create new database on first entry | str, str -> pd.DataFrame """
        print('Initializing database')
        self.db = pd.DataFrame.from_dict({key_lang2:[True]},
                                         orient='index',
                                         columns=[key_lang1])
        self.db.to_pickle(self.get_filepath())

    def save_entry(self, key_lang1, key_lang2):
        """ Save new translation to database | str, str -> None """
        if not key_lang1 or not key_lang2: #To prevent accidental empty entry
            return
        if self.db.empty: #If first entry, initialize new database
            self.initialize_db(key_lang1, key_lang2)
            self.save_entry(key_lang1, key_lang2)
        else:
            print('Found DataFrame')
            if not key_lang2 in self.db.index:
                self.db.loc[key_lang2] = False #Initialize row with all False 
            self.add_column_if_missing(key_lang1) #Add missing new key 
            self.db.loc[key_lang2, key_lang1] = True #Set key in key_lang1 to True
            self.save()

    def delete_match(self, key_lang1, key_lang2):
        """ Delete translation match from database | str, str -> None """
        self.db.loc[key_lang2, key_lang1] = False
        self.db = self.db.loc[:, self.db.any()]
        self.db = self.db.loc[self.db.any(axis=1),:]
        self.save()

    def get_lang1_keys(self):
        """ Gets list of keys for language 1 | None -> np.Array """
        return list(self.db.columns.values)
            
    def get_lang2_keys(self):
        """ Gets list of keys for language 2 | None -> np.Array """
        return list(self.db.index.values)
            
    def get_lang1_matches(self, key_lang2):
        """ Get list of valid translations for language 2 key | str -> list(str) """
        try:
            row = self.db.loc[key_lang2.lower(), :]
            return list(row[row==True].index)
        except KeyError:
            try:
                row = self.db.loc[key_lang2.title(), :]
                return list(row[row==True].index)
            except KeyError:
                return []

    def get_lang2_matches(self, key_lang1):
        """ Get list of valid translations for language 1 key | str -> list(str) """
        try:
            index = self.db.loc[self.db[key_lang1.lower()], :].index
            return list(index.values)
        except KeyError:
            try:
                index = self.db.loc[self.db[key_lang1.title()], :].index
                return list(index.values)
            except KeyError:
                return []

    def valid_lang1_keys(self, partial_key):
        """ Get list of language 1 keys starting with string | str -> list(str) """
        if partial_key:
            mask = self.db.columns.str.lower().str.startswith(partial_key.lower())
            return list(self.db.columns[mask])
        return []

    def valid_lang2_keys(self, partial_key):
        """ Get list of language 2 keys starting with string | str -> list(str) """
        if partial_key:
            mask = self.db.index.str.lower().str.startswith(partial_key.lower())
            return list(self.db.index[mask])
        return []
