""" Tests for Database class

Tests not written for all methods. Add more as bugs arise.
"""
import shutil
import pytest
import config
from Databases import StandardDatabase, TranslationDatabase

original_standard_filepath = StandardDatabase().get_filepath()

original_translation_filepath = TranslationDatabase('français', 'anglais').get_filepath()

@pytest.fixture(autouse=True)
def mock_get_standard_filepath(monkeypatch):
    """ Get filepath of standard test database file | None -> Path """
    def get_test_filepath(self):
        folder = config.get_db_path()
        extension = '.pickle'
        filename = 'test_standard_db' + extension
        filepath = folder / filename
        return filepath

    monkeypatch.setattr(StandardDatabase, 'get_filepath', get_test_filepath)

@pytest.fixture(autouse=True)
def mock_get_translation_filepath(monkeypatch):
    """ Get filepath of translation test database file | None -> Path """
    def get_test_filepath(self):
        folder = config.get_db_path()
        extension = '.pickle'
        filename = 'test_translation_db' + extension
        filepath = folder / filename
        return filepath

    monkeypatch.setattr(TranslationDatabase, 'get_filepath', get_test_filepath)

def restore_standard_db(test_db):
    shutil.copy2(original_standard_filepath, test_db.get_filepath())

def restore_translation_filepath(test_db):
    shutil.copy2(original_translation_filepath, test_db.get_filepath())
    
def test_standard_get_filepath():
    test_db = StandardDatabase()
    expected_output = '/Users/jimmy/Library/Application Support/KeyPhrase/db/'
    expected_output += 'test_standard_db.pickle'
    assert str(test_db.get_filepath()) == expected_output
 
def test_translation_get_filepath():
    test_db = TranslationDatabase('lang1', 'lang2')
    expected_output = '/Users/jimmy/Library/Application Support/KeyPhrase/db/'
    expected_output += 'test_translation_db.pickle'
    assert str(test_db.get_filepath()) == expected_output

def get_index(db):
    return list(db.index.values)

def get_columns(db):
    return list(db.columns.values)

def test_standard_save_entry():
    test_db = StandardDatabase()
    pre_index = get_index(test_db.db)
    pre_columns = get_columns(test_db.db)
    test_db.save_entry(['key1', 'key2'], '')
    assert pre_index == get_index(test_db.db)
    assert pre_columns == get_columns(test_db.db)
    return
    if self.db.empty: #If first entry, initialize new database
        self.initialize_db(key_list, phrase)
        self.save_entry(key_list, phrase)
    test_db.save_entry([],'baba')
    assert [key for key in pre_columns
            if not key == 'baba'] == get_columns(test_db.db)
    test_db.save_entry([], 'not_in_db')
    assert pre_columns == get_columns(test_db.db)
    test_db.save_entry(['a', 'voila', 'new_key'], 'new_phrase')
    assert pre_columns + ['new_phrase'] == get_columns(test_db.db)
    assert pre_index + ['new_key'] == get_index(test_db.db)
    assert test_db.get_matching_keys('new_phrase') == ['a', 'voila', 'new_key']
    restore_standard_db(test_db)
    
def test_standard_delete_phrase():
    test_db = StandardDatabase()
    pre_index = get_index(test_db.db)
    pre_columns = get_columns(test_db.db)
    test_db.delete_phrase('baba')
    assert pre_index == get_index(test_db.db) + ['a']
    assert pre_columns == ['baba'] + get_columns(test_db.db)

def test_restore_standard_db():
    """ Not a real test, just to restore db after tests """
    restore_standard_db(StandardDatabase())
    assert True
    
def _test_standard_get_phrase_series(self):
    """ Gets phrase Series from key DataFrame | None -> pd.Series """
    return self.db.index

def _test_standard_get_phrase_list(self, key_list):
    """ Get list of valid phrases for a list of keys | list(str) -> list(str) """
    try:
        index = self.db.loc[self.db[key_list].all(axis=1), :].index
        return list(index.values)
    except KeyError:
        return None

def _test_standard_get_matching_keys(self, phrase):
    """ Get matching keys for phrase if any | str -> list(str) """
    try:
        return list(self.db.loc[phrase,self.db.loc[phrase,:]].index)
    except KeyError:
        return []

def _test_standard_valid_keys(self, partial_key):
    """ Get list of db keys starting with specific string | str -> list(str) """
    if partial_key:
        mask = self.db.columns.str.lower().str.startswith(partial_key.lower())
        return list(self.db.columns[mask])
    return []

def _test_standard_valid_phrases(self, partial_phrase):
    """ Get list of db phrases starting with specific string | str -> list(str) """
    if partial_phrase:
        return list(self.db.index[self.db.index.str.startswith(partial_phrase)])
    return []

def _test_standard_saved_keys(self, phrase):
    """ Get list of db keys for specific phrase | None -> list(str) """
    try:
        row = self.db.loc[phrase, :]
        return list(row[row==True].index)
    except KeyError:
        return []

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

