import pandas as pd

def load_data(file):
    return pd.read_csv(file)

def missing_values(df):
    return df.isnull().sum()

def duplicate_count(df):
    return df.duplicated().sum()

def remove_duplicates(df):
    return df.drop_duplicates()

def clean_missing(df):
    return df.dropna()