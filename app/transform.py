import pandas as pd
import re

def camel_to_snake(column_name):
    return re.sub(r'(?<!^)(?=[A-Z])', '_', column_name).lower()

def normalize_columns(df: pd.DataFrame):
    rename = {}
    for c in df.columns:
        new_c = c.strip().lower().replace(" ", "_")
        new_c = camel_to_snake(new_c)
        rename[c] = new_c
    df = df.rename(columns=rename)
    return df

def is_datetime_object(c):
    DATE_KEYWORDS = re.compile(r"(date|datum|dag)", re.IGNORECASE)
    return DATE_KEYWORDS.search(c)

def is_financial(c):
    ENG_KEYWORDS = re.compile(r"(eur|dollar|price|value|balance|currency|usd|cost|fee|charge|net|gross|profit|tax|vat|credit|debit)", re.IGNORECASE)
    NL_KEYWORDS = re.compile(r"(prijs|bedrag|bruto|winst|waarde|saldo|kost)", re.IGNORECASE)

    return ENG_KEYWORDS.search(c) or NL_KEYWORDS.search(c)

def translate_numeric(df, c):
    c = c.strip().replace(",", ".")
    df[c] = pd.to_numeric(df[c], errors="coerce")
    return df
    

def parse_dates(df: pd.DataFrame, c):
    parsed = pd.to_datetime(df[c], errors="coerce", dayfirst=True)
    df[c] = parsed.dt.strftime("%d-%m-%Y")
    return df

    
def run_pipeline(df: pd.DataFrame):
    df = normalize_columns(df)
    for c in df.columns:
        if is_datetime_object(c):
            df = parse_dates(df, c)
        elif is_financial(c):
            df = translate_numeric(df, c)
    return df
