import pandas as pd
import numpy as np
import re


'''
methods 

def normalize_columns()
def parse_date(): forcing date column(s) to datetime objects
def cast_types(): forces columns to right types
def clean_strings(): from spaces and quotes
def missing_values(): 
def delete_duplicates():
'''

def camel_to_snake(column_name):
    return re.sub(r'(?<!^)(?=[A-Z])', '_', column_name).lower()


def normalize_columns(df: pd.DataFrame):
    for c in df.columns:
        df.columns = camel_to_snake(c)
        df.columns = c.strip().lower().replace(" ", "_")
    return df.columns

def run_pipeline(df: pd.DataFrame):
    return df