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
def test_standard_add_column_if_missing():
    test_db = standard_test_db()
    test_db.add_column_if_missing('e')
    assert test_db.get_index() == ['phrase 1', 'phrase 2']
    assert test_db.get_columns() == ['a', 'b', 'c', 'd', 'e']
    assert test_db.db['e'].any() == False

@delete_test_db
def test_standard_save_entry():
    test_db = standard_test_db()
    assert test_db.get_index() == ['phrase 1','phrase 2']
    assert test_db.get_columns() == ['a','b','c','d']
    test_db.save_entry([],'phrase 2')
    assert test_db.get_index() == ['phrase 1']
    assert test_db.get_columns() == ['a','b']
    test_db.save_entry([], 'not_in_db')
    assert test_db.get_index() == ['phrase 1']
    assert test_db.get_columns() == ['a','b']
    test_db.save_entry(['key_1', 'a', 'key_2'], 'new_phrase')
    assert test_db.get_index() == ['phrase 1', 'new_phrase']
    assert test_db.get_columns() == ['a','b', 'key_1', 'key_2']

@delete_test_db
def test_standard_delete_phrase():
    test_db = standard_test_db()
    assert test_db.get_index() == ['phrase 1','phrase 2']
    assert test_db.get_columns() == ['a','b','c','d']
    test_db.delete_phrase('')
    assert test_db.get_index() == ['phrase 1','phrase 2']
    assert test_db.get_columns() == ['a','b','c','d']
    test_db.delete_phrase('afgasdfg')
    assert test_db.get_index() == ['phrase 1','phrase 2']
    assert test_db.get_columns() == ['a','b','c','d']
    test_db.delete_phrase('phrase 1')
    assert test_db.get_index() == ['phrase 2']
    assert test_db.get_columns() == ['c','d']

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

def translation_test_db():
    test_db = TranslationDatabase('Français','English')
    test_db.save_entry('mouton','lamb')
    test_db.save_entry('porc', 'pork')
    return test_db
    
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

@delete_test_db
def test_translation_add_row_if_missing():
    test_db = translation_test_db()
    test_db.add_row_if_missing('chicken')
    assert test_db.get_index() == ['lamb', 'pork', 'chicken']
    assert test_db.get_columns() == ['mouton', 'porc']
    assert test_db.db.loc['chicken'].any() == False

@delete_test_db
def test_translation_add_column_if_missing():
    test_db = translation_test_db()
    test_db.add_column_if_missing('poulet')
    assert test_db.get_index() == ['lamb', 'pork']
    assert test_db.get_columns() == ['mouton', 'porc', 'poulet']
    assert test_db.db['poulet'].any() == False
            
@delete_test_db
def test_translation_save_entry():
    test_db = translation_test_db()
    assert test_db.get_index() == ['lamb', 'pork']
    assert test_db.get_columns() == ['mouton', 'porc']
    test_db.save_entry('', '')
    assert test_db.get_index() == ['lamb', 'pork']
    assert test_db.get_columns() == ['mouton', 'porc']
    test_db.save_entry('nouveau', '')
    assert test_db.get_index() == ['lamb', 'pork']
    assert test_db.get_columns() == ['mouton', 'porc']
    test_db.save_entry('', 'new')
    assert test_db.get_index() == ['lamb', 'pork']
    assert test_db.get_columns() == ['mouton', 'porc']
    test_db.save_entry('boeuf', 'beef')
    assert test_db.get_index() == ['lamb', 'pork', 'beef']
    assert test_db.get_columns() == ['mouton', 'porc', 'boeuf']
    test_db.save_entry('mouton', 'mutton')
    assert test_db.get_index() == ['lamb', 'pork', 'beef', 'mutton']
    assert test_db.get_columns() == ['mouton', 'porc', 'boeuf']

