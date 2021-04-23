""" File operation utilities

Functions:
    get_default_dir

Folder structure:

All user info goes in the base path, which is user configurable. It defaults to
the system-specific user data directory.

base_path -> backup -> standard
                    -> translation -> language_pair_1
                                   -> language_pair_2
                                   -> language_pair_...
          -> config
          -> db
          -> session
"""

from pathlib import Path
from appdirs import user_data_dir

def get_default_dir():
    """ Gets default directory and creates it if needed | None -> Path """
    default_dir = Path(user_data_dir('KeyPhrase'))
    default_dir.mkdir(parents=True, exist_ok=True)
    return default_dir

def create_backup_dir(path=None):
    """ Creates standard db backup dir and returns path | Path -> Path """
    if not path:
        path = get_default_dir()
    backup_dir = path / 'backup'
    backup_dir.mkdir(parents=True, exist_ok=True)
    return backup_dir

def create_session_dir(path=None):
    """ Creates session dir if needed and returns path | Path -> Path """
    if not path:
        path = get_default_dir()
    session_dir = path / 'session'
    session_dir.mkdir(parents=True, exist_ok=True)
    return session_dir

def create_db_dir(path=None):
    """ Creates database dir if needed and returns path | Path -> Path """
    if not path:
        path = get_default_dir()
    db_dir = path / 'db'
    db_dir.mkdir(parents=True, exist_ok=True)
    return db_dir

def create_docs_dir(path=None):
    """ Creates docs dir if needed and returns path | Path -> Path """
    if not path:
        path = get_default_dir()
    docs_dir = path / 'config'
    docs_dir.mkdir(parents=True, exist_ok=True)
    return docs_dir
