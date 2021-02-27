import pandas as pd
import numpy as np

def load_key_dataframe():
    try:
        key_df = pd.read_pickle('database/alt_key.pickle')
        print('Loading saved alt key dataframe')
    except FileNotFoundError:
        print('No saved alt key dataframe')
        key_df = None
    return key_df

def get_phrase_series():
    return key_df.index

key_df = load_key_dataframe()

def save(key_df):
    key_df.to_pickle('database/alt_key.pickle')

def reset(): #Temp function / to be deleted
    import os
    os.remove('database/alt_key.pickle')

def backup():
    shutil.copy2('database/alt_key.pickle', 'database/alt_key_bkup.pickle')

def restore():
    shutil.copy2('database/alt_key_bkup.pickle', 'database/alt_key.pickle')
    
def add_column_if_missing(name, df):
    if not name in df.columns:
        df[name] = False

def initialize_key_df(phrase, key_list):
    print('Initializing DataFrame')
    row_data = []
    for i in range(len(key_list)):
        row_data.append(True)
    key_df = pd.DataFrame.from_dict({phrase:row_data},
                                    orient='index',
                                    columns=key_list)
    return key_df

def save_entry(phrase, key_list, key_df=key_df):
    if key_df is None:
        key_df = initialize_key_df(phrase, key_list)
        save_entry(phrase, key_list, key_df=key_df)
    else:
        print('Found DataFrame')
        key_df.loc[phrase] = False #Initialize row with all False 
        for key in key_list:
            add_column_if_missing(key, key_df) #Add missing new keys 
        key_df.loc[phrase, key_list] = True #Set keys to True
        print(key_df)
    save(key_df)
    
def get_phrase_list(key_list, key_df=key_df):
    try:
        index = key_df.loc[key_df[key_list].all(axis=1), :].index
        return list(index.values)
    except KeyError:
        return None

def valid_keys(partial_key, key_df=key_df):
    if partial_key:
        mask = key_df.columns.str.lower().str.startswith(partial_key.lower())
        return list(key_df.columns[mask])
    return []
