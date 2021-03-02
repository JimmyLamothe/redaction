""" File operation utilities

Note that some imports are done in function definitions to preserve proper
order of functions registered with atexit.

Functions:
    backup_db()
    restore_db()
    delete_db()
    backup_config()
    restore_config()
    delete_config()
"""

import shutil, os

def backup_db():
    """ Create backup copy of database | None -> None """
    import config #Here to preserve proper atexit registration order
    if config.config_dict['db'] == 'def':
        shutil.copy2('database/key.pickle', 'database/key_bkup.pickle')
    else:
        shutil.copy2('database/alt_key.pickle', 'database/alt_key_bkup.pickle')

def restore_db():
    """ Restore database from backup | None -> None """
    import config #Here to preserve proper atexit registration order
    if config.config_dict['db'] == 'def':
        shutil.copy2('database/key_bkup.pickle', 'database/key.pickle')
        os.remove('database/key_bkup.pickle')
    else:
        shutil.copy2('database/alt_key_bkup.pickle', 'database/alt_key.pickle')
        os.remove('database/alt_key_bkup.pickle')

def delete_db():
    """ Delete saved database | None -> None
    
    NOTE: Must never be called in production except as part
    of a heavily vetted, safe procedure with proper backups
    """
    import config #Here to preserve proper atexit registration order
    if config.config_dict['db'] == 'def':
        print('removing key.pickle')
        os.remove('database/key.pickle')
        print(os.listdir('database'))
    else:
        print('removing alt_key.pickle')
        os.remove('database/alt_key.pickle')        

def backup_config():
    """ Create backup copy of config file | None -> None """
    shutil.copy2('config/config.json', 'config/config_bkup.json')

def restore_config():
    """ Restore config file from backup | None -> None """
    shutil.copy2('config/config_bkup.json', 'config/config.json')
    os.remove('config/config_bkup.json')
    
def delete_config():
    """ Delete config file | None -> None
    
    Not as crucial as the database, but also should not be called
    except as part of a properly vetted procedure with backups.
    """
    os.remove('config/config.json')

