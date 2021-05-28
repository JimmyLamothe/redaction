""" Tests for Database class

Tests not written for all methods. Add more as bugs arise.
"""
import pytest
import config
from Databases import StandardDatabase, TranslationDatabase

reference_standard_filepath = StandardDatabase().get_filepath()

reference_translation_filepath = TranslationDatabase('français', 'anglais').get_filepath()

def get_standard_test_filepath(*args): #will replace instance method
    folder = config.get_db_path()
    extension = '.pickle'
    filename = 'test_standard_db' + extension
    filepath = folder / filename
    return filepath

@pytest.fixture(autouse=True)
def mock_get_standard_filepath(monkeypatch):
    """ Get filepath of standard test database file | None -> Path """
    monkeypatch.setattr(StandardDatabase, 'get_filepath', get_standard_test_filepath)

def get_translation_test_filepath(*args): #will replace instance method
    folder = config.get_db_path()
    extension = '.pickle'
    filename = 'test_translation_db' + extension
    filepath = folder / filename
    return filepath
    
@pytest.fixture(autouse=True)
def mock_get_translation_filepath(monkeypatch):
    """ Get filepath of translation test database file | None -> Path """
    monkeypatch.setattr(TranslationDatabase, 'get_filepath',
                        get_translation_test_filepath)
    
def delete_standard_test_db():
    test_db = get_standard_test_filepath()
    try:
        test_db.unlink()
        print('deleted standard test db')
    except FileNotFoundError:
        print('No standard test db to delete')

def delete_translation_test_db():
    test_db = get_translation_test_filepath()
    try:
        test_db.unlink()
        print('deleted translation test db')
    except FileNotFoundError:
        print('No translation test db to delete')

def delete_test_db(func):
    """ Decorator to delete test dbs after testing | func -> func """
    def decorator(*args, **kwargs):
        try:
            func(*args, **kwargs)
        finally:
            delete_standard_test_db()
            delete_translation_test_db()
    return decorator

def get_index(db):
    return list(db.db.index.values)

def get_columns(db):
    return list(db.db.columns.values)

def compare_db(db1, db2):
    if get_index(db1) == get_index(db2):
        if get_columns(db1) == get_columns(db2):
            return True
    return False

def standard_test_db():
    test_db = StandardDatabase()
    test_db.save_entry(['a','b'],'phrase 1')
    test_db.save_entry(['c','d'],'phrase 2')
    return test_db

@delete_test_db
def test_standard_save_entry():
    test_db = standard_test_db()
    assert get_index(test_db) == ['phrase 1','phrase 2']
    assert get_columns(test_db) == ['a','b','c','d']
    test_db.save_entry([],'phrase 2')
    assert get_index(test_db) == ['phrase 1']
    assert get_columns(test_db) == ['a','b']
    test_db.save_entry([], 'not_in_db')
    assert get_index(test_db) == ['phrase 1']
    assert get_columns(test_db) == ['a','b']
    test_db.save_entry(['key_1', 'a', 'key_2'], 'new_phrase')
    assert get_index(test_db) == ['phrase 1', 'new_phrase']
    assert get_columns(test_db) == ['a','b', 'key_1', 'key_2']

@delete_test_db
def test_standard_delete_phrase():
    test_db = standard_test_db()
    assert get_index(test_db) == ['phrase 1','phrase 2']
    assert get_columns(test_db) == ['a','b','c','d']
    test_db.delete_phrase('')
    assert get_index(test_db) == ['phrase 1','phrase 2']
    assert get_columns(test_db) == ['a','b','c','d']
    test_db.delete_phrase('afgasdfg')
    assert get_index(test_db) == ['phrase 1','phrase 2']
    assert get_columns(test_db) == ['a','b','c','d']
    test_db.delete_phrase('phrase 1')
    assert get_index(test_db) == ['phrase 2']
    assert get_columns(test_db) == ['c','d']

@delete_test_db
def test_standard_get_phrase_list():
    test_db = standard_test_db()
    assert test_db.get_phrase_list([]) == None
    assert test_db.get_phrase_list(['a']) == ['phrase 1']
    assert test_db.get_phrase_list(['c']) == ['phrase 2']
    assert test_db.get_phrase_list(['a','b']) == ['phrase 1']
    assert test_db.get_phrase_list(['a','c']) == None
    assert test_db.get_phrase_list(['e','f']) == None

@delete_test_db
def test_standard_get_matching_keys():
    test_db = standard_test_db()
    assert test_db.get_matching_keys('') == []
    assert test_db.get_matching_keys('phrase 1') == ['a','b']
    assert test_db.get_matching_keys('phrase 2') == ['c','d']
    assert test_db.get_matching_keys('afgasfgasdfg') == []

@delete_test_db    
def test_standard_valid_keys():
    test_db = standard_test_db()
    test_db.save_entry(['allo_allo', 'zenitude'], 'phrase 3')
    assert test_db.valid_keys('f') == []
    assert test_db.valid_keys('b') == ['b']
    assert test_db.valid_keys('a') == ['a', 'allo_allo']
    assert test_db.valid_keys('A') == ['a', 'allo_allo']
    assert test_db.valid_keys('zen') == ['zenitude']
    assert test_db.valid_keys('allo_allo') == ['allo_allo']
    assert test_db.valid_keys('') == []

@delete_test_db    
def test_standard_valid_phrases():
    test_db = standard_test_db()
    test_db.save_entry(['a'], 'Bla bla \n bla bla')
    assert test_db.valid_phrases('p') == ['phrase 1', 'phrase 2']
    assert test_db.valid_phrases('r') == []
    assert test_db.valid_phrases('phrase ') == ['phrase 1', 'phrase 2']
    assert test_db.valid_phrases('phrase 1') == ['phrase 1']
    assert test_db.valid_phrases('B') == ['Bla bla \n bla bla']
    assert test_db.valid_phrases('') == []

def _test_translation_save_entry(self, key_lang1, key_lang2):
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

def _test_translation_delete_match(self, key_lang1, key_lang2):
    """ Delete translation match from database | str, str -> None """
    self.db.loc[key_lang2, key_lang1] = False
    self.db = self.db.loc[:, self.db.any()]
    self.db = self.db.loc[self.db.any(axis=1),:]
    self.save()

def _test_translation_get_lang1_keys(self):
    """ Gets list of keys for language 1 | None -> np.Array """
    return list(self.db.columns.values)

def _test_translation_get_lang2_keys(self):
    """ Gets list of keys for language 2 | None -> np.Array """
    return list(self.db.index.values)

def _test_translation_get_lang1_matches(self, key_lang2):
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

def _test_translation_get_lang2_matches(self, key_lang1):
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

def _test_translation_valid_lang1_keys(self, partial_key):
    """ Get list of language 1 keys starting with string | str -> list(str) """
    if partial_key:
        mask = self.db.columns.str.lower().str.startswith(partial_key.lower())
        return list(self.db.columns[mask])
    return []

def _test_translation_valid_lang2_keys(self, partial_key):
    """ Get list of language 2 keys starting with string | str -> list(str) """
    if partial_key:
        mask = self.db.index.str.lower().str.startswith(partial_key.lower())
        return list(self.db.index[mask])
    return []

