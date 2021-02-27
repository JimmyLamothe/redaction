import argparse
import atexit
import tkinter as tk
from utilities import backup_db, restore_db, backup_config, restore_config
from utilities import delete_db, delete_config
@atexit.register
def cleanup(): #Must be registered before atexit functions in config module
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
import config

config.config_dict['test_mode'] = True
            
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

import database as db
    
db.generate_test_db(language=args.language, size=args.size)

from Root import Root

root = Root()

root.mainloop()
