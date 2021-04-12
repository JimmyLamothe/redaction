"""
The backup module stores four backups of the database. One from the previous day,
one from the previous week, one from the previous month, and one from the previous
year. As new backups are made, previous ones are deleted.
"""

import shutil
import json
from datetime import date
import config


DEFAULT_DATES = {
    'day': None, #Time of last daily backup (1 day)
    'week': None, #Time of last weekly backup (7 days)
    'month': None, #Time of last monthly backup (30 days)
    'year': None #Time of last yearly backup (365 days)
    }

def load_backup_dates():
    """ Loads backup dates from disk or returns default setting | None -> dict """
    try:
        with open('config/backup_dates.json', 'r') as date_file:
            backup_date_dict = json.load(date_file)
            print('Loading backup dates:', backup_date_dict)
    except (FileNotFoundError, ValueError):
        print('Loading empty backup dates:', DEFAULT_DATES)
        backup_date_dict = DEFAULT_DATES
    return backup_date_dict

backup_date_dict = load_backup_dates()

def save_backup_dates():
    """ Saves backup dates to disk | None -> None """
    with open('config/backup_dates.json', 'w') as date_file:
        print('Saving backup dates:', backup_date_dict)
        json.dump(backup_date_dict, date_file)

def new_day():
    if not backup_date_dict['day'] == date.today():
        return True
    return False

def new_week():
    if not backup_date_dict['week']:
        return True
    diff = date.today() - backup_date_dict['week']
    if diff.days > 7:
        return True
    return False

def new_month():
    if not backup_date_dict['month']:
        return True
    diff = date.today() - backup_date_dict['month']
    if diff.days > 29:
        return True
    return False

def new_year():
    if not backup_date_dict['year']:
        return True
    diff = date.today() - backup_date_dict['year']
    if diff.days > 365:
        return True
    return False

def daily_backup():
    print('daily backup in progress')
    db_filepath = config.get_full_db_path()
    backup_path = config.get_backup_path()
    backup_filepath = backup_path / 'daily.pickle'
    print(f'saving {backup_filepath}')
    shutil.copy(db_filepath, backup_filepath)

def weekly_backup():
    print('weekly backup in progress')
    db_filepath = config.get_full_db_path()
    backup_path = config.get_backup_path()
    backup_filepath = backup_path / 'weekly.pickle'
    print(f'saving {backup_filepath}')
    shutil.copy(db_filepath, backup_filepath)

def monthly_backup():
    print('monthly backup in progress')
    db_filepath = config.get_full_db_path()
    backup_path = config.get_backup_path()
    backup_filepath = backup_path / 'monthly.pickle'
    print(f'saving {backup_filepath}')
    shutil.copy(db_filepath, backup_filepath)

def yearly_backup():
    print('yearly backup in progress')
    db_filepath = config.get_full_db_path()
    backup_path = config.get_backup_path()
    backup_filepath = backup_path / 'yearly.pickle'
    print(f'saving {backup_filepath}')
    shutil.copy(db_filepath, backup_filepath)
    
def backup():
    if new_day():
        daily_backup()
    if new_week():
        weekly_backup()
    if new_month():
        monthly_backup()
    if new_year():
        yearly_backup()

