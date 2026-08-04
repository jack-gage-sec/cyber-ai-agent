"""
Database loading functions.

Takes transformed DataFrames and inserts
them into PostgreSQL.
"""

import os
import sys

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "D:\Backup Files\Experiments\Compliance Evidence Pipeline"))

external_path = os.path.join(parent_dir, "Compliance-AI")
sys.path.append(external_path)

from database.connection import engine

from database.lineage import log_ingestion



def load_dataframe(
        df,
        table_name
):

    print(
        f"Loading {len(df)} records into {table_name}"
    )

    print(f"Loaders**** Loading {len(df)} records into {table_name}")
    print(df.columns.tolist())

    df.to_sql(
        table_name,
        engine,
        if_exists="append",
        index=False
    )

    log_ingestion(
        table_name,
        "synthetic_data/output",
        len(df)
    )


    print(
        f"Successfully loaded {table_name}"
    )