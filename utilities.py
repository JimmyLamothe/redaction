""" File operation utilities

Functions:
    get_default_dir
"""

from pathlib import Path
from appdirs import user_data_dir

def get_default_dir():
    """ Gets default directory and creates it if needed | None -> Path """
    default_dir = Path(user_data_dir('KeyPhrase'))
    default_dir.mkdir(parents=True, exist_ok=True)
    return default_dir

def get_default_backup():
    """ Gets default backup directory and creates it if needed | None -> Path """
    default_dir = get_default_dir()
    backup_dir = default_dir / 'backup'
    backup_dir.mkdir(parents=True, exist_ok=True)
    return backup_dir
