""" Tests for database module

Not all functions have tests, add more tests as bugs arise
"""

def load_database():
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

db = load_database() #The application database (Pandas DataFrame)

def reload_database():
    """ Reload db from disk - used for undo and redo """
    global db
    db = load_database()

def get_phrase_series():
    """ Gets phrase Series from key DataFrame | None -> pd.Series """
    return db.index

def save():
    """ Save contents of database to disk | db.DataFrame -> None """
    global db
    db.to_pickle(config.get_full_db_path())
    
def add_column_if_missing(name):
    """ Initializes column if it doesn't exist | str, pd.DataFrame -> None """
    global db
    if not name in db.columns:
        db[name] = False

def initialize_db(key_list, phrase):
    """ Create new database on first startup | list(str), str -> pd.DataFrame """
    print('Initializing database')
    global db
    row_data = []
    for i in range(len(key_list)):
        row_data.append(True)
    db = pd.DataFrame.from_dict({phrase:row_data},
                                    orient='index',
                                    columns=key_list)
    db.to_pickle(config.get_full_db_path())

def strip_trailing_newline(string):
    """ Removes last character recursively while it's a new line | str -> str """
    if string[-1] in ['\n','\r']:
        return strip_trailing_newline(string[:-1])
    return string
    
def save_entry(key_list, phrase):
    """ Save new key/phrase combination to database | list(str), str -> None """
    global db
    if not phrase: #To prevent accidental empty phrase entry
        return
    if db.empty: #If first entry, initialize new database
        initialize_db(key_list, phrase)
        save_entry(key_list, phrase)
    else:
        print('Found DataFrame')
        if not key_list: #If no keys given
            try:
                db = db.drop(phrase) #Used to delete phrase from database
            except KeyError:
                return
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

#Paths of backup database saves for current session
undo_db_list = []

redo_db_list = []

def generate_undo_filepath():
    """ Generate filepath for undo file | None -> Path """
    session_path = config.get_session_path()
    name = 'undo_' + str(len(undo_db_list)) + '.pickle'
    filepath = session_path / name
    return filepath

def prepare_undo():
    """ Saves current db state to undo file and saves path | None -> None """
    db_filepath = config.get_full_db_path()
    filepath = generate_undo_filepath()
    shutil.copy(db_filepath, filepath)
    undo_db_list.append(filepath)

def generate_redo_filepath():
    """ Generate filepath for redo file | None -> Path """
    session_path = config.get_session_path()
    name = 'redo_' + str(len(redo_db_list)) + '.pickle'
    filepath = session_path / name 
    return filepath

def prepare_redo():
    """ Saves current db state to redo file and saves path | None -> None """
    db_filepath = config.get_full_db_path()
    filepath = generate_redo_filepath()
    shutil.copy(db_filepath, filepath)
    redo_db_list.append(filepath)
    
def undo():
    """ Reverts previous database save command | None -> None """
    if not undo_db_list: #If no previous saved state
        return
    #Part 1: Save current state to temp backup
    prepare_redo()
    #Part 2: Revert previous save command
    db_filepath = config.get_full_db_path()
    revert_filepath = undo_db_list[-1]
    shutil.copy(revert_filepath, db_filepath)
    undo_db_list.pop().unlink()
    reload_database()
    
def redo():
    """ Reverts previous undo call | None -> None """
    if not redo_db_list: # If no undo in memory
        return
    #Part 1: Save current state to temp backup
    prepare_undo()
    #Part 2: Revert previous undo command
    db_filepath = config.get_full_db_path()
    revert_filepath = redo_db_list[-1]
    shutil.copy(revert_filepath, db_filepath)
    redo_db_list.pop().unlink()
    reload_database()
