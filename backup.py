"""
The backup module stores four backups of the database. One from the previous day,
one from the previous week, one from the previous month, and one from the previous
year. As new backups are made, previous ones are deleted.

It also implements undo and redo functionality using temporary saved
database states that are deleted at session end.
"""

import atexit
import shutil
import json
from pathlib import Path
from datetime import date
import config

DEFAULT_DATES = {
    'day': None, #Time of last daily backup (1 day)
    'week': None, #Time of last weekly backup (7 days)
    'month': None, #Time of last monthly backup (30 days)
    'year': None #Time of last yearly backup (365 days)
    }

def date_from_string(date_string):
    """ Creates date object from date string | str -> datetime.Date """
    return date(*[int(item) for item in date_string.split('-')])

def load_backup_dates():
    """ Loads backup dates from disk or returns default setting | None -> dict """
    try:
        with open('config/backup_dates.json', 'r') as date_file:
            backup_date_dict = json.load(date_file)
            backup_date_dict = {k:date_from_string(v)
                                for k, v in backup_date_dict.items()}
            print('Loading backup dates:', backup_date_dict)
    except (FileNotFoundError, ValueError):
        print('Loading empty backup dates:', DEFAULT_DATES)
        backup_date_dict = DEFAULT_DATES
    return backup_date_dict

#Dates of most recent daily, weekly, monthly and yearly backups
backup_date_dict = load_backup_dates()

def save_backup_dates():
    """ Saves backup dates to disk | None -> None """
    with open('config/backup_dates.json', 'w') as date_file:
        print('Saving backup dates:', backup_date_dict)
        json.dump(backup_date_dict, date_file, default=str)

def new_day():
    """ Checks if 1 day has passed since last backup | None -> bool """
    if not backup_date_dict['day'] == date.today():
        return True
    return False

def new_week():
    """ Checks if 7 days have passed since last backup | None -> bool """
    if not backup_date_dict['week']:
        return True
    diff = date.today() - backup_date_dict['week']
    if diff.days > 6:
        return True
    return False

def new_month():
    """ Checks if 30 days have passed since last backup | None -> bool """
    if not backup_date_dict['month']:
        return True
    diff = date.today() - backup_date_dict['month']
    if diff.days > 29:
        return True
    return False

def new_year():
    """ Checks if 365 days have passed since last backup | None -> bool """
    if not backup_date_dict['year']:
        return True
    diff = date.today() - backup_date_dict['year']
    if diff.days > 364:
        return True
    return False

def daily_backup():
    """ Performs daily backup | None -> None """
    print('daily backup in progress')
    db_filepath = config.get_full_db_path()
    backup_path = config.get_backup_path()
    backup_filepath = backup_path / 'daily.pickle'
    print(f'saving {backup_filepath}')
    shutil.copy(db_filepath, backup_filepath)
    backup_date_dict['day'] = date.today()
    save_backup_dates()

def weekly_backup():
    """ Performs weekly backup | None -> None """
    print('weekly backup in progress')
    db_filepath = config.get_full_db_path()
    backup_path = config.get_backup_path()
    backup_filepath = backup_path / 'weekly.pickle'
    print(f'saving {backup_filepath}')
    shutil.copy(db_filepath, backup_filepath)
    backup_date_dict['week'] = date.today()
    save_backup_dates()
    
def monthly_backup():
    """ Performs monthly backup | None -> None """
    print('monthly backup in progress')
    db_filepath = config.get_full_db_path()
    backup_path = config.get_backup_path()
    backup_filepath = backup_path / 'monthly.pickle'
    print(f'saving {backup_filepath}')
    shutil.copy(db_filepath, backup_filepath)
    backup_date_dict['month'] = date.today()
    save_backup_dates()
    
def yearly_backup():
    """ Performs yearly backup | None -> None """
    print('yearly backup in progress')
    db_filepath = config.get_full_db_path()
    backup_path = config.get_backup_path()
    backup_filepath = backup_path / 'yearly.pickle'
    print(f'saving {backup_filepath}')
    shutil.copy(db_filepath, backup_filepath)
    backup_date_dict['year'] = date.today()
    save_backup_dates()
    
def backup():
    """ Performs all backups if needed | None -> None """
    if new_day():
        daily_backup()
    if new_week():
        weekly_backup()
    if new_month():
        monthly_backup()
    if new_year():
        yearly_backup()
