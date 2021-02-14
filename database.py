import pandas as pd
import numpy as np

def load_key_dataframe():
    try:
        key_df = pd.read_pickle('database/key.pickle')
        print('Loading saved key dataframe')
    except FileNotFoundError:
        print('Creating new key dataframe')
        key_df = pd.DataFrame.from_dict({})
    return key_df

def load_phrase_series():
    try:
        phrase_series = pd.read_pickle('database/phrase.pickle')
        print('Loading saved phrase series')
    except FileNotFoundError:
        print('Creating new phrase series')
        phrase_series = pd.Series([], dtype='object')
    return phrase_series

key_df = load_key_dataframe()
phrase_series = load_phrase_series()

def save():
    key_df.to_pickle('database/key.pickle')
    phrase_series.to_pickle('database/phrase.pickle')

def reset(): #Temp function / to be deleted
    import os
    os.remove('database/phrase.pickle')
    os.remove('database/key.pickle')
    
def add_column_if_missing(name, df):
    if not name in df.columns:
        df[name] = False

def get_index(df_or_s, default=None):
    index = df_or_s.last_valid_index()
    if index is None:
        return 0
    else:
        return index + 1

def add_keys(key_list, key_df):
    index = get_index(key_df, default=False)
    for key in key_list:
        add_column_if_missing(key, key_df)
    key_df.loc[index,key_list] = True
    other_columns = [column for column in key_df.columns if column not in key_list]
    key_df.loc[index, other_columns] = False
    return index

def add_phrase(phrase, phrase_series, index=None):
    if not index:
        index = get_index(phrase_series, default='')
    phrase_series.loc[index] = phrase

def save_entry(phrase, key_list, key_df=key_df, phrase_series=phrase_series):
    index = add_keys(key_list, key_df)
    add_phrase(phrase, phrase_series, index=index)
    save()
    
def get_phrase_list(key_list, key_df=key_df, phrase_series=phrase_series):
    try:
        mask = key_df.loc[key_df[key_list].all(axis=1), :].index #mask?
        print(mask)
        return list(phrase_series[mask].values)
    except KeyError:
        return None

def valid_keys(partial_key, key_df=key_df):
    if partial_key:
        mask = key_df.columns.str.lower().str.startswith(partial_key.lower())
        return list(key_df.columns[mask])
    return []
