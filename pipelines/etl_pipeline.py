"""
ETL transformations for compliance data.
"""

import pandas as pd



def normalize_columns(df):

    df.columns = (
        df.columns
        .str.lower()
        .str.strip()
    )

    return df



def normalize_dates(df):

    date_columns = [
        column
        for column in df.columns
        if "date" in column
        or "timestamp" in column
    ]


    for column in date_columns:

        df[column] = pd.to_datetime(
            df[column],
            errors="coerce"
        )

    return df



def normalize_severity(df):

    if "severity" in df.columns:

        df["severity"] = (
            df["severity"]
            .str.title()
        )

    return df



def transform(df):

    df = normalize_columns(df)

    df = normalize_dates(df)

    df = normalize_severity(df)

    return df