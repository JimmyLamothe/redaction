import pandas as pd
import numpy as np

def load_key_dataframe():
    try:
        with open('database/key.csv', 'r') as key_file:
            key_df = pd.read_csv(key_file, delimiter=',')
            print('Loading saved key dataframe')
    except FileNotFoundError:
        print('Creating new key dataframe')
        key_df = pd.DataFrame.from_dict({})
    return key_df

def load_phrase_series():
    try:
        with open('database/phrase.csv', 'r') as phrase_file:
            phrase_series = pd.read_csv(phrase_file, delimiter=',')
            print('Loading saved phrase series')
    except FileNotFoundError:
        print('Creating new phrase series')
        phrase_series = pd.Series([], dtype='object')
    return phrase_series

key_df = load_key_dataframe()
phrase_series = load_phrase_series()

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

def add_entry(phrase, key_list, phrase_series, key_df):
    index = add_keys(key_list, key_df)
    add_phrase(phrase, phrase_series, index=index)

def get_phrase_list(key_list, key_df, phrase_series):
    return phrase_series[key_df.loc[key_df[key_list].all(axis=1), :].index].values

def save_entry(phrase, key_list):
    print(phrase)
    print(key_list)
    add_entry(phrase, key_list, phrase_series, key_df)

active_phrases = None

current_index = None

def next_entry():
    try:
        return active_phrases[current_index+1]
    except IndexError or TypeError:
        return None

def previous_entry():
    try:
        return active_phrases[current_index-1]
    except IndexError or TypeError:
        return None
