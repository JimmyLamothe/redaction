""" Database speedtests

This script is meant to test different database implementations for maximum speed.
"""

import argparse
import atexit
import cProfile
import tkinter as tk

@atexit.register
def cleanup(): #Must be registered before @atexit functions in config module
    if restore_config_on_exit:
        print('restoring config')
        restore_config()
    elif delete_config_on_exit:
        print('deleting config')
        try:
            delete_config()
        except FileNotFoundError:
            pass
    if restore_db_on_exit:
        print('restoring db')
        restore_db()
    elif delete_db_on_exit:
        print('deleting db')
        try:
            delete_db()
        except FileNotFoundError:
            pass

import config #Imported here for proper @atexit order

config.config_dict['test_mode'] = True

def backup_db():
    """ Create backup copy of database | None -> None """
    if config.config_dict['db'] == 'def':
        shutil.copy2('database/key.pickle', 'database/key_bkup.pickle')
    else:
        shutil.copy2('database/alt_key.pickle', 'database/alt_key_bkup.pickle')

def restore_db():
    """ Restore database from backup | None -> None """
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
            
try:
    backup_config()
    restore_config_on_exit = True
    delete_config_on_exit = False
except FileNotFoundError:
    restore_config_on_exit = False
    delete_config_on_exit = True

parser = argparse.ArgumentParser()

parser.add_argument('db',
                    help='Use "def" for default database or "alt" for comparison',
                    choices=['def', 'alt'])
parser.add_argument('size',
                    help='Databse size - int',
                    type=int,
                    default=500)
parser.add_argument('language',
                    help='Use "fr" for French and "en" for English',
                    choices=['en', 'fr'])

args = parser.parse_args()
config.config_dict['db'] = args.db

try:
    print('backing up db')
    backup_db()
    restore_db_on_exit = True
    delete_db_on_exit = False
    print('deleting db')
    delete_db()
except FileNotFoundError:
    restore_db_on_exit = False
    delete_db_on_exit = True

if args.db == 'alt':
    import database_alt as db
else:
    import database as db

pr=cProfile.Profile()
pr.enable()

db.generate_test_db(language=args.language, size=args.size)

pr.disable()

pr.print_stats(sort='cumtime')

from Root import Root

root = Root()

root.mainloop()
