import shutil, os

def backup_db():
    import config #Here to preserve proper atexit registration order
    if config.config_dict['db'] == 'def':
        shutil.copy2('database/key.pickle', 'database/key_bkup.pickle')
        shutil.copy2('database/phrase.pickle', 'database/phrase_bkup.pickle')
    else:
        shutil.copy2('database/alt_key.pickle', 'database/alt_key_bkup.pickle')

def restore_db():
    import config #Here to preserve proper atexit registration order
    if config.config_dict['db'] == 'def':
        shutil.copy2('database/key_bkup.pickle', 'database/key.pickle')
        shutil.copy2('database/phrase_bkup.pickle', 'database/phrase.pickle')
        os.remove('database/key_bkup.pickle')
        os.remove('database/phrase_bkup.pickle')
    else:
        shutil.copy2('database/alt_key_bkup.pickle', 'database/alt_key.pickle')
        os.remove('database/alt_key_bkup.pickle')
def backup_config():
    shutil.copy2('config/config.json', 'config/config_bkup.json')

def restore_config():
    shutil.copy2('config/config_bkup.json', 'config/config.json')
    os.remove('config/config_bkup.json')
    
def delete_config():
    os.remove('config/config.json')

def delete_db():
    import config
    if config.config_dict['db'] == 'def':
        print('removing key.pickle and phrase.pickle')
        os.remove('database/key.pickle')
        os.remove('database/phrase.pickle')
        print(os.listdir('database'))
    else:
        print('removing alt_key.pickle')
        os.remove('database/alt_key.pickle')