@delete_test_db
def test_translation_delete_match():
    test_db = translation_test_db()
    assert test_db.get_index() == ['lamb', 'pork']
    assert test_db.get_columns() == ['mouton', 'porc']
    test_db.delete_match('', '')
    assert test_db.get_index() == ['lamb', 'pork']
    assert test_db.get_columns() == ['mouton', 'porc']
    test_db.delete_match('nouveau', '')
    assert test_db.get_index() == ['lamb', 'pork']
    assert test_db.get_columns() == ['mouton', 'porc']
    test_db.delete_match('', 'new')
    assert test_db.get_index() == ['lamb', 'pork']
    assert test_db.get_columns() == ['mouton', 'porc']
    test_db.delete_match('boeuf', '')
    assert test_db.get_index() == ['lamb', 'pork']
    assert test_db.get_columns() == ['mouton', 'porc']
    test_db.delete_match('', 'beef')
    assert test_db.get_index() == ['lamb', 'pork']
    assert test_db.get_columns() == ['mouton', 'porc']
    test_db.delete_match('porc', 'pork')
    assert test_db.get_index() == ['lamb']
    assert test_db.get_columns() == ['mouton']
    test_db.save_entry('mouton', 'mutton')
    test_db.delete_match('mouton', 'lamb')
    assert test_db.get_index() == ['mutton']
    assert test_db.get_columns() == ['mouton']
   
def test_translation_get_lang1_matches():
    test_db = translation_test_db()
    assert test_db.get_lang1_matches('') == []
    assert test_db.get_lang1_matches('chicken') == []
    assert test_db.get_lang1_matches('pork') == ['porc']
    assert test_db.get_lang1_matches('lamb') == ['mouton']
    test_db.save_entry('agneau', 'lamb')
    assert test_db.get_lang1_matches('lamb') == ['mouton', 'agneau']

def test_translation_get_lang2_matches():
    test_db = translation_test_db()
    assert test_db.get_lang2_matches('') == []
    assert test_db.get_lang2_matches('poulet') == []
    assert test_db.get_lang2_matches('porc') == ['pork']
    assert test_db.get_lang2_matches('mouton') == ['lamb']
    test_db.save_entry('mouton', 'mutton')
    assert test_db.get_lang2_matches('mouton') == ['lamb', 'mutton']

def test_translation_valid_lang1_keys():
    test_db = translation_test_db()
    assert test_db.valid_lang1_keys('') == []
    assert test_db.valid_lang1_keys('pou') == []
    assert test_db.valid_lang1_keys('porcin') == []
    assert test_db.valid_lang1_keys('m') == ['mouton']
    assert test_db.valid_lang1_keys('mout') == ['mouton']
    assert test_db.valid_lang1_keys('mouton') == ['mouton']
    assert test_db.valid_lang1_keys('p') == ['porc']
    assert test_db.valid_lang1_keys('porc') == ['porc']
    test_db.save_entry('poulet', 'chicken')
    assert test_db.valid_lang1_keys('p') == ['porc', 'poulet']
    assert test_db.valid_lang1_keys('po') == ['porc', 'poulet']
    assert test_db.valid_lang1_keys('por') == ['porc']
    assert test_db.valid_lang1_keys('pou') == ['poulet']
    assert test_db.valid_lang1_keys('porc') == ['porc']
    assert test_db.valid_lang1_keys('poulet') == ['poulet']
    
def test_translation_valid_lang2_keys():
    test_db = translation_test_db()
    assert test_db.valid_lang2_keys('') == []
    assert test_db.valid_lang2_keys('pou') == []
    assert test_db.valid_lang2_keys('lambi') == []
    assert test_db.valid_lang2_keys('l') == ['lamb']
    assert test_db.valid_lang2_keys('lam') == ['lamb']
    assert test_db.valid_lang2_keys('lamb') == ['lamb']
    assert test_db.valid_lang2_keys('p') == ['pork']
    assert test_db.valid_lang2_keys('pork') == ['pork']
    test_db.save_entry('poulet', 'poultry')
    assert test_db.valid_lang2_keys('p') == ['pork', 'poultry']
    assert test_db.valid_lang2_keys('po') == ['pork', 'poultry']
    assert test_db.valid_lang2_keys('por') == ['pork']
    assert test_db.valid_lang2_keys('pou') == ['poultry']
    assert test_db.valid_lang2_keys('pork') == ['pork']
    assert test_db.valid_lang2_keys('poultry') == ['poultry']
    assert test_db.valid_lang2_keys('porky') == []
